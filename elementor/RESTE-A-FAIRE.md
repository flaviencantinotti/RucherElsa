# Reste à faire

État au 31 août 2026. Branche `elementor-template`, commit `aa9ed9e`.

## À faire dans WordPress

**1. Vérifier deux réglages Elementor avant d'importer.**
- *Réglages → Fonctionnalités* → **Conteneur** doit être **actif**.
- *Réglages → Éditeur Atomic* → doit être **désactivé**. C'était la cause du
  « les conteneurs ne contiennent que du HTML » : l'éditeur atomique utilise
  ses propres éléments et ne présente pas les conteneurs V3 comme modifiables.

**2. Réimporter le template avec les photos.**
- *Modèles → Modèles enregistrés* : supprimer les anciens imports du rucher,
  y compris les huit entrées de type *Conteneur* (`01-navigation` à
  `08-effets`) qui font doublon avec la page complète.
- Importer `rucher-accueil.json` — la ligne de type **Page**.
- Ouvrir la page, supprimer son contenu, puis icône dossier → *Mes modèles*.

**3. Deux réglages que le fichier ne pose pas.**
- *Réglages de la page → Mise en page* → **Elementor Canvas**. Le template
  fournit sa propre navigation et son propre pied de page ; sans ce réglage,
  ceux du thème s'ajouteraient par-dessus.
- Supprimer la section **« Gabarits — à supprimer avant mise en ligne »**
  (7ᵉ conteneur) une fois le modèle appliqué.

## À faire sur GitHub

**4. Supprimer l'ancienne branche.** `claude/wordpress-custom-template-fuks6v`
existe encore dans RucherElsa. Le proxy réseau de la session refuse la
suppression de branche distante, et l'API GitHub disponible n'expose pas
l'outil. C'est un clic : onglet *Branches* → corbeille. Tant qu'elle existe,
son nom et ses messages de commit restent visibles.

**5. Optionnel — TemplateTest.** Le nettoyage des messages de commit du dépôt
AnnaGreen a été fait en local mais le `push --force` a été refusé par le
garde-fou de sécurité. La réécriture locale est perdue avec le conteneur ;
elle se refait en une commande. Contenu des fichiers strictement identique,
seuls les messages changent.

## Avant la mise en ligne

**6. Passer les images en médiathèque.** Elles sont servies depuis l'URL
publique du dépôt, ce qui convient à un aperçu mais pas à un site en
production : pas de cache maîtrisé, pas de tailles dérivées, et tout casse si
le dépôt passe en privé. Envoyer les six fichiers de `elementor/images/` puis
régénérer :

```bash
python3 build_rucher.py https://votre-site.fr/wp-content/uploads/2026/08/
```

**7. Compléter le contact.** Le téléphone `06 00 00 00 00` du pied de page est
une valeur d'exemple héritée de `index.html`. L'adresse et le courriel sont
réels.

**8. Mentions légales et confidentialité.** Les deux liens du pied de page
pointent vers `#`. Ces pages sont obligatoires, et d'autant plus si le miel
est vendu en ligne un jour.

## Écarts connus, assumés

- **Les polices** n'ont pas pu être vérifiées visuellement : le proxy de la
  session bloque Google Fonts. Les noms sont corrects dans le template
  (Fraunces, Manrope), Elementor les chargera normalement.
- **L'aperçu** (`apercu_elementor.py`) approxime Elementor, il ne le remplace
  pas. Il attrape les fautes de structure, pas un décalage au pixel près.
- **Le bloc d'effets** (8ᵉ conteneur) est le seul widget HTML de la page. Il
  porte le découpage hexagonal, l'en-tête collant et la lampe torche. Le
  supprimer fait perdre ces trois effets, rien d'autre.

## Si l'import échoue de nouveau

Voir `DEPANNAGE.md`. Par ordre de fréquence : import lancé depuis l'éditeur au
lieu de l'admin, erreur 500 côté serveur (activer `WP_DEBUG_LOG` et lire
`wp-content/debug.log`), fichier `.json` refusé à l'upload. Le dossier
`sections/` permet d'importer section par section, de 5 à 16 Ko chacune.
