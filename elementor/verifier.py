#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Contrôle le JSON produit avant de l'importer dans Elementor.

Vérifie ce qu'un import raté fait généralement payer : identifiants en
double, clés d'élément manquantes, valeurs de taille non numériques,
widgets réservés à Elementor Pro, couleurs mal formées.

Usage : python3 verifier.py [fichier.json]
Code de sortie 1 si une anomalie bloquante est trouvée.
"""

import json
import os
import re
import sys

# Widgets présents dans Elementor gratuit et utilisés ici.
WIDGETS_GRATUITS = {
    "heading", "text-editor", "button", "image", "divider", "spacer",
    "icon-list", "icon", "video", "social-icons", "google_maps",
    "image-box", "icon-box", "star-rating", "toggle", "accordion", "tabs",
    "alert", "counter", "progress", "testimonial", "html", "shortcode",
    "text-path", "menu-anchor", "sidebar", "read-more", "rating",
}

# Widgets qui exigent une licence Pro : leur présence casserait l'import
# sur une installation gratuite.
WIDGETS_PRO = {
    "form", "nav-menu", "posts", "portfolio", "slides", "gallery",
    "price-table", "price-list", "flip-box", "call-to-action", "media-carousel",
    "testimonial-carousel", "reviews", "table-of-contents", "lottie",
    "countdown", "share-buttons", "blockquote", "loop-grid", "loop-carousel",
    "woocommerce-products", "woocommerce-cart", "theme-site-logo",
    "theme-page-title", "theme-post-content", "search-form", "animated-headline",
}

COULEUR = re.compile(
    r"^(#[0-9A-Fa-f]{3,8}|rgba?\([\d\s,.]+\)|)$"
)

erreurs = []
avertissements = []
vus = set()
widgets_utilises = {}
profondeur_max = [0]


def signaler(msg):
    erreurs.append(msg)


def verifier_taille(cle, val, chemin):
    """Un contrôle slider attend une taille numérique ou vide."""
    if not isinstance(val, dict) or "size" not in val:
        return
    taille = val["size"]
    if taille == "" or taille is None:
        return
    if not isinstance(taille, (int, float)):
        signaler("%s : %s a une taille non numérique (%r)"
                 % (chemin, cle, taille))
    if "unit" in val and val["unit"] not in (
            "px", "%", "em", "rem", "vw", "vh", "deg", "fr", "custom", "s",
            "ms"):
        avertissements.append("%s : %s utilise l'unité inhabituelle %r"
                              % (chemin, cle, val["unit"]))


# Largeur utile au centre de la page : boxed_width moins le padding
# horizontal des sections. Sert à convertir les gouttières en pourcentage.
# La tablette est jugée au pire cas de sa plage (768 px), pas au confort
# d'un iPad en paysage : une gouttière qui passe à 1024 peut faire tomber
# la grille à une colonne par ligne à 768.
UTILE = {"bureau": 1092.0, "tablette": 720.0}
UTILE_PX = UTILE["bureau"]


def verifier_rangee(el, chemin):
    """Une rangée dont les colonnes + gouttières dépassent 100 % se replie.

    Avec flex-wrap actif, un dépassement d'un seul pixel fait basculer la
    dernière colonne sur une ligne à elle seule, en plein écran : le défaut
    est invisible dans le JSON et saute aux yeux une fois importé.
    """
    reglages = el["settings"]
    if reglages.get("flex_wrap") != "wrap":
        return

    enfants = [e for e in el["elements"] if e.get("elType") == "container"]
    if len(enfants) < 2:
        return

    for suffixe, etiquette in (("", "bureau"), ("_tablet", "tablette")):
        utile = UTILE[etiquette]
        total = 0.0
        comptees = 0
        largeurs = []
        for enfant in enfants:
            largeur = enfant["settings"].get("width" + suffixe) \
                or enfant["settings"].get("width")
            if not isinstance(largeur, dict) or largeur.get("unit") != "%":
                continue
            taille = largeur.get("size")
            if not isinstance(taille, (int, float)):
                continue
            total += taille
            largeurs.append(taille)
            comptees += 1

        if comptees < 2:
            continue

        gouttiere = reglages.get("flex_gap") or {}
        gap_px = gouttiere.get("size", 0) if gouttiere.get("unit") == "px" else 0
        if not isinstance(gap_px, (int, float)):
            gap_px = 0

        # Colonnes toutes identiques : c'est une grille de cartes, dont le
        # repli sur plusieurs lignes est l'effet recherché. Reste à vérifier
        # qu'il se produit au bon endroit : des colonnes à 48 % sont censées
        # aller par deux, mais quelques pixels de gouttière de trop les font
        # tomber à une par ligne, et la grille se déroule en pile.
        if len(set(largeurs)) == 1:
            pct = largeurs[0]
            if pct <= 0:
                continue
            gap_pct_unit = gap_px / utile * 100
            # Combien tiendraient sans gouttiere, plafonne au nombre reel
            # de colonnes : trois colonnes a 28 % tiennent sur une ligne,
            # meme si la largeur en autoriserait une quatrieme.
            voulu = min(comptees, int(100.0 / pct))
            tiennent = int((100 + gap_pct_unit) // (pct + gap_pct_unit))
            if voulu > 1 and tiennent < voulu:
                signaler(
                    "%s : %s colonnes à %s %% %s — %d par ligne attendues, "
                    "les gouttières de %s px n'en laissent que %d"
                    % (chemin, comptees, pct, etiquette, voulu,
                       gap_px, max(tiennent, 1)))
            continue

        gap_pct = (comptees - 1) * gap_px / utile * 100

        if total + gap_pct > 99.5:
            signaler(
                "%s : rangée %s à %.1f %% (%d colonnes = %.0f %% + %.1f %% de "
                "gouttières) — elle se repliera, réduire les largeurs"
                % (chemin, etiquette, total + gap_pct, comptees, total,
                   gap_pct))


def verifier_responsive(el, chemin):
    """Chaque reglage de mise en page doit exister aux trois tailles.

    Elementor fait descendre la valeur bureau sur tablette et mobile quand
    la declinaison manque. Une colonne a 23 % reste donc a 23 % sur un
    telephone — quatre cartes illisibles cote a cote — sans qu'aucune
    erreur ne soit levee. C'est le defaut responsive le plus courant, et
    il ne se voit qu'en ouvrant la page sur un vrai appareil.
    """
    reglages = el["settings"]
    est_conteneur = el["elType"] == "container"

    # Une colonne dimensionnee en % doit prevoir tablette et mobile.
    largeur = reglages.get("width")
    if est_conteneur and isinstance(largeur, dict) \
            and largeur.get("unit") == "%" \
            and isinstance(largeur.get("size"), (int, float)) \
            and largeur["size"] < 100:
        for suffixe, ecran in (("_tablet", "tablette"), ("_mobile", "mobile")):
            if "width" + suffixe not in reglages:
                signaler("%s : colonne à %s %% sans largeur %s"
                         % (chemin, largeur["size"], ecran))

    # Une rangee doit repasser en colonne sur mobile.
    if est_conteneur and reglages.get("flex_direction") == "row":
        if reglages.get("flex_direction_mobile") != "column":
            enfants = [e for e in el["elements"]
                       if e.get("elType") == "container"]
            if len(enfants) > 1:
                avertissements.append(
                    "%s : rangée de %d colonnes qui ne repasse pas en "
                    "colonne sur mobile" % (chemin, len(enfants)))

    # Un gros corps de texte doit etre reduit sur mobile.
    taille_police = reglages.get("typography_font_size")
    if isinstance(taille_police, dict) \
            and isinstance(taille_police.get("size"), (int, float)) \
            and taille_police["size"] >= 26:
        for suffixe, ecran in (("_tablet", "tablette"), ("_mobile", "mobile")):
            if "typography_font_size" + suffixe not in reglages:
                signaler("%s : texte de %s px sans taille %s"
                         % (chemin, taille_police["size"], ecran))


def verifier_element(el, chemin, profondeur):
    profondeur_max[0] = max(profondeur_max[0], profondeur)

    for cle in ("id", "elType", "settings", "elements"):
        if cle not in el:
            signaler("%s : clé « %s » manquante" % (chemin, cle))
            return

    ident = el["id"]
    if not isinstance(ident, str) or not ident:
        signaler("%s : identifiant vide ou non textuel" % chemin)
    elif ident in vus:
        signaler("%s : identifiant en double « %s »" % (chemin, ident))
    else:
        vus.add(ident)

    el_type = el["elType"]
    if el_type not in ("container", "widget", "section", "column"):
        signaler("%s : elType inconnu « %s »" % (chemin, el_type))

    if el_type == "widget":
        wt = el.get("widgetType")
        if not wt:
            signaler("%s : widget sans widgetType" % chemin)
        else:
            widgets_utilises[wt] = widgets_utilises.get(wt, 0) + 1
            if wt in WIDGETS_PRO:
                signaler("%s : « %s » exige Elementor Pro" % (chemin, wt))
            elif wt not in WIDGETS_GRATUITS:
                avertissements.append(
                    "%s : widget « %s » non répertorié, à vérifier"
                    % (chemin, wt))
        if el["elements"]:
            signaler("%s : un widget ne peut pas contenir d'enfants" % chemin)

    reglages = el["settings"]
    if not isinstance(reglages, dict):
        signaler("%s : settings n'est pas un objet" % chemin)
        return

    for cle, val in reglages.items():
        verifier_taille(cle, val, chemin)
        if isinstance(val, str) and (
                cle.endswith("_color") or cle == "color"
                or cle.endswith("color")):
            if not COULEUR.match(val):
                signaler("%s : couleur mal formée pour %s (%r)"
                         % (chemin, cle, val))

    if el_type == "container" and reglages.get("flex_direction") == "row":
        verifier_rangee(el, chemin)

    verifier_responsive(el, chemin)

    for i, enfant in enumerate(el["elements"]):
        verifier_element(enfant, "%s > %s[%d]" % (chemin, el_type, i),
                         profondeur + 1)


def main():
    ici = os.path.dirname(os.path.abspath(__file__))
    fichier = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        ici, "annagreen-accueil.json")

    with open(fichier, encoding="utf-8") as f:
        doc = json.load(f)

    for cle in ("content", "version", "title", "type"):
        if cle not in doc:
            signaler("racine : clé « %s » manquante" % cle)

    if doc.get("type") not in ("page", "section", "container", "wp-page"):
        avertissements.append("racine : type « %s » inhabituel"
                              % doc.get("type"))

    for i, el in enumerate(doc.get("content", [])):
        verifier_element(el, "content[%d]" % i, 1)

    print("Fichier    : %s (%.0f Ko)"
          % (os.path.basename(fichier), os.path.getsize(fichier) / 1024))
    print("Éléments   : %d  ·  profondeur max %d"
          % (len(vus), profondeur_max[0]))
    print("Sections   : %d" % len(doc.get("content", [])))
    print("Widgets    : %s"
          % ", ".join("%s×%d" % (w, n)
                      for w, n in sorted(widgets_utilises.items())))

    if avertissements:
        print("\nAvertissements (%d) :" % len(avertissements))
        for a in avertissements[:15]:
            print("  · %s" % a)
        if len(avertissements) > 15:
            print("  · … et %d autres" % (len(avertissements) - 15))

    if erreurs:
        print("\nERREURS (%d) :" % len(erreurs))
        for e in erreurs[:30]:
            print("  ✗ %s" % e)
        if len(erreurs) > 30:
            print("  ✗ … et %d autres" % (len(erreurs) - 30))
        return 1

    print("\n✓ Structure valide, aucun widget Pro, prêt à importer.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
