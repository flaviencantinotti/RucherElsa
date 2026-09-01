#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rejoue un template Elementor en HTML, pour le voir sans WordPress.

Ce n'est pas Elementor : c'est une reimplementation de ses regles de mise
en page sur les reglages effectivement utilises par nos generateurs
(flex, largeurs, marges interieures, gouttieres, fonds, rayons, ombres).
Suffisant pour attraper ce qu'un controle statique ne voit pas — un
debordement, une colonne qui ne s'empile pas, un texte illisible sur
telephone.

Les points de rupture sont ceux d'Elementor par defaut :
tablette <= 1024 px, mobile <= 767 px.

Usage : python3 apercu_elementor.py site/01-accueil.json [sortie.html]
"""

import json
import os
import sys

TABLETTE = 1024
MOBILE = 767

_cls = [0]


def classe():
    _cls[0] += 1
    return "e%d" % _cls[0]


def px(v):
    """Valeur de curseur Elementor -> longueur CSS."""
    if not isinstance(v, dict):
        return None
    taille = v.get("size")
    if taille == "" or taille is None:
        return None
    return "%s%s" % (taille, v.get("unit", "px"))


def boite(v):
    """Valeur de marge/padding Elementor -> raccourci CSS."""
    if not isinstance(v, dict):
        return None
    u = v.get("unit", "px")
    cotes = [v.get(c, "") for c in ("top", "right", "bottom", "left")]
    if all(c in ("", None) for c in cotes):
        return None
    return " ".join("%s%s" % (c or 0, u) for c in cotes)


def regles(s, conteneur, partiel=False):
    """Traduit un dictionnaire de reglages en declarations CSS.

    partiel=True pour les declinaisons tablette et mobile : on n'emet
    alors que les proprietes reellement declinees. Sinon la passe
    responsive reposerait les valeurs par defaut du conteneur et
    ecraserait la direction du bureau — une rangee redeviendrait une
    colonne des qu'un seul reglage tablette existe.
    """
    d = {}

    if s.get("_flex_align_self"):
        d["align-self"] = s["_flex_align_self"]

    if conteneur:
        if not partiel:
            d["display"] = "flex"
            d["flex-direction"] = s.get("flex_direction") or "column"
            d["flex-wrap"] = s.get("flex_wrap") or "nowrap"
        else:
            if s.get("flex_direction"):
                d["flex-direction"] = s["flex_direction"]
            if s.get("flex_wrap"):
                d["flex-wrap"] = s["flex_wrap"]
        if s.get("flex_justify_content"):
            d["justify-content"] = s["flex_justify_content"]
        if s.get("flex_align_items"):
            d["align-items"] = s["flex_align_items"]
        g = px(s.get("flex_gap"))
        if g:
            d["gap"] = g
        # Elementor ne connait que grow / shrink / custom pour _flex_size.
        # Toute autre valeur ne produit aucune regle, et un conteneur
        # enfant vaut alors 100 % — c'est son defaut. L'apercu doit
        # modeliser ce defaut, sinon il montre une mise en page que
        # WordPress ne produira jamais.
        if s.get("_flex_size") in ("grow", "shrink", "custom"):
            d["flex"] = {"grow": "1 1 auto", "shrink": "0 1 auto",
                         "custom": "0 0 auto"}[s["_flex_size"]]
        if s.get("overflow"):
            d["overflow"] = s["overflow"]

        largeur = px(s.get("width"))
        if largeur:
            d["width"] = largeur
        elif not partiel and s.get("content_width") == "full":
            # Defaut d'Elementor pour un conteneur enfant sans largeur.
            d["width"] = "100%"
        elif not partiel and s.get("content_width") == "boxed":
            # Elementor : fond pleine largeur, contenu centre.
            d["width"] = "100%"
            d["align-items"] = s.get("flex_align_items") or "stretch"
        h = px(s.get("min_height"))
        if h:
            d["min-height"] = h

    p = boite(s.get("padding")) or boite(s.get("text_padding"))
    if p:
        d["padding"] = p
    m = boite(s.get("margin"))
    if m:
        d["margin"] = m

    # Image de fond, avec sa superposition eventuelle : c'est ainsi que
    # le site pose ses photos, pas via le widget Image.
    img = (s.get("background_image") or {}).get("url")
    voile = s.get("background_overlay_color")
    voile_b = s.get("background_overlay_color_b")
    if img:
        couches = []
        if voile and voile_b:
            couches.append("linear-gradient(%s, %s)" % (voile, voile_b))
        elif voile:
            couches.append("linear-gradient(%s, %s)" % (voile, voile))
        couches.append("url('%s')" % img)
        d["background-image"] = ", ".join(couches)
        d["background-size"] = s.get("background_size", "cover")
        d["background-position"] = s.get("background_position", "center center")
        d["background-repeat"] = "no-repeat"
    elif s.get("background_background") == "classic" and s.get("background_color"):
        d["background"] = s["background_color"]
    elif not conteneur and s.get("background_color"):
        # Le bouton porte sa couleur de fond sans drapeau background_background.
        d["background"] = s["background_color"]
    elif s.get("background_background") == "gradient":
        a = s.get("background_color", "#000")
        b = s.get("background_color_b", "#fff")
        ang = px(s.get("background_gradient_angle")) or "180deg"
        d["background"] = "linear-gradient(%s, %s, %s)" % (ang, a, b)

    r = boite(s.get("border_radius"))
    if r:
        d["border-radius"] = r
    if s.get("border_border"):
        d["border-style"] = s["border_border"]
        d["border-width"] = boite(s.get("border_width")) or "1px"
        d["border-color"] = s.get("border_color", "#ddd")

    if s.get("box_shadow_box_shadow_type") == "yes":
        o = s.get("box_shadow_box_shadow") or {}
        d["box-shadow"] = "%spx %spx %spx %spx %s" % (
            o.get("horizontal", 0), o.get("vertical", 0), o.get("blur", 0),
            o.get("spread", 0), o.get("color", "rgba(0,0,0,.1)"))

    # Liste d'icones : space_between est la gouttiere entre entrees,
    # et la typographie passe par le groupe icon_typography.
    if s.get("space_between"):
        d["gap"] = px(s["space_between"])
    if s.get("icon_typography_font_family"):
        d["font-family"] = "'%s', system-ui, sans-serif" % s["icon_typography_font_family"]
    if s.get("icon_typography_font_size"):
        d["font-size"] = px(s["icon_typography_font_size"])
    if s.get("icon_typography_font_weight"):
        d["font-weight"] = s["icon_typography_font_weight"]

    # Typographie
    if s.get("title_color"):
        d["color"] = s["title_color"]
    if s.get("text_color"):
        d["color"] = s["text_color"]
    if s.get("button_text_color"):
        d["color"] = s["button_text_color"]
    f = s.get("typography_font_family")
    if f:
        d["font-family"] = "'%s', system-ui, sans-serif" % f
    t = px(s.get("typography_font_size"))
    if t:
        d["font-size"] = t
    if s.get("typography_font_weight"):
        d["font-weight"] = s["typography_font_weight"]
    if s.get("typography_font_style"):
        d["font-style"] = s["typography_font_style"]
    lh = px(s.get("typography_line_height"))
    if lh:
        d["line-height"] = lh
    ls = px(s.get("typography_letter_spacing"))
    if ls:
        d["letter-spacing"] = ls
    if s.get("typography_text_transform"):
        d["text-transform"] = s["typography_text_transform"]
    if s.get("align"):
        d["text-align"] = s["align"]

    return d


def bloc_css(sel, d):
    if not d:
        return ""
    return "%s{%s}" % (sel, "".join("%s:%s;" % kv for kv in d.items()))


# Masquage responsive natif d'Elementor : hide_desktop, hide_tablet et
# hide_mobile posent des classes qu'Elementor masque via sa propre
# feuille. L'apercu doit les honorer, sinon il montre visible ce que
# WordPress cache — c'est ce qui m'a fait croire le burger corrige.
MASQUAGE = {"hide_desktop": (TABLETTE + 1, None),
            "hide_tablet": (MOBILE + 1, TABLETTE),
            "hide_mobile": (None, MOBILE)}


def regles_masquage(s, cl, css, css_tab, css_mob, css_plage):
    for cle, (mini, maxi) in MASQUAGE.items():
        if not s.get(cle):
            continue
        if cle == "hide_desktop":
            css.append(".%s{display:none!important}" % cl)
        elif cle == "hide_tablet":
            css_plage.append(".%s{display:none!important}" % cl)
        else:
            css_mob.append(".%s{display:none!important}" % cl)


def variantes(s, conteneur, cl, css, css_tab, css_mob, css_plage):
    """Genere la regle bureau et ses declinaisons tablette et mobile."""
    css.append(bloc_css("." + cl, regles(s, conteneur)))
    regles_masquage(s, cl, css, css_tab, css_mob, css_plage)
    for suffixe, cible in (("_tablet", css_tab), ("_mobile", css_mob)):
        sous = {k[:-len(suffixe)]: v for k, v in s.items()
                if k.endswith(suffixe)}
        if sous:
            cible.append(bloc_css("." + cl,
                                  regles(sous, conteneur, partiel=True)))


def rendre_widget(el, cl):
    s = el["settings"]
    wt = el.get("widgetType")

    if wt == "heading":
        return "<div class='%s w-heading'>%s</div>" % (cl, s.get("title", ""))
    if wt == "text-editor":
        return "<div class='%s w-text'>%s</div>" % (cl, s.get("editor", ""))
    if wt == "button":
        # Elementor pose le fond, le rayon et le padding sur le <a>, pas sur
        # le bloc qui l'entoure : la classe va donc sur le bouton lui-meme.
        aligne = s.get("align", "left")
        boite_align = {"left": "flex-start", "center": "center",
                       "right": "flex-end"}.get(aligne, "flex-start")
        return ("<div class='w-btnwrap' style='display:flex;justify-content:%s'>"
                "<span class='%s btn'>%s</span></div>"
                % (boite_align, cl, s.get("text", "")))
    if wt == "icon-list":
        lignes = []
        for i in s.get("icon_list", []):
            ico = (i.get("selected_icon") or {}).get("value")
            puce = "<span class='ico'>✓</span>" if ico else ""
            texte = i.get("text", "")
            lien = (i.get("link") or {}).get("url")
            if lien:
                texte = "<a href='%s'>%s</a>" % (lien, texte)
            lignes.append("<li>%s<span>%s</span></li>" % (puce, texte))
        # view=inline : les entrees s'alignent en ligne, cas des menus.
        mode = "w-list-inline" if s.get("view") == "inline" else ""
        return "<ul class='%s w-list %s'>%s</ul>" % (cl, mode, "".join(lignes))
    if wt == "spacer":
        return "<div class='%s' style='height:%s'></div>" % (
            cl, px(s.get("space")) or "20px")
    if wt == "image":
        # Hauteur et recadrage natifs du widget Image.
        sup = []
        if px(s.get("height")):
            sup.append("height:%s" % px(s["height"]))
        if s.get("object-fit"):
            sup.append("object-fit:%s" % s["object-fit"])
        if s.get("object-position"):
            sup.append("object-position:%s" % s["object-position"])
        style_sup = (" style=\"%s\"" % ";".join(sup)) if sup else ""
        im = s.get("image") or {}
        src = im.get("url")
        if src:
            # Vraie balise, avec son alt : c'est ce qu'on cherche a verifier.
            return ("<img class='%s' src='%s' alt='%s'%s>"
                    % (cl, src, im.get("alt", "").replace("'", "&#39;"),
                       style_sup))
        return "<div class='%s w-img'>emplacement image</div>" % cl
    if wt == "html":
        # Rendu tel quel : c'est le seul moyen de verifier que le bloc
        # d'effets produit bien ce qu'on attend.
        return s.get("html", "")
    if wt == "google_maps":
        return ("<div class='%s w-map'>plan Google Maps — %s</div>"
                % (cl, s.get("address", "")))
    return "<div class='%s'>[%s]</div>" % (cl, wt)


def rendre(el, css, css_tab, css_mob, css_plage):
    cl = classe()
    conteneur = el["elType"] == "container"
    variantes(el["settings"], conteneur, cl, css, css_tab, css_mob,
              css_plage)

    # Les classes personnalisees valent aussi pour les widgets : c'est par
    # elles que passent le H1 et les cartes hexagonales.
    sup = el["settings"].get("_css_classes")

    if not conteneur:
        return rendre_widget(el, cl + (" " + sup if sup else ""))

    cl = cl + " e-con"
    if sup:
        cl = cl + " " + sup
    dedans = "".join(rendre(e, css, css_tab, css_mob, css_plage) for e in el["elements"])
    if el["settings"].get("content_width") == "boxed":
        largeur = px(el["settings"].get("boxed_width")) or "1140px"
        aligne = el["settings"].get("flex_align_items") or "stretch"
        interne = ("<div class='boxed e-con-inner' style=\"max-width:%s;align-items:%s;"
                   "gap:%s\">%s</div>"
                   % (largeur, aligne,
                      px(el["settings"].get("flex_gap")) or "0px", dedans))
        return "<div class='%s'>%s</div>" % (cl, interne)
    return "<div class='%s'>%s</div>" % (cl, dedans)


BASE = """
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Plus Jakarta Sans',system-ui,sans-serif;background:#fff;}
.e-con{position:relative;}
img{max-width:100%;}
.boxed{width:100%;margin:0 auto;display:flex;flex-direction:column;}
.w-text p{margin:0 0 .6em;}
.w-text p:last-child{margin:0;}
.w-text a{color:inherit;}
.btn{display:inline-flex;align-items:center;justify-content:center;
  white-space:nowrap;}
