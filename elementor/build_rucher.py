#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convertit le site du Rucher d'Elsa en conteneurs Elementor.

Reprend fidelement le design du index.html existant — fond noir, miel dore,
titres en Fraunces — en une page unique avec ancres, comme aujourd'hui.

Format conteneurs V3, widgets natifs uniquement, aucun widget Pro, aucun
widget HTML : tout est editable au clic dans le panneau Elementor.

Usage : python3 build_rucher.py
Sortie : rucher-accueil.json et sections/*.json
"""

import json
import os
import unicodedata

# --- Palette, reprise du :root de index.html ---------------------------------

NOIR = "#0A0908"        # fond principal
NOIR2 = "#121110"       # fond des cartes
MIEL = "#DC9F2E"        # dore : accents, surtitres, boutons
MIEL_CLAIR = "#F0C878"  # dore clair : survols
CREME = "#F5EFE1"       # texte principal
CREME_DOUX = "#A89F8C"  # texte secondaire
ROUILLE = "#D0925D"     # numeros de carte. Le #7A4B23 d'origine tombait
                        # a 1,2:1 sur le fond reel des cartes — une photo
                        # sous un voile trop leger, pas du noir plein.
                        # Meme teinte et meme saturation, clarte montee a
                        # 59 % : 4,6:1, au-dessus du seuil WCAG AA.
TRAIT = "rgba(245,239,225,0.10)"
TRAIT_MIEL = "rgba(220,159,46,0.25)"

SERIF = "Fraunces"      # titres
SANS = "Manrope"        # textes

LARGEUR = 1180
UTILE = 1132.0

# Base d'URL des photos. Par defaut le depot public, ce qui rend le
# template utilisable des l'import. Pour la mise en ligne, mieux vaut
# pointer la mediatheque WordPress : les images y sont servies avec les
# bons en-tetes de cache et les tailles derivees.
#   python3 build_rucher.py https://votre-site.fr/wp-content/uploads/2026/08/
BASE_IMAGES = ("https://raw.githubusercontent.com/"
               "flaviencantinotti-ship-it/RucherElsa/"
               "elementor-template/elementor/images/")


def photo(nom):
    return BASE_IMAGES + nom

_n = [0]


def cid():
    _n[0] += 1
    return "re%05d" % _n[0]


# --- Valeurs ----------------------------------------------------------------

def t(v, u="px"):
    return {"unit": u, "size": v, "sizes": []}


def esp(h, d, b, g, u="px"):
    return {"unit": u, "top": str(h), "right": str(d), "bottom": str(b),
            "left": str(g), "isLinked": False}


def uni(v, u="px"):
    return {"unit": u, "top": str(v), "right": str(v), "bottom": str(v),
            "left": str(v), "isLinked": True}


def gap(v):
    return {"unit": "px", "size": v, "column": str(v), "row": str(v),
            "isLinked": True}


def url(u):
    return {"url": u, "is_external": "", "nofollow": "",
            "custom_attributes": ""}


# --- Elements ---------------------------------------------------------------

def conteneur(enfants=None, **r):
    base = {"content_width": "boxed", "boxed_width": t(LARGEUR)}
    base.update(r)
    return {"id": cid(), "elType": "container", "settings": base,
            "elements": enfants or [], "isInner": False}


def w(type_w, **r):
    return {"id": cid(), "elType": "widget", "widgetType": type_w,
            "settings": r, "elements": []}


def titre(txt, niveau="h2", px=44, tab=34, mob=27, couleur=CREME,
          align="left", poids="500", inter=1.15, italique="",
          police=None):
    return w("heading", title=txt, header_size=niveau, align=align,
             title_color=couleur,
             typography_typography="custom",
             typography_font_family=police or SERIF,
             typography_font_size=t(px), typography_font_size_tablet=t(tab),
             typography_font_size_mobile=t(mob),
             typography_font_weight=poids,
             typography_font_style=italique,
             typography_letter_spacing=t(-0.4),
             typography_line_height=t(inter, "em"))


def titre_h1(debut, accent, px=60, tab=44, mob=33):
    """Le H1 : un seul widget portant la phrase entiere.

    Le referencement lit la balise <h1> ; la couper en deux widgets
    n'y laisserait que la moitie, soit le nom sans le metier ni le lieu.
    L'italique dore de la seconde moitie passe donc par une balise <em>
    dans le champ Titre — exactement ce que faisait index.html, dont le
    CSS ciblait « .hero h1 em ». La regle vit dans le bloc d'effets.

    Le texte reste modifiable au clic : l'editeur de titre d'Elementor
    accepte l'italique depuis sa barre d'outils.
    """
    return w("heading", title="%s<br><em>%s</em>" % (debut, accent),
             header_size="h1", align="left", title_color=CREME,
             _css_classes="rdl-h1",
             typography_typography="custom",
             typography_font_family=SERIF,
             typography_font_size=t(px), typography_font_size_tablet=t(tab),
             typography_font_size_mobile=t(mob),
             typography_font_weight="500",
             typography_letter_spacing=t(-0.4),
             typography_line_height=t(1.06, "em"))


def surtitre(txt, align="left"):
    return w("heading", title=txt, header_size="div", align=align,
             title_color=MIEL,
             typography_typography="custom", typography_font_family=SANS,
             typography_font_size=t(12), typography_font_weight="600",
             typography_text_transform="uppercase",
             typography_letter_spacing=t(2.2))


def para(html, couleur=CREME_DOUX, px=16, align="left", inter=1.7):
    return w("text-editor", editor=html, text_color=couleur, align=align,
             typography_typography="custom", typography_font_family=SANS,
             typography_font_size=t(px), typography_line_height=t(inter, "em"))


def bouton(lib, u="#", fond=MIEL, encre=NOIR, fond_h=MIEL_CLAIR,
           encre_h=NOIR, align="left", bord=None):
    r = dict(
        text=lib, link=url(u), align=align,
        button_text_color=encre, background_color=fond,
        hover_color=encre_h, button_background_hover_color=fond_h,
        border_radius=uni(2),
        text_padding=esp(14, 26, 14, 26),
        typography_typography="custom", typography_font_family=SANS,
        typography_font_size=t(14), typography_font_weight="600",
        typography_letter_spacing=t(0.3),
    )
    if bord:
        r.update({"border_border": "solid", "border_width": uni(1),
                  "border_color": bord})
    return w("button", **r)


def bouton_fantome(lib, u="#", align="left"):
    """Bouton contour, comme le .btn-ghost du site actuel."""
    return bouton(lib, u, fond="rgba(0,0,0,0)", encre=CREME,
                  fond_h="rgba(0,0,0,0)", encre_h=MIEL, align=align,
                  bord="rgba(245,239,225,0.25)")


def liste_liens(entrees, inline=False, couleur=CREME, survol=MIEL,
                px=16, ecart=38, poids="500"):
    """Liste de liens en widget Liste d'icones natif.

    Chaque entree a son champ Texte et son champ Lien dans le panneau.
    L'icone est laissee vide : seul le texte s'affiche. C'est ainsi qu'on
    monte un menu a la main en Elementor gratuit, le widget Menu etant
    reserve a Pro.
    """
    return w("icon-list",
             icon_list=[{"text": lib, "link": url(u),
                         "selected_icon": {"value": "", "library": ""},
                         "_id": cid()} for lib, u in entrees],
             view="inline" if inline else "traditional",
             space_between=t(ecart),
             text_color=couleur, text_color_hover=survol,
             icon_typography_typography="custom",
             icon_typography_font_family=SANS,
             icon_typography_font_size=t(px),
             icon_typography_font_weight=poids,
             icon_typography_line_height=t(1.8, "em"))


def marque_logo():
    """Le logo : un conteneur, un widget, le losange en image de fond.

    L'empiler en deux colonnes imposait de dimensionner chaque colonne
    sur son contenu, ce qu'Elementor ne fait pas : un conteneur enfant
    sans largeur vaut 100 %. Le losange passe donc en arriere-plan, cale
    a gauche, et le titre est decale par une marge interieure.

    Le PNG plutot qu'un data URI ou un SVG : le data URI ne survit pas a
    l'assainissement des modeles importes, et un .svg servi par
    raw.githubusercontent arrive en text/plain, que le navigateur refuse
    comme image de fond.
    """
    return conteneur([lien_titre("Le Rucher d'Elsa", "#hero")],
                     content_width="full", width=t(100, "%"),
                     _css_classes="rdl-logo",
                     min_height=t(34), padding=esp(0, 0, 0, 46),
                     flex_justify_content="center",
                     background_background="classic",
                     background_image={"url": photo("hexagone.png"),
                                       "id": "", "source": "url"},
                     background_size="contain",
                     background_position="left center",
                     background_repeat="no-repeat")


def lien_titre(txt, u, px=24, tab=22, mob=20):
    """Titre cliquable : le widget Titre porte nativement un champ Lien."""
    el = titre(txt, niveau="div", px=px, tab=tab, mob=mob, inter=1.2)
    el["settings"]["link"] = url(u)
    return el


def etapes(entrees):
    """Les trois etapes de pollinisation, en Liste d'icones numerotee."""
    return w("icon-list",
             icon_list=[{"text": "<b>%s</b><br>%s" % (h, d),
                         "selected_icon": {"value": "fas fa-circle",
                                           "library": "fa-solid"},
                         "_id": cid()} for h, d in entrees],
             space_between=t(22), icon_color=MIEL, icon_size=t(7),
             text_color=CREME_DOUX,
             icon_typography_typography="custom",
             icon_typography_font_family=SANS,
             icon_typography_font_size=t(14.5),
             icon_typography_line_height=t(1.65, "em"))


def espace(px=30):
    return w("spacer", space=t(px))


def image_fond(fichier, ratio=340, rayon=6, bordure=TRAIT_MIEL, alt="",
               voile=0.25):
    """Bloc photo : un vrai widget Image, pas un fond de conteneur.

    Une image d'arriere-plan n'a pas de texte alternatif, n'apparait pas
    dans Google Images et reste muette pour un lecteur d'ecran. Le site
    d'origine utilisait bien des balises <img> pour ces trois visuels :
    on garde la meme semantique.

    Le cadrage passe par la classe rdl-photo, qui applique object-fit au
    conteneur : sans elle, trois photos de rapports differents donneraient
    trois hauteurs differentes.
    """
    # La hauteur et le recadrage sont des reglages natifs du widget
    # Image, pas du CSS : ainsi la photo remplit son cadre meme si le
    # bloc d'effets ne s'applique pas.
    return conteneur([
        w("image", image={"url": photo(fichier), "id": "", "alt": alt,
                          "source": "url"},
          image_size="full", align="center",
          width=t(100, "%"), height=t(ratio),
          **{"object-fit": "cover", "object-position": "center center"}),
    ], content_width="full", width=t(100, "%"),
        _css_classes="rdl-photo", overflow="hidden", padding=uni(0),
        border_border="solid", border_width=uni(1),
        border_color=bordure, border_radius=uni(rayon))


# --- Assemblages ------------------------------------------------------------

def section(enfants, fond=NOIR, haut=110, bas=110, centre=False, g=26,
            **extra):
    r = {
        "padding": esp(haut, 24, bas, 24),
        "padding_mobile": esp(int(haut * .62), 18, int(bas * .62), 18),
        "flex_direction": "column",
        "flex_gap": gap(g),
    }
    if centre:
        r["flex_align_items"] = "center"
    if fond:
        r["background_background"] = "classic"
        r["background_color"] = fond
    r.update(extra)
    return conteneur(enfants, **r)


def rangee(enfants, g=26, align="stretch", justif="", retour="wrap", **extra):
    r = {
        "content_width": "full", "flex_direction": "row",
        "flex_wrap": retour, "flex_gap": gap(g),
        "flex_align_items": align, "flex_direction_mobile": "column",
        "padding": uni(0), "width": t(100, "%"),
    }
    if justif:
        r["flex_justify_content"] = justif
    r.update(extra)
    return conteneur(enfants, **r)


def colonne(enfants, pct=48, tab=None, g=16, **extra):
    r = {
        "content_width": "full", "flex_direction": "column",
        "flex_gap": gap(g), "padding": uni(0),
        "width": t(pct, "%"),
        "width_tablet": t(pct if tab is None else tab, "%"),
        "width_mobile": t(100, "%"),
    }
    r.update(extra)
    return conteneur(enfants, **r)


# col_auto a ete retire : il posait _flex_size="none", valeur qu'Elementor
# ne connait pas — ses options sont grow, shrink et custom. Sans regle
# produite, le conteneur enfant retombait sur son defaut, 100 % de large,
# et tout ce qui devait se dimensionner sur son contenu occupait la
# largeur entiere. Les widgets vont desormais directement dans la rangee.


def carte(enfants, pct=31, tab=47, interieur=30, fond=NOIR2, rayon=6,
          bordure=TRAIT, g=14, anim=True, **extra):
    r = {
        "content_width": "full", "flex_direction": "column",
        "flex_gap": gap(g), "padding": uni(interieur),
        "width": t(pct, "%"), "width_tablet": t(tab, "%"),
        "width_mobile": t(100, "%"),
        "background_background": "classic", "background_color": fond,
        "border_border": "solid", "border_width": uni(1),
        "border_color": bordure, "border_radius": uni(rayon),
    }
    if anim:
        r["animation"] = "fadeInUp"
    r.update(extra)
    return conteneur(enfants, **r)


# --- Sections du site -------------------------------------------------------

MENU = [("Le miel", "#miel"), ("Notre histoire", "#histoire"),
        ("Pollinisation", "#pollinisation"), ("Contact", "#contact")]


def nav():
    marque = marque_logo()

    # Le widget porte lui-meme sa classe et son masquage : un conteneur
    # d'enveloppe vaudrait 100 % de large et pousserait le reste.
    burger = w("button", text="☰", link=url("#"), align="right",
               _css_classes="rdl-burger",
               hide_desktop="hidden-desktop", hide_tablet="hidden-tablet",
               hide_mobile="hidden-mobile",
               button_text_color=CREME, background_color="rgba(0,0,0,0)",
               hover_color=MIEL,
               button_background_hover_color="rgba(0,0,0,0)",
               border_border="solid", border_width=uni(1),
               border_color="rgba(245,239,225,0.30)", border_radius=uni(2),
               text_padding=esp(9, 13, 9, 13),
               typography_typography="custom", typography_font_family=SANS,
               typography_font_size=t(18))

    return section([
        # flex_direction_mobile en ligne : sur telephone la marque et le
        # burger restent cote a cote, le menu se deplie sous eux.
        rangee([
            colonne([marque], pct=32, tab=32, _css_classes="rdl-marque"),
            # Le burger vient juste apres la marque : sur telephone, les
            # deux se partagent la premiere ligne et le menu se deplie
            # dessous. Place en dernier, il tombait sous le menu ouvert.
            burger,
            colonne([liste_liens(MENU, inline=True)], pct=44, tab=44,
                    _css_classes="rdl-menu"),
            colonne([bouton_fantome("Nous écrire", "#contact",
                                    align="right")],
                    pct=18, tab=18, _css_classes="rdl-cta"),
        ], g=16, align="center", retour="wrap",
            flex_direction_mobile="row", _css_classes="rdl-rangee"),
    ], haut=18, bas=18, g=0,
        # Fond translucide et z-index sont natifs ; seuls le collage au
        # defilement et le flou passent par la feuille de style du bloc
        # d'effets, faute d'equivalent en Elementor gratuit.
        _css_classes="rdl-nav", z_index=50,
        # Opaque, et non translucide : la transparence n'avait de sens
        # qu'avec le flou du bloc d'effets. Si celui-ci ne s'applique
        # pas, 72 % de noir sur un corps de page clair donnent du gris.
        background_color=NOIR,
        border_border="solid", border_width=esp(0, 0, 1, 0),
        border_color=TRAIT)


def hero():
    gauche = colonne([
        surtitre("bienvenue"),
        titre_h1("Le Rucher d'Elsa,", "apicultrice à Gordes"),
        para("Vingt colonies conduites en transhumance entre garrigue et "
             "lavande. Récolte à la main, extraction à froid sous 40 °C, "
             "sans mélange de miellées.", px=17),
        espace(8),
        # Widgets directement dans la rangee : un conteneur d'enveloppe
        # vaudrait 100 % et les boutons s'empileraient.
        rangee([bouton("Découvrir le miel", "#miel"),
                bouton_fantome("Notre histoire", "#histoire")], g=14),
    ], pct=54, tab=100, g=20)
    droite = colonne([image_fond("abeille1.jpg", 600,
                                 alt="Abeille butinant sur des épis secs")],
                     pct=40, tab=100)
    return section([rangee([gauche, droite], g=52, align="center")],
                   haut=96, bas=110, _element_id="hero")


def histoire():
    faits = rangee([
        colonne([titre(v, niveau="div", px=30, tab=27, mob=25, couleur=MIEL,
                       inter=1.1),
                 para("<p>%s</p>" % s, px=13)], pct=28, tab=28, g=2)
        for v, s in [("20", "ruches en activité"), ("4", "terroirs butinés"),
                     ("12", "ans de pratique")]
    ], g=24)
    return section([rangee([
        colonne([image_fond("abeille2.jpg", 580,
                            alt="Abeille domestique en gros plan")],
                pct=42, tab=100),
        colonne([
            surtitre("Notre histoire"),
            titre("Un rucher, une saison.", px=42, tab=34, mob=27),
            para("Depuis 2014, nous transhumons nos colonies au fil des "
                 "floraisons : toutes fleurs de printemps en avril, garrigue "
                 "en juin, lavande de fin juin à début août. Chaque hausse "
                 "est levée à la fin de la miellée, jamais avant que le "
                 "nectar ne soit operculé."),
            para("Les cadres sont désoperculés à froid, centrifugés sous "
                 "40 °C puis décantés plusieurs jours avant la mise en pot — "
                 "aucune chauffe, aucun ensemencement, pour garder intacts "
                 "les enzymes et les arômes de chaque terroir."),
            espace(6),
            faits,
        ], pct=52, tab=100, g=18, animation="fadeInUp"),
    ], g=52, align="center")], _element_id="histoire")


MIELS = [
    ("01 — Avril", "Toutes fleurs de printemps",
     "La première miellée de l'année, butinée avant la montée des chaleurs. "
     "Miel doux et clair, qui cristallise vite en pot.",
     "8,90 € · pot de 250g", "miel-fleurs.jpg"),
    ("02 — Juin", "Miel de garrigue",
     "Thym, romarin et ciste des collines sèches. Ambré, corsé, à la pointe "
     "résineuse typique de la garrigue.",
     "9,90 € · pot de 250g", "miel-garrigue.jpg"),
    ("03 — Juillet", "Miel de lavande",
     "Butiné sur les plateaux de Haute-Provence entre fin juin et début "
     "août. Texture fine, parfum floral persistant.",
     "9,50 € · pot de 250g", "miel-lavande.jpg"),
]


def miel():
    cartes = []
    for num, nom, desc, prix, photo_fichier in MIELS:
        c = carte([
            w("heading", title=num, header_size="div", align="left",
              title_color=ROUILLE,
              typography_typography="custom", typography_font_family=SANS,
              typography_font_size=t(12), typography_letter_spacing=t(1.6)),
            titre(nom, niveau="h3", px=22, tab=21, mob=20, inter=1.25),
            para("<p>%s</p>" % desc, px=14.5),
            titre(prix, niveau="div", px=18, tab=17, mob=17, couleur=MIEL,
                  inter=1.3),
        ], interieur=32)
        # Le site actuel pose la photo en fond, assombrie par un degrade.
        # On garde le fond sombre ; l'image se choisit dans le panneau.
        # Photo en fond, sous le degrade noir du site d'origine :
        # linear-gradient(rgba(10,9,8,.55), rgba(10,9,8,.9)) sur l'image.
        c["settings"].update({
            "_css_classes": "rdl-hexcard",
            "background_background": "classic",
            "background_image": {"url": photo(photo_fichier), "id": "",
                                 "source": "url"},
            "background_size": "cover",
            "background_position": "center center",
            "background_repeat": "no-repeat",
            "background_overlay_background": "gradient",
            # Voile renforce : a 0,55 en haut, la photo laissait passer
            # des zones a #5E472B sous lesquelles ni le numero ni
            # le descriptif ne tenaient 4,5:1.
            "background_overlay_color": "rgba(10,9,8,0.70)",
            "background_overlay_color_b": "rgba(10,9,8,0.92)",
            "background_overlay_gradient_type": "linear",
            "background_overlay_gradient_angle": t(180, "deg"),
        })
        cartes.append(c)
    return section([
        rangee([
            colonne([surtitre("Nos récoltes"),
                     titre("Trois terroirs, trois miels.", px=42, tab=34,
                           mob=27)], pct=52, tab=100, g=12),
            colonne([para("Récoltés séparément selon la floraison butinée, "
                          "sans mélange ni pasteurisation. Disponibles en "
                          "magasin.", px=15)], pct=34, tab=100),
        ], g=24, align="flex-end"),
        espace(14),
        rangee(cartes, g=24),
    ], haut=100, bas=100, _element_id="miel")


def pollinisation():
    return section([rangee([
        colonne([
            surtitre("Pollinisation"),
            titre("Nos ruches travaillent aussi<br>dans vos vergers.",
                  px=42, tab=34, mob=27),
            para("Mise à disposition de colonies pour la pollinisation "
                 "d'espèces à forte dépendance entomophile — amandiers, "
                 "cerisiers, pruniers — sur la base d'un contrat simple qui "
                 "fixe le calendrier de pose, le nombre de colonies par "
                 "hectare et la conduite du verger pendant la floraison."),
            etapes([
                ("Diagnostic de la parcelle",
                 "Visite avant floraison pour évaluer la surface et définir "
                 "le nombre de colonies nécessaires à l'hectare."),
                ("Installation et suivi",
                 "Colonies posées à l'entrée en floraison ; aucun traitement "
                 "insecticide ou acaricide n'est appliqué en présence des "
                 "abeilles."),
                ("Retrait en fin de floraison",
                 "Retrait dès la chute des pétales, avant la reprise des "
                 "traitements phytosanitaires du verger."),
            ]),
            espace(8),
            bouton("Demander un devis", "#contact"),
        ], pct=52, tab=100, g=18, animation="fadeInUp"),
        colonne([image_fond("abeille3.jpg", 470,
                            alt="Rayon de miel operculé dont le miel s'écoule")],
                pct=42, tab=100),
    ], g=52, align="center")], haut=120, bas=120,
        border_border="solid", border_width=esp(1, 0, 0, 0),
        border_color=TRAIT, _element_id="pollinisation")


def pied():
    appel = colonne([
        surtitre("Où nous trouver", align="center"),
        titre("Retrouvez-nous sur les marchés du coin<br>ou au magasin.",
              px=48, tab=38, mob=29, align="center", inter=1.12),
        para("Notre magasin se situe au 14 chemin des Lavandières,<br>"
             "84220 Gordes, Vaucluse — Provence-Alpes-Côte d'Azur.",
             px=16, align="center"),
        espace(6),
        rangee([bouton("Nous écrire", "mailto:contact@rucherdelsa.fr",
                       align="center")], g=0, justif="center"),
    ], pct=60, tab=90, g=16, animation="fadeInUp")

    col_a = colonne([
        titre("Le Rucher d'Elsa", niveau="div", px=22, tab=20, mob=19,
              inter=1.3),
        para("<p>Apiculture artisanale en Provence-Alpes-Côte d'Azur.</p>",
             px=14),
    ], pct=38, tab=46, g=12)
    col_b = colonne([
        surtitre("Navigation"),
        liste_liens(MENU[:3], px=14, ecart=8, couleur=CREME_DOUX),
    ], pct=24, tab=46, g=14)
    col_c = colonne([
        surtitre("Contact"),
        liste_liens([("contact@rucherdelsa.fr",
                      "mailto:contact@rucherdelsa.fr"),
                     ("06 00 00 00 00", "tel:0600000000"),
                     ("14 chemin des Lavandières, 84220 Gordes",
                      "https://www.google.com/maps/search/"
                      "?api=1&query=14+chemin+des+Lavandi%C3%A8res+84220+Gordes")],
                    px=14, ecart=8, couleur=CREME_DOUX),
    ], pct=26, tab=46, g=14)

    bas = rangee([
        colonne([para("<p>© 2026 Le Rucher d'Elsa</p>", px=12.5)], pct=46),
        # Ces deux pages restent a creer dans WordPress ; pointer leur
        # futur permalien vaut mieux qu'un « # » qui ne mene nulle part.
        colonne([liste_liens([("Mentions légales", "/mentions-legales/"),
                              ("Politique de confidentialité",
                               "/politique-de-confidentialite/")],
                             inline=True, px=12.5, ecart=16,
                             couleur=CREME_DOUX)], pct=50),
    ], g=16, align="center")

    return section([
        rangee([appel], g=0, justif="center"),
        espace(40),
        # 38+24+26 = 88 % : a 94 % les gouttieres de 52 px faisaient
        # basculer la troisieme colonne sur une ligne a elle seule.
        rangee([col_a, col_b, col_c], g=40,
               border_border="solid", border_width=esp(1, 0, 0, 0),
               border_color=TRAIT, padding=esp(50, 0, 0, 0)),
        espace(30),
        bas,
    ], haut=110, bas=44, g=8,
        border_border="solid", border_width=esp(1, 0, 0, 0),
        border_color=TRAIT, _element_id="contact")


def gabarits():
    TAB = {100: 100, 48: 48, 31: 47, 23: 47}

    def vide(pct, lib):
        return carte([para("<p>%s</p>" % lib, px=14, align="center")],
                     pct=pct, tab=TAB[pct], interieur=34,
                     fond="rgba(0,0,0,0)", anim=False)
    return section([
        colonne([
            surtitre("Gabarits — à supprimer avant mise en ligne"),
            titre("Conteneurs vierges à dupliquer.", niveau="div", px=30,
                  tab=26, mob=23),
            para("Clic droit sur un conteneur → Dupliquer, puis glissez-y vos "
                 "widgets. Largeurs et responsive sont déjà réglés.", px=15),
        ], pct=70, tab=100),
        espace(10),
        rangee([vide(100, "Pleine largeur")], g=24),
        rangee([vide(48, "Deux colonnes"), vide(48, "Deux colonnes")], g=24),
        rangee([vide(31, "Trois colonnes") for _ in range(3)], g=24),
        rangee([vide(23, "Quatre colonnes") for _ in range(4)], g=24),
    ], fond=NOIR2, haut=70, bas=70)



# --- Bloc d'effets ----------------------------------------------------------
# Tout ce qu'Elementor gratuit ne sait pas exprimer au panneau, rassemble
# en un unique widget HTML pose en fin de page : le decoupage hexagonal
# des cartes, le collage de l'en-tete au defilement, et les trois calques
# de la lampe torche. Il n'affiche aucun texte et ne se rouvre jamais.
#
# La trame hexagonale est embarquee en data URI : rien a envoyer dans la
# mediatheque, et WordPress n'a pas a etre convaincu d'accepter le SVG.

TRAME = (
    "<svg xmlns='http://www.w3.org/2000/svg' width='52' height='90'>"
    "<g fill='none' stroke='rgba(220,159,46,0.18)' stroke-width='1'>"
    "<polygon points='26,2 47,15 47,42 26,55 5,42 5,15'/>"
    "<polygon points='0,47 21,60 21,87 0,100 -21,87 -21,60'/>"
    "<polygon points='52,47 73,60 73,87 52,100 31,87 31,60'/>"
    "</g></svg>"
)


def trame_data_uri():
    from urllib.parse import quote
    return "data:image/svg+xml;utf8," + quote(TRAME, safe="")


EFFETS = """<style>
/* En-tete colle au defilement. position:sticky garde l'element dans le
   flux : aucun decalage a compenser, contrairement a position:fixed. */
