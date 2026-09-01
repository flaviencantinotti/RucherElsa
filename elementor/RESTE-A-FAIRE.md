# Reste à faire

Ce qui n'est pas dans le dépôt et qui se règle dans WordPress, plus les
limites connues du template.

## À faire dans WordPress

**1. Vérifier deux réglages Elementor avant d'importer.**
- *Réglages → Fonctionnalités* → **Conteneur** doit être **actif**.
- *Réglages → Éditeur Atomic* → doit être **désactivé**. L'éditeur atomique
  utilise ses propres éléments : il affiche le contenu des conteneurs V3
  comme un bloc de code au lieu de widgets modifiables.

**2. Importer le template.**
- *Modèles → Modèles enregistrés* : supprimer d'éventuels imports
  antérieurs, y compris les entrées de type *Conteneur* (`01-effets` à
  `07-pied-de-page`) qui font doublon avec la page complète.
- Importer `rucher-accueil.json` — la ligne de type **Page**.
- Ouvrir la page, supprimer son contenu, puis icône dossier → *Mes modèles*.

**3. Le seul réglage que le fichier ne pose pas.**
*Réglages de la page → Mise en page* → **Elementor Canvas**. Le template
fournit sa propre navigation et son propre pied de page ; sans ce réglage,
ceux du thème s'ajouteraient par-dessus.

## Avant une mise en production

**4. Passer les images en médiathèque.** Elles sont servies depuis l'URL
publique du dépôt, ce qui convient à une démonstration mais pas à un site en
production : pas de cache maîtrisé, pas de tailles dérivées, et tout casse si
le dépôt passe en privé. Envoyer les six fichiers de `elementor/images/` puis
régénérer :

```bash
python3 build_rucher.py https://votre-site.fr/wp-content/uploads/2026/08/
```

**5. Contact et pages légales — sans objet ici.** Le Rucher d'Elsa est un
projet de démonstration. Le téléphone `06 00 00 00 00` du pied de page est
une valeur d'exemple, et les liens *Mentions légales* et *Politique de
confidentialité* pointent vers `#`.

Pour une exploitation réelle, ces trois points redeviendraient obligatoires,
la page de confidentialité d'autant plus si du miel s'y vendait en ligne.

## Écarts connus, assumés

- **Les polices** n'ont pas été vérifiées à l'écran : Google Fonts n'était
  pas joignable depuis l'environnement de développement. Les noms sont
  corrects dans le template (Fraunces, Manrope), Elementor les chargera
  normalement.
- **L'aperçu** (`apercu_elementor.py`) rejoue les règles de mise en page
  d'Elementor, il ne le remplace pas. Il attrape les fautes de structure —
  débordement, colonne qui ne s'empile pas — pas un décalage au pixel près.
- **Le bloc d'effets** (1ᵉʳ conteneur) est le seul widget HTML de la page. Il
  porte le découpage hexagonal des cartes, l'en-tête collant et la lampe
  torche. Le supprimer fait perdre ces trois effets, rien d'autre.

## Si l'import échoue

Par ordre de fréquence : import lancé depuis l'icône dossier de l'éditeur au
lieu de l'admin, erreur 500 côté serveur (activer `WP_DEBUG_LOG` et lire
`wp-content/debug.log`), fichier `.json` refusé à l'upload par la
configuration du site.

En dernier recours, le dossier `sections/` permet d'importer la page section
par section — de 6 à 14 Ko chacune, là où la page entière fait 65 Ko.
