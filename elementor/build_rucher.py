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
ROUILLE = "#7A4B23"     # numeros de carte
TRAIT = "rgba(245,239,225,0.10)"
TRAIT_MIEL = "rgba(220,159,46,0.25)"

SERIF = "Fraunces"      # titres
SANS = "Manrope"        # textes

LARGEUR = 1180
UTILE = 1132.0

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


def titre_mixte(debut, accent, px=60, tab=44, mob=33, align="left",
                niveau="h1"):
    """Titre en deux morceaux : romain puis italique doré.

    Deux widgets Titre plutot qu'une balise inline : chaque moitie reste
    editable au clic, et Elementor charge reellement les deux graisses.
    """
    # Pas de _flex_size "none" ici : les deux moities doivent pouvoir
    # retrecir, sinon un titre plus large que sa colonne deborde sur le
    # voisin au lieu de passer a la ligne.
    r = rangee([
        conteneur([titre(debut, niveau=niveau, px=px, tab=tab, mob=mob,
                         align=align, inter=1.06)],
                  content_width="full", padding=uni(0)),
        conteneur([titre(accent, niveau="div", px=px, tab=tab, mob=mob,
                         couleur=MIEL, align=align, italique="italic",
                         inter=1.06)],
                  content_width="full", padding=uni(0)),
    ], g=14, retour="wrap", align="baseline")
    r["settings"]["flex_justify_content"] = (
        "center" if align == "center" else "flex-start")
    return r


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


def image_fond(fichier, ratio=340, rayon=6, bordure=TRAIT_MIEL, libelle=""):
    """Emplacement photo : fond en degre sombre, image a poser ensuite.

    Le site actuel superpose un degrade noir sur la photo ; on reproduit
    le degrade, l'image se choisit dans le panneau Arriere-plan.
    """
    enfants = []
    if libelle:
        enfants.append(w("heading", title=libelle, header_size="div",
                         align="center", title_color="rgba(245,239,225,0.42)",
                         typography_typography="custom",
                         typography_font_family=SANS,
                         typography_font_size=t(13)))
    return conteneur(enfants, content_width="full", width=t(100, "%"),
                     min_height=t(ratio),
                     flex_justify_content="center",
                     flex_align_items="center",
                     background_background="gradient",
                     background_color=NOIR2,
                     background_color_b="#241c10",
                     background_gradient_type="linear",
                     background_gradient_angle=t(160, "deg"),
                     border_border="solid", border_width=uni(1),
                     border_color=bordure, border_radius=uni(rayon),
                     padding=uni(20))


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


def col_auto(enfants, g=10, **extra):
    r = {"content_width": "full", "flex_direction": "column",
         "flex_gap": gap(g), "padding": uni(0), "_flex_size": "none"}
    r.update(extra)
    return conteneur(enfants, **r)


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
    return section([
        rangee([
            colonne([lien_titre("Le Rucher d'Elsa", "#hero")],
                    pct=30, tab=100, flex_align_items_tablet="center"),
            colonne([liste_liens(MENU, inline=True)], pct=44, tab=100),
            colonne([bouton_fantome("Nous écrire", "#contact", align="right")],
                    pct=22, tab=100,
                    flex_align_items_tablet="center"),
        ], g=18, align="center"),
    ], haut=22, bas=22, g=0,
        # Fond translucide et z-index sont natifs ; seuls le collage au
        # defilement et le flou passent par la feuille de style du bloc
        # d'effets, faute d'equivalent en Elementor gratuit.
        _css_classes="rdl-nav", z_index=50,
        background_color="rgba(10,9,8,0.72)",
        border_border="solid", border_width=esp(0, 0, 1, 0),
        border_color=TRAIT)


def hero():
    gauche = colonne([
        surtitre("bienvenue"),
        titre_mixte("Le Rucher d'Elsa", "Apicultrice et passionnée."),
        para("Vingt colonies conduites en transhumance entre garrigue et "
             "lavande. Récolte à la main, extraction à froid sous 40 °C, "
             "sans mélange de miellées.", px=17),
        espace(8),
        rangee([
            col_auto([bouton("Découvrir le miel", "#miel")]),
            col_auto([bouton_fantome("Notre histoire", "#histoire")]),
        ], g=14),
    ], pct=54, tab=100, g=20)
    droite = colonne([image_fond("abeille1.jpg", 460,
                                 libelle="Photo — Elsa au rucher")],
                     pct=40, tab=100)
    return section([rangee([gauche, droite], g=52, align="center")],
                   haut=96, bas=110, _element_id="hero")