.rdl-nav{position:sticky;top:0;
  -webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);}

/* Cartes de miel en hexagone, comme sur le site actuel. */
.rdl-hexcard{
  clip-path:polygon(8%% 0,92%% 0,100%% 50%%,92%% 100%%,8%% 100%%,0 50%%);
  transition:transform .4s ease,border-color .4s ease;}
.rdl-hexcard:hover{transform:translateY(-6px);border-color:%(miel)s!important;}
@media(max-width:900px){
  .rdl-hexcard{clip-path:none;border-radius:6px;}
}

/* En-tete. Le soulignement dore au survol et le menu deroulant sur
   telephone n'ont pas d'equivalent au panneau : ils reprennent les regles
   « .nav-links a::after » et « .burger » de index.html. */
.rdl-menu a{position:relative;padding-bottom:4px;text-decoration:none;}
.rdl-menu a::after{content:'';position:absolute;left:0;bottom:0;width:0;
  height:1px;background:%(miel)s;transition:width .3s ease;}
.rdl-menu a:hover::after{width:100%%;}
/* Le burger est masque nativement partout. Il ne reapparait sur
   telephone que si cette feuille s'applique, donc si le script qui
   l'anime est la aussi : un burger sans script ne ferait rien. */
@media(max-width:767px){
  .rdl-burger{display:block!important;}
}

