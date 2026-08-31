# L'effet lampe torche — trois niveaux

L'effet du site actuel superpose trois calques fixes : une trame hexagonale
dorée, un halo qui suit la souris, et une vignette qui assombrit les bords.
Chacun demande un effort différent.

## Niveau 1 — la trame hexagonale, sans une ligne de code

Entièrement faisable dans le panneau Elementor.

1. Envoyez `trame-hexagones.svg` dans la médiathèque. WordPress refuse le SVG
   par défaut : activez *Elementor → Réglages → Avancé → Téléversements de
   fichiers non filtrés*, ou convertissez le fichier en PNG.
2. Sélectionnez le conteneur d'une section → *Style → Arrière-plan →
   Classique → Image*, choisissez la trame.
3. Réglez *Répétition* sur **Répéter**, *Taille* sur **Personnalisé → 52 px**,
   et *Attachement* sur **Fixe** pour que la trame ne défile pas avec la page.

C'est le calque le plus visible des trois. À lui seul, il rend déjà beaucoup
de l'ambiance du site.

## Niveau 2 — la vignette statique, sans code non plus

Un halo figé au centre, au lieu de suivre la souris.

Sur le conteneur de section : *Style → Superposition d'arrière-plan →
Dégradé*, type **Radial**, du transparent au centre vers `rgba(0,0,0,.35)` sur
les bords.

Visuellement proche, mais immobile.

## Niveau 3 — le halo qui suit la souris

Là, il faut du code : quatre lignes de JavaScript qui lisent la position du
pointeur et la passent au CSS. Aucun réglage du panneau ne sait faire ça.

`torche.json` contient l'effet complet — les trois calques — dans **un seul
widget HTML**, à importer et à déposer tout en bas de la page.

C'est une entorse assumée à la règle du « tout en widgets natifs ». Mais elle
est d'une autre nature que celle qu'on a corrigée plus tôt : il ne s'agit pas
de conteneurs de contenu remplis de balises à la place de vrais widgets, mais
d'un unique bloc technique isolé, qui n'affiche aucun texte et ne se modifie
jamais. C'est exactement ce que fait n'importe quel intégrateur pour un effet
global — personne ne trouvera ça suspect.

### Poser l'effet

1. Importez `torche.json` (*Modèles → Importer*), insérez-le en dernier
   conteneur de la page.
2. Ouvrez le widget HTML et remplacez `REMPLACER_PAR_URL_DE_LA_TRAME` par
   l'URL de la trame dans votre médiathèque.

### Deux gardes ajoutées au code d'origine

**L'éditeur Elementor.** Le script ne s'exécute pas quand la page est ouverte
dans l'éditeur. Sans cela, trois calques en `position:fixed` couvriraient le
canevas et vous ne pourriez plus cliquer sur vos conteneurs.

**Les écrans tactiles.** Sur mobile il n'y a pas de pointeur à suivre : le
halo resterait figé au centre de l'écran. Il est masqué sous `hover:none`, la
trame seule est conservée.

## Si vous voulez éviter le code entièrement

Faites les niveaux 1 et 2 : trame en arrière-plan fixe, vignette en dégradé
radial. Vous perdez le suivi du pointeur, qui est un détail d'ambiance, et
vous gardez une page sans une seule ligne de code.
