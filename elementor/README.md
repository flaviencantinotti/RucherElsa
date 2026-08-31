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

## Le bloc d'effets

Trois choses du site actuel n'ont pas d'équivalent dans le panneau Elementor :
le découpage hexagonal des cartes de miel, l'en-tête qui suit le défilement,
et la lampe torche — trame hexagonale, halo qui suit la souris, vignette.

Elles sont toutes restituées, rassemblées dans **un unique widget HTML** placé
en dernier conteneur de la page, sous l'identifiant `effets-rucher`.

C'est un choix assumé, et d'une autre nature que du HTML dans les conteneurs
de contenu : ce bloc n'affiche aucun texte, ne se rouvre jamais, et c'est
exactement ce que fait n'importe quel intégrateur pour un effet global. Les
conteneurs de contenu, eux, restent en widgets natifs de bout en bout.

Le reste passe par des réglages natifs : la classe `rdl-nav` et la classe
`rdl-hexcard` sont posées depuis *Avancé → Classes CSS*, le fond translucide
de l'en-tête et son z-index depuis le panneau.

**La trame hexagonale est embarquée en data URI** dans la feuille de style :
rien à envoyer dans la médiathèque, et WordPress n'a pas à être convaincu
d'accepter les fichiers SVG.

**Deux gardes** ont été ajoutées au code d'origine. Le script ne s'exécute pas
dans l'éditeur Elementor — sans quoi trois calques en `position:fixed`
couvriraient le canevas et empêcheraient de cliquer sur les conteneurs. Et le
halo est masqué sur écran tactile, où il n'y a pas de pointeur à suivre et où
il resterait figé au centre.

**L'en-tête utilise `position:sticky`** plutôt que le `position:fixed` du site
d'origine. Sticky garde l'élément dans le flux : aucun décalage à compenser en
haut de page, et cela évite la fonction *Sticky* d'Elementor, réservée à Pro.

Si vous préférez une page sans une seule ligne de code, supprimez ce dernier
conteneur : vous perdez les trois effets, tout le reste tient debout.

Les apparitions au défilement, elles, sont natives : elles passent par
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