@media(max-width:767px){
  .rdl-rangee{flex-direction:row!important;flex-wrap:wrap!important;
    align-items:center!important;}
  .rdl-marque{width:auto!important;flex:1 1 auto!important;}
  .rdl-burger{display:block!important;}
  .rdl-menu,.rdl-cta{display:none!important;width:100%%!important;}
  .rdl-nav.rdl-ouvert .rdl-menu,
  .rdl-nav.rdl-ouvert .rdl-cta{display:flex!important;}
  .rdl-nav.rdl-ouvert .rdl-menu{padding-top:18px;}
  .rdl-nav.rdl-ouvert .rdl-cta{padding-top:12px;
    justify-content:flex-start!important;}
  .rdl-cta .elementor-widget-button,
  .rdl-cta .elementor-button-wrapper,
  .rdl-cta .w-btnwrap{text-align:left!important;
    justify-content:flex-start!important;}
  .rdl-menu .elementor-icon-list-items,
  .rdl-menu ul{flex-direction:column!important;align-items:flex-start!important;
    gap:16px!important;}
}

/* Seconde moitie du H1 : italique doree, comme « .hero h1 em » dans
   index.html. Le H1 reste une seule balise, donc une seule phrase pour
   le referencement. */
.rdl-h1 em{font-style:italic;color:%(miel)s;}

