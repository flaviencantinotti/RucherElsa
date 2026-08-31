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

Les six photos du site sont déjà en place : les trois abeilles dans le hero,
l'histoire et la pollinisation, les trois pots dans les cartes de miel — sous
le voile sombre du site d'origine, pour que le doré garde son contraste.

Elles sont servies depuis `elementor/images/`, via l'URL publique du dépôt.
Le template s'affiche donc correctement dès l'import, sans rien envoyer dans
la médiathèque.

**Elles ont été optimisées** : 9,8 Mo à l'origine, 1,3 Mo maintenant, soit
87 % de moins. Les PNG de miel pesaient 2,3 Mo chacun pour un affichage à
350 px de large ; ils sont passés en JPEG à 1400 px. À 9,8 Mo, la page aurait
mis plusieurs secondes à s'afficher sur mobile.

### Pour la mise en ligne

Servir les images depuis GitHub convient à un aperçu, pas à un site en
production : pas de cache maîtrisé, pas de tailles dérivées, et tout casse si
le dépôt passe en privé.

Envoyez les six fichiers de `elementor/images/` dans la médiathèque
WordPress, puis régénérez le template avec l'adresse de votre dossier
d'envois :

```bash
python3 build_rucher.py https://votre-site.fr/wp-content/uploads/2026/08/
```

Sans passer par le script, chaque conteneur se modifie au panneau :
*Style → Arrière-plan → Image*.

## Les gabarits vierges

Ils ne sont plus dans la page livrée : c'était un échafaudage qu'il fallait
penser à supprimer après l'import, ce qui s'oublie vite.

Ils restent disponibles dans `sections/gabarits.json` — quatre rangées vides
en une, deux, trois et quatre colonnes, largeurs et responsive déjà réglés.
À importer et insérer si vous voulez composer de nouvelles sections à la
souris, puis à retirer avant publication.

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

## SEO et accessibilité

Ce que le template porte déjà :

- **Un seul H1**, puis 4 H2 et 3 H3 — hiérarchie propre, sans niveau sauté.
- **Trois vraies balises `<img>`** avec texte alternatif pour le hero,
  l'histoire et la pollinisation. Une image d'arrière-plan n'a pas d'alt,
  n'apparaît pas dans Google Images et reste muette pour un lecteur d'écran.
  Seules les cartes de miel gardent une image de fond — comme dans le site
  d'origine, où elles en étaient déjà une.
- **Des données structurées `LocalBusiness`** en JSON-LD, dans le bloc
  d'effets : nom, description, adresse complète, courriel, fourchette de prix,
  et les trois miels en `Offer`. C'est ce qui permet à Google d'afficher
  l'atelier sur une recherche « miel Gordes » ou « apiculteur Vaucluse ».
- **Contrastes conformes WCAG AA** : le crème est à 17,4:1 sur le noir, le
  doré à 8,6:1. Les numéros de carte ont été éclaircis de `#7A4B23` à
  `#B87A3D` — la valeur d'origine tombait à 2,6:1, sous le seuil de 4,5:1.
- **Aucun lien mort** : 18 liens, toutes les ancres résolues.

### Textes alternatifs

Ceux du site d'origine décrivaient autre chose que les photos —
« Verger en pollinisation » sur un rayon de miel, « Elsa au rucher » sur une
abeille seule. Un alt qui ment est pire qu'un alt absent pour qui navigue au
lecteur d'écran. Ils ont été réécrits d'après les images réelles.

Ils sont posés dans le template, mais **Elementor lit l'alt depuis la
médiathèque** une fois l'image envoyée. Après le passage en médiathèque,
recopiez-les dans le champ *Texte alternatif* de chaque fichier.

### À régler dans WordPress

Le titre et la méta-description ne sont pas dans le template — ils se règlent
au niveau de la page, via Yoast, Rank Math ou l'onglet *Réglages de la page*.
Propositions :

| | |
| --- | --- |
| Titre | Le Rucher d'Elsa — miel artisanal de Provence, Gordes (84) |
| Description | Miels de printemps, garrigue et lavande, récoltés à la main et extraits à froid à Gordes. Vente au magasin et pollinisation de vergers. |

Le H1 dit **« Le Rucher d'Elsa, apicultrice à Gordes »** — métier et commune
dans la balise, ce qui compte pour le référencement local.

Il tient en **un seul widget Titre**, sa seconde moitié en `<em>` doré
italique. C'est exactement le procédé de `index.html`, dont le CSS ciblait
`.hero h1 em`. Le couper en deux widgets aurait laissé la moitié de la phrase
hors de la balise `<h1>` — le nom sans le métier ni le lieu. Le texte reste
modifiable au clic, l'éditeur de titre acceptant l'italique depuis sa barre
d'outils.

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