.w-list{list-style:none;display:flex;flex-direction:column;}
.w-list.w-list-inline{flex-direction:row;flex-wrap:wrap;
  justify-content:center;align-items:center;}
.w-list li{display:flex;gap:10px;align-items:flex-start;}
.w-list a{text-decoration:none;color:inherit;}
.w-list .ico{color:#2FA36B;font-weight:800;}
.w-img,.w-map{display:grid;place-items:center;background:#EDEFEC;
  color:#8A938C;font-size:13px;min-height:200px;border-radius:12px;}
"""


def polices_utilisees(el, vues):
    """Releve les familles declarees, pour ne demander que celles-la."""
    for cle, val in el["settings"].items():
        if cle.endswith("font_family") and isinstance(val, str) and val:
            vues.add(val)
    for e in el.get("elements", []):
        polices_utilisees(e, vues)
    return vues


def construire(chemin_json):
    doc = json.load(open(chemin_json, encoding="utf-8"))
    css, css_tab, css_mob, css_plage = [], [], [], []
    corps = "".join(rendre(s, css, css_tab, css_mob, css_plage)
                    for s in doc["content"])

    feuille = BASE + "".join(css)
    feuille += "@media(max-width:%dpx){%s}" % (TABLETTE, "".join(css_tab))
    feuille += "@media(max-width:%dpx){%s}" % (MOBILE, "".join(css_mob))
    # Masquage limite a la plage tablette, comme elementor-hidden-tablet.
    feuille += "@media(min-width:%dpx) and (max-width:%dpx){%s}" % (
        MOBILE + 1, TABLETTE, "".join(css_plage))

    familles = set()
    for sec in doc["content"]:
        polices_utilisees(sec, familles)
    lien = ""
    if familles:
        params = "&".join(
            "family=%s:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400"
            % f.replace(" ", "+") for f in sorted(familles))
        lien = ("<link rel='preconnect' href='https://fonts.gstatic.com' "
                "crossorigin><link rel='stylesheet' "
                "href='https://fonts.googleapis.com/css2?%s&display=swap'>"
                % params)

    return ("<!DOCTYPE html><html lang='fr'><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width,initial-scale=1'>"
            "<title>%s</title>%s"
            "<style>%s</style></head><body><div class='elementor'>%s</div></body></html>"
            % (doc.get("title", "Aperçu"), lien, feuille, corps))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    entree = sys.argv[1]
    sortie = sys.argv[2] if len(sys.argv) > 2 else \
        os.path.splitext(entree)[0] + ".apercu.html"
    _cls[0] = 0
    html = construire(entree)
    with open(sortie, "w", encoding="utf-8") as f:
        f.write(html)
    print("%s -> %s (%.0f Ko)" % (entree, sortie, len(html) / 1024))