/* La lampe torche. Elle tenait dans trois <div> au fond du dernier
   conteneur de la page. Un <div> en position:fixed depend de ses
   ancetres : le moindre contexte d'empilement ou bloc conteneur sur un
   conteneur Elementor le ramene a la boite de ce conteneur, donc en bas
   de page — c'est le halo qui ne s'allumait qu'au pied de page. Deux
   pseudo-elements de <body> n'ont aucun ancetre Elementor : leur bloc
   conteneur est la fenetre, ou que soit pose le bloc d'effets. */
body::before,body::after{content:'';position:fixed;inset:0;
  pointer-events:none;}
/* Trame hexagonale, vignette par-dessus : deux couches d'un meme fond.
   L'opacite de la trame est passee dans le trait du SVG. */
body::before{z-index:1;
  background-image:radial-gradient(circle 460px at var(--rdl-x,50%%)
    var(--rdl-y,50%%),transparent 0%%,rgba(0,0,0,.35) 75%%),
    url("%(trame)s");
  background-repeat:no-repeat,repeat;
  background-size:auto,52px 90px;}
body::after{z-index:3;mix-blend-mode:screen;transition:opacity .4s ease;
  background:radial-gradient(circle 380px at var(--rdl-x,50%%)
  var(--rdl-y,50%%),rgba(220,159,46,.45),rgba(220,159,46,.10) 40%%,
  transparent 70%%);}