def histoire():
    faits = rangee([
        col_auto([titre(v, niveau="div", px=30, tab=27, mob=25, couleur=MIEL,
                        inter=1.1),
                  para("<p>%s</p>" % s, px=13)], g=2)
        for v, s in [("20", "ruches en activité"), ("4", "terroirs butinés"),
                     ("12", "ans de pratique")]
    ], g=40)
    return section([rangee([
        colonne([image_fond("abeille2.jpg", 460,
                            libelle="Photo — cadre de hausse")],
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
     "8,90 € · pot de 250g", "miel-fleurs.png"),
    ("02 — Juin", "Miel de garrigue",
     "Thym, romarin et ciste des collines sèches. Ambré, corsé, à la pointe "
     "résineuse typique de la garrigue.",
     "9,90 € · pot de 250g", "miel-garrigue.png"),
    ("03 — Juillet", "Miel de lavande",
     "Butiné sur les plateaux de Haute-Provence entre fin juin et début "
     "août. Texture fine, parfum floral persistant.",
     "9,50 € · pot de 250g", "miel-lavande.png"),
]


def miel():
    cartes = []
    for num, nom, desc, prix, photo in MIELS:
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
        c["settings"].update({
            "_css_classes": "rdl-hexcard",
            "background_background": "gradient",
            "background_color": NOIR2,
            "background_color_b": "#1d1710",
            "background_gradient_type": "linear",
            "background_gradient_angle": t(165, "deg"),
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
        colonne([image_fond("abeille3.jpg", 440,
                            libelle="Photo — verger en pollinisation")],
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
        rangee([col_auto([bouton("Nous écrire",
                                 "mailto:contact@rucherdelsa.fr")])],
               g=0, justif="center"),
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
                     ("14 chemin des Lavandières, 84220 Gordes", "#")],
                    px=14, ecart=8, couleur=CREME_DOUX),
    ], pct=26, tab=46, g=14)

    bas = rangee([
        colonne([para("<p>© 2026 Le Rucher d'Elsa</p>", px=12.5)], pct=46),
        colonne([liste_liens([("Mentions légales", "#"),
                              ("Politique de confidentialité", "#")],
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
            titre("Conteneurs vierges à dupliquer.", px=30, tab=26, mob=23),
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
    "<g fill='none' stroke='rgba(220,159,46,0.35)' stroke-width='1'>"
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

/* Les trois calques de la lampe torche. */
#rdl-hexfield,#rdl-vignette,#rdl-glow{position:fixed;inset:0;
  pointer-events:none;}
#rdl-hexfield{z-index:1;opacity:.5;background-repeat:repeat;
  background-size:52px 90px;background-image:url("%(trame)s");}
#rdl-vignette{z-index:1;background:radial-gradient(circle 460px at
  var(--rdl-x,50%%) var(--rdl-y,50%%),transparent 0%%,rgba(0,0,0,.35) 75%%);}
#rdl-glow{z-index:3;mix-blend-mode:screen;transition:opacity .4s ease;
  background:radial-gradient(circle 380px at var(--rdl-x,50%%)
  var(--rdl-y,50%%),rgba(220,159,46,.45),rgba(220,159,46,.10) 40%%,
  transparent 70%%);}
/* Sans pointeur a suivre, le halo resterait fige au centre. */
@media (hover:none){#rdl-glow,#rdl-vignette{display:none;}}
</style>
<div id="rdl-hexfield"></div>
<div id="rdl-vignette"></div>
<div id="rdl-glow"></div>
<script>
(function(){
  /* Dans l'editeur, trois calques fixes couvriraient le canevas. */
  if(document.body.classList.contains('elementor-editor-active'))return;
  if(!window.matchMedia('(hover:hover)').matches)return;
  if(window.__rdlTorche)return;
  window.__rdlTorche=1;
  document.addEventListener('mousemove',function(e){
    var r=document.documentElement.style;
    r.setProperty('--rdl-x',e.clientX+'px');
    r.setProperty('--rdl-y',e.clientY+'px');
  });
})();
</script>"""


def effets():
    return conteneur([w("html", html=EFFETS % {"miel": MIEL,
                                               "trame": trame_data_uri()})],
                     content_width="full", width=t(100, "%"),
                     padding=uni(0), _element_id="effets-rucher")


SECTIONS = [
    ("01-navigation", nav),
    ("02-hero", hero),
    ("03-histoire", histoire),
    ("04-miel", miel),
    ("05-pollinisation", pollinisation),
    ("06-pied-de-page", pied),
    ("07-gabarits", gabarits),
    ("08-effets", effets),
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
