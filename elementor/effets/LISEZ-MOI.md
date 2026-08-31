# Le bloc d'effets — voie de secours

Le template contient déjà ces effets dans un widget HTML, dernier conteneur de
la page. Mais **WordPress assainit les balises `<style>` et `<script>` des
modèles importés** selon le rôle de l'utilisateur et la configuration du site.
Quand cela arrive, le widget est bien là mais son contenu ne s'applique pas.

Le symptôme est net : le burger reste visible sur grand écran, les cartes de
miel ne sont plus hexagonales, l'en-tête ne suit plus le défilement, et il n'y
a plus de halo.

Ces trois fichiers reprennent le même contenu, par des voies qui ne sont
jamais filtrées.

## 1. Le CSS — sans plugin

`effets-rucher.css` → **Apparence → Personnaliser → CSS additionnel**.
Coller, publier. C'est du WordPress natif, aucune extension nécessaire.

Ce fichier porte le découpage hexagonal des cartes, l'en-tête collant, le
soulignement doré au survol, le cadrage des photos, le menu mobile et les trois
calques de la lampe torche.

## 2. Les calques — dans la page

`calques-torche.html` → trois `<div>` vides que le CSS habille.

Si le widget HTML du dernier conteneur fonctionne, ils y sont déjà : ne les
ajoutez pas deux fois. Sinon, collez-les dans un widget HTML placé en fin de
page.

## 3. Le JavaScript — le seul point qui demande un peu plus

`effets-rucher.js` fait deux choses : suivre le pointeur pour le halo, et
ouvrir le menu mobile au clic sur le burger.

Trois façons de le poser, de la plus simple à la plus propre :

- **Elementor → Éléments personnalisés → Code** (visible dans le menu de
  gauche de votre installation), emplacement *Body — fin*.
- Un plugin de snippets — WPCode, Code Snippets — en mode JavaScript.
- Le `functions.php` d'un thème enfant, via `wp_enqueue_script`.

### Sans JavaScript du tout

Le site reste utilisable. Vous perdez le halo qui suit la souris — un détail
d'ambiance — et le menu mobile ne se déplie plus au clic.

Pour ce dernier, une solution sans code : dans Elementor, sélectionnez le
conteneur du burger et masquez-le sur mobile aussi (*Avancé → Responsive*),
puis affichez le menu et le bouton en permanence. L'en-tête redevient une pile
de six lignes sur téléphone, comme avant — moins élégant, mais fonctionnel.

## Ce qui ne dépend de rien de tout cela

Le burger est masqué en bureau et en tablette par le réglage natif d'Elementor,
pas par ce CSS. Même sans aucun de ces fichiers, l'en-tête reste correct sur
grand écran — c'était le défaut de la version précédente.

Les photos, la mise en page, les couleurs, la typographie, le responsive et les
données structurées sont tous portés par le template lui-même.