/* Sans pointeur a suivre, le halo resterait fige au centre et la
   vignette au milieu de l'ecran. Reste la trame seule. */
@media (hover:none){
  body::after{display:none;}
  body::before{background-image:url("%(trame)s");
    background-repeat:repeat;background-size:52px 90px;}
}

/* Le contenu passe devant la trame, le fond des sections reste
   derriere : c'est le « z-index:2 » du .wrap de index.html. Les
   sections gardent z-index:auto, sans quoi elles emprisonneraient
   leur contenu sous la trame. */
.elementor>.e-con>*{position:relative;z-index:2;}
</style>
<script type="application/ld+json">
{
  "@context":"https://schema.org",
  "@type":"LocalBusiness",
  "additionalType":"https://schema.org/Farm",
  "name":"Le Rucher d'Elsa",
  "description":"Apiculture artisanale en Provence-Alpes-Cote d'Azur. Miels de printemps, garrigue et lavande, recoltes a la main et extraits a froid. Pollinisation de vergers.",
  "address":{
    "@type":"PostalAddress",
    "streetAddress":"14 chemin des Lavandieres",
    "postalCode":"84220",
    "addressLocality":"Gordes",
    "addressRegion":"Vaucluse",
    "addressCountry":"FR"
  },
  "email":"contact@rucherdelsa.fr",
  "priceRange":"8-10 EUR",
  "makesOffer":[
    {"@type":"Offer","itemOffered":{"@type":"Product","name":"Miel toutes fleurs de printemps"},"price":"8.90","priceCurrency":"EUR"},
    {"@type":"Offer","itemOffered":{"@type":"Product","name":"Miel de garrigue"},"price":"9.90","priceCurrency":"EUR"},
    {"@type":"Offer","itemOffered":{"@type":"Product","name":"Miel de lavande"},"price":"9.50","priceCurrency":"EUR"}
  ]
}
</script>
<script>
(function(){
  /* Dans l'editeur, trois calques fixes couvriraient le canevas. */
  if(document.body.classList.contains('elementor-editor-active'))return;
  if(window.__rdlTorche)return;
  window.__rdlTorche=1;
  /* L'ecoute est posee sur le conteneur, pas sur le lien : selon la
     version, Elementor rend le bouton en <a> ou en <button>. */
  var burger=document.querySelector('.rdl-burger'),
      entete=document.querySelector('.rdl-nav');
  if(burger&&entete){
    var cible=burger.querySelector('a,button')||burger;
    cible.setAttribute('aria-label','Ouvrir le menu');
    burger.addEventListener('click',function(e){
      e.preventDefault();
      entete.classList.toggle('rdl-ouvert');
    });
    /* Refermer apres avoir choisi une destination. */
    entete.querySelectorAll('.rdl-menu a').forEach(function(a){
      a.addEventListener('click',function(){
        entete.classList.remove('rdl-ouvert');
      });
    });
  }
  /* Le halo n'a de sens qu'avec un pointeur ; le burger, lui, sert
     precisement la ou il n'y en a pas. */
  if(window.matchMedia('(hover:hover)').matches){
    document.addEventListener('mousemove',function(e){
      var r=document.documentElement.style;
      r.setProperty('--rdl-x',e.clientX+'px');
      r.setProperty('--rdl-y',e.clientY+'px');
    });
  }
})();
</script>"""


def effets():
    return conteneur([w("html", html=EFFETS % {"miel": MIEL,
                                               "trame": trame_data_uri()})],
                     content_width="full", width=t(100, "%"),
                     padding=uni(0), _element_id="effets-rucher")


# Les sections de la page livree. Les gabarits vierges n'en font pas
# partie : ils servaient d'echafaudage et devaient etre supprimes a la
# main apres import, ce qui est vite oublie. Ils restent disponibles a
# part, dans sections/gabarits.json, pour qui veut les inserer.
# Le bloc d'effets vient en premier. En dernier, sa feuille de style
# n'etait analysee qu'apres 3 800 px de contenu : la trame et le halo
# n'apparaissaient qu'en fin de page, ou tres tard.
SECTIONS = [
    ("01-effets", effets),
    ("02-navigation", nav),
    ("03-hero", hero),
    ("04-histoire", histoire),
    ("05-miel", miel),
    ("06-pollinisation", pollinisation),
    ("07-pied-de-page", pied),
]

EN_OPTION = [
    ("gabarits", gabarits),
]


# --- Sortie -----------------------------------------------------------------

def nettoyer(el):
    el["settings"] = {k: v for k, v in el["settings"].items()
                      if v != "" and v is not None}
    for e in el.get("elements", []):
        nettoyer(e)
    return el


def envelopper(contenu, titre_doc, type_doc):
    return {"content": contenu, "page_settings": [], "version": "0.4",
            "title": titre_doc, "type": type_doc}


def ecrire(doc, chemin):
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
    return os.path.getsize(chemin)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        BASE_IMAGES = sys.argv[1]
        if not BASE_IMAGES.endswith("/"):
            BASE_IMAGES += "/"
        print("Base des images : %s\n" % BASE_IMAGES)
    ici = os.path.dirname(os.path.abspath(__file__))

    _n[0] = 0
    doc = envelopper([nettoyer(f()) for _, f in SECTIONS],
                     "Le Rucher d'Elsa — Accueil", "page")
    poids = ecrire(doc, os.path.join(ici, "rucher-accueil.json"))
    print("rucher-accueil.json   %6.1f Ko  (%d sections, %d éléments)"
          % (poids / 1024, len(doc["content"]), _n[0]))

    dossier = os.path.join(ici, "sections")
    if not os.path.isdir(dossier):
        os.makedirs(dossier)
    print("\nDécoupe par section")
    plus_gros = 0
    for nom, fab in SECTIONS:
        _n[0] = 0
        d = envelopper([nettoyer(fab())], "Rucher d'Elsa — %s" % nom,
                       "container")
        p = ecrire(d, os.path.join(dossier, nom + ".json"))
        plus_gros = max(plus_gros, p)
        print("  sections/%-22s %6.1f Ko" % (nom + ".json", p / 1024))
    print("  plus gros fichier : %.1f Ko" % (plus_gros / 1024))

    # Le bloc d'effets aussi en fichiers separes : WordPress assainit les
    # balises <style> et <script> des modeles importes selon le role et la
    # configuration du site. Ces deux fichiers passent par des voies qui,
    # elles, ne sont jamais filtrees.
    corps = EFFETS % {"miel": MIEL, "trame": trame_data_uri()}
    css = corps.split("<style>")[1].split("</style>")[0].strip()
    js = corps.split("<script>")[1].split("</script>")[0].strip()
    dossier_e = os.path.join(ici, "effets")
    if not os.path.isdir(dossier_e):
        os.makedirs(dossier_e)
    for nom, contenu in [("effets-rucher.css", css),
                         ("effets-rucher.js", js)]:
        with open(os.path.join(dossier_e, nom), "w", encoding="utf-8") as f:
            f.write(contenu + "\n")
    print("\nBloc d'effets, en fichiers separes")
    for nom in ("effets-rucher.css", "effets-rucher.js"):
        c = os.path.join(dossier_e, nom)
        print("  effets/%-24s %5.1f Ko" % (nom, os.path.getsize(c) / 1024))

    print("\nEn option, hors page livree")
    for nom, fab in EN_OPTION:
        _n[0] = 0
        d = envelopper([nettoyer(fab())], "Rucher d'Elsa — %s" % nom,
                       "container")
        p = ecrire(d, os.path.join(dossier, nom + ".json"))
        print("  sections/%-22s %6.1f Ko" % (nom + ".json", p / 1024))
