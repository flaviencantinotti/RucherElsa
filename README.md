# Le Rucher d'Elsa

Page unique pour un rucher artisanal : l'histoire du lieu, trois miels de
terroir, une offre de pollinisation et les points de vente.

**Client fictif.** Ce projet est un exercice réalisé pendant ma formation
Développement web et web mobile (Formagraph Design, Besançon — 2026). Ni le
rucher ni Elsa n'existent : le cahier des charges est inventé, les textes aussi.
Ce qui est réel, c'est le code.

---

## Le contexte technique

La page est écrite pour être collée dans un **widget HTML d'Elementor**, sous
WordPress. C'est ce qui explique deux partis pris inhabituels dans le CSS :

- **Tout est préfixé par `.rdl-scope`**, pour qu'aucune règle ne déborde sur le
  thème WordPress qui accueille la page. Sans ce préfixe, un sélecteur comme
  `h2` repeindrait tous les titres du site hôte.
- **Quelques règles neutralisent les conteneurs d'Elementor** (`.elementor`,
  `.elementor-widget-container`), qui imposent leurs propres largeurs et
  empêchent une section de s'étendre sur toute la fenêtre.

Un seul fichier, styles et scripts compris. Aucune dépendance, aucun outil de
construction.

---

## Ce qui est fait à la main

- **Effet torche** : un halo doré suit le curseur et éclaire un champ
  d'hexagones en arrière-plan, avec une vignette qui assombrit les bords. Les
  coordonnées de la souris passent par deux variables CSS (`--mx`, `--my`), ce
  qui évite de recalculer des styles en JavaScript à chaque déplacement.
- **Révélations au défilement** via `IntersectionObserver`
- **Menu burger** en dessous de 900 px
- **Défilement doux** vers les ancres, avec compensation de la barre fixe
  (`scroll-margin-top`)

---

## Structure de la page

| Section | Contenu |
|---|---|
| Hero | Accroche et navigation fixe |
| Histoire | « Un rucher, une saison » |
| Miels | Trois terroirs : toutes fleurs, garrigue, lavande |
| Pollinisation | Location de ruches pour les vergers |
| Contact | Marchés et points de vente |

---

## Stack

HTML, CSS et JavaScript, sans bibliothèque. Polices Fraunces et Manrope via
Google Fonts. Le rendu est adapté aux écrans à 1024, 900 et 600 px.

---

## Utilisation

Ouvrir `index.html` dans un navigateur — il n'y a rien à installer.

Pour l'intégrer à WordPress : copier le contenu de `<body>` dans un widget HTML
d'Elementor, et téléverser les six images dans la médiathèque en corrigeant les
chemins.

---

## Limites connues

- **Les images pèsent 9,8 Mo à elles seules**, contre 20 Ko pour le HTML. Les
  trois pots de miel sont des PNG de plus de 2 Mo chacun, alors que ce sont des
  photos : du JPEG ou du WebP les ramènerait sous les 200 Ko sans perte visible.
  C'est le premier chantier si la page devait être mise en ligne.
- La section contact affiche les points de vente mais ne comporte pas de
  formulaire.
- Les chemins d'images sont relatifs à la racine, à adapter lors d'une
  intégration WordPress.

---

## Auteur

**Flavien Cantinotti** — développeur web
[GitHub](https://github.com/flaviencantinotti-ship-it) ·
[LinkedIn](https://www.linkedin.com/in/flavien-cantinotti/)
