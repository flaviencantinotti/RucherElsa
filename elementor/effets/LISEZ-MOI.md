# Le bloc d'effets — voie de secours

Le template contient déjà ces effets dans un widget HTML, **premier conteneur
de la page**. Mais **WordPress assainit les balises `<style>` et `<script>` des
modèles importés** selon le rôle de l'utilisateur et la configuration du site.
Quand cela arrive, le widget est bien là mais son contenu ne s'applique pas.

Le symptôme est net : le burger reste visible sur grand écran, les cartes de
miel ne sont plus hexagonales, l'en-tête ne suit plus le défilement, et il n'y
a plus de halo.

Ces deux fichiers reprennent le même contenu, par des voies qui ne sont
jamais filtrées.

## 1. Le CSS — sans plugin

`effets-rucher.css` → **Apparence → Personnaliser → CSS additionnel**.
Coller, publier. C'est du WordPress natif, aucune extension nécessaire.

C'est aussi la pose la plus sûre : le CSS part alors dans le `<head>`, donc
avant le corps de la page. Dans le widget HTML il est lu au fil du document —
c'est pour cela que le bloc est passé en tête de page.

Ce fichier porte le découpage hexagonal des cartes, l'en-tête collant, le
soulignement doré au survol, le menu mobile et la lampe torche.

## 2. Le JavaScript — le seul point qui demande un peu plus

`effets-rucher.js` fait deux choses : suivre le pointeur pour le halo, et
ouvrir le menu mobile au clic sur le burger.

Trois façons de le poser, de la plus simple à la plus propre :

- **Elementor → Éléments personnalisés → Code** (visible dans le menu de
  gauche de votre installation), emplacement *Body — fin*.
- Un plugin de snippets — WPCode, Code Snippets — en mode JavaScript.
- Le `functions.php` d'un thème enfant, via `wp_enqueue_script`.

### Sans JavaScript du tout

Le site reste utilisable. Vous perdez le halo qui suit la souris — un détail
d'ambiance ; la trame hexagonale et la vignette, elles, restent. Et le menu
mobile ne se déplie plus au clic.

Pour ce dernier, une solution sans code : dans Elementor, sélectionnez le
bouton burger et masquez-le sur mobile aussi (*Avancé → Responsive*), puis
affichez le menu et le bouton en permanence. L'en-tête redevient une pile de
lignes sur téléphone — moins élégant, mais fonctionnel.

## Plus de calques à coller

Les trois `<div>` de la lampe torche ont disparu. Un élément `position:fixed`
dépend de ses ancêtres : posé au fond d'un conteneur Elementor, le moindre
contexte d'empilement le ramenait à la boîte de ce conteneur, donc en bas de
page — c'était le halo qui ne s'allumait qu'au pied de page.

La trame, la vignette et le halo sont maintenant deux pseudo-éléments de
`<body>`, portés par le CSS seul. Aucun ancêtre Elementor, donc aucun endroit
où les poser : le fichier `calques-torche.html` n'a plus de raison d'être.

## Ce qui ne dépend de rien de tout cela

Le burger est masqué en bureau et en tablette par le réglage natif d'Elementor,
pas par ce CSS. L'en-tête est opaque par réglage natif lui aussi. Même sans
aucun de ces fichiers, la page est correcte aux trois tailles.

Les photos, la mise en page, les couleurs, la typographie, le responsive et les
données structurées sont tous portés par le template lui-même.
