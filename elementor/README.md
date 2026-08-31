# Le Rucher d'Elsa — version Elementor

Le site actuel converti en conteneurs Elementor natifs. Même design — fond
noir, miel doré, titres en Fraunces — et même structure : une seule page avec
ancres vers *Le miel*, *Notre histoire*, *Pollinisation* et *Contact*.

Chaque titre, texte, bouton et lien s'édite au clic dans le panneau. Aucun
widget HTML, aucun CSS personnalisé, aucun widget Pro : le template
s'importe sur une installation Elementor gratuite.

| Fichier | Rôle |
| --- | --- |
| `rucher-accueil.json` | La page entière, 72 Ko — le fichier à importer |
| `sections/` | Les 7 sections séparées, 5 à 16 Ko, si l'import complet cale |
| `build_rucher.py` | Régénère le tout — palette en tête de fichier |
| `verifier.py` | Contrôle le JSON avant import |
| `apercu_elementor.py` | Rejoue le rendu en HTML, pour voir sans WordPress |

## Importer

**WP Admin → Modèles → Modèles enregistrés → Importer des modèles**, puis
appliquer le modèle à une page. Pas depuis l'icône dossier de l'éditeur :
elle échoue sur Elementor 4.x.

Vérifiez d'abord deux réglages :

- *Elementor → Réglages → Fonctionnalités* → **Conteneur** doit être **actif**.
- *Elementor → Réglages → Éditeur Atomic* → doit être **désactivé**. L'éditeur
  atomique utilise ses propres éléments et ne présente pas les conteneurs V3
  comme modifiables.

## Les photos

Les six emplacements sont des conteneurs à fond dégradé sombre. Pour poser une
photo : sélectionner le conteneur → *Style → Arrière-plan* → passer de
*Dégradé* à *Classique* → choisir l'image. Le site actuel superposait un
dégradé noir sur chaque photo ; pour le reproduire, ajoutez une *Superposition
d'arrière-plan* noire à environ 60 % d'opacité.

Les fichiers d'origine sont à la racine du dépôt : `abeille1.jpg` à
`abeille3.jpg`, `miel-fleurs.png`, `miel-garrigue.png`, `miel-lavande.png`.

## Ce qui n'a pas pu être repris à l'identique

Trois effets du site actuel reposent sur du CSS ou du JavaScript qu'Elementor
gratuit ne sait pas produire sans widget de code.

**Les cartes hexagonales.** Le `clip-path` qui découpe les trois cartes de
miel en hexagones n'a pas d'équivalent dans le panneau. Les cartes sont des
rectangles à coins légèrement arrondis, avec le même fond et la même bordure.

**La lampe torche.** Le halo doré qui suit la souris, la trame hexagonale de
fond et la vignette sont trois calques animés en JavaScript. Absents de la
page principale, mais récupérables : voir `effet-torche/`. La trame et la
vignette se refont entièrement dans le panneau, sans code ; seul le suivi du
pointeur demande quatre lignes de JavaScript, isolées dans un widget dédié.

**L'en-tête fixe.** Le *sticky* est une fonction Elementor Pro. La barre reste
en haut de page au lieu de suivre le défilement.

Les apparitions au défilement, elles, sont conservées : elles passent par
l'animation d'entrée d'Elementor, disponible en version gratuite.

## Vérifier avant d'importer

```bash
python3 verifier.py rucher-accueil.json
python3 apercu_elementor.py rucher-accueil.json apercu.html
```

Le vérificateur attrape ce qui casse une page sans se voir dans le JSON :
identifiants en double, tailles non numériques qu'Elementor ignore en
silence, widgets Pro, largeurs manquantes en tablette ou mobile, et les
rangées dont les colonnes plus les gouttières dépassent la largeur utile —
celles-ci se replient, et la dernière colonne part seule sur une ligne.

L'aperçu rejoue les règles de mise en page d'Elementor en HTML. C'est une
approximation, pas Elementor : elle sert à repérer un débordement ou une
colonne qui ne s'empile pas, pas à juger un rendu au pixel près.

Les deux ont servi ici : le pied de page à trois colonnes dépassait de 3,5 %
une fois les gouttières comptées, et le titre du hero débordait sur la photo
au lieu de passer à la ligne.

## Régénérer

La palette et les polices sont en tête de `build_rucher.py`, une valeur par
ligne, reprises du `:root` de `index.html`.

```bash
python3 build_rucher.py
python3 verifier.py rucher-accueil.json
```
