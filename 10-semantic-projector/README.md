# README

## Context

I would like to create a python app that projects any text on a set of semantic dimensions, this in French, like a ranking per dimension by grouping words and their occurrences in semantic dimensions.

Voici ma proposition pour cette app. Je vais construire une version complète en Python avec :

- **Analyse sémantique** : dimensions prédéfinies (émotions, valeurs, registres, etc.) avec des lexiques en français
- **Comptage d'occurrences** par dimension
- **Visualisation** : classement des mots par dimension
- **Interface Tkinter** soignée, dans ton style habituel

Laisse-moi d'abord clarifier l'approche sémantique :

Q: Comment veux-tu définir les dimensions sémantiques ?

A: Les deux : dimensions par défaut + possibilité d'en ajouter

Q: Quelle méthode de correspondance pour les mots ?

A: Les deux selon la dimension

Parfait. Je vais construire une app complète avec :

- Lexiques prédéfinis français (émotions, valeurs, registre, temporalité, etc.)
- Éditeur de dimensions personnalisées
- Correspondance exacte (lemmatisation via `spacy fr`) + similarité cosine (embeddings `sentence-transformers`)
- Interface Tkinter avec visualisation par barres et tableau de détailBonne nouvelle : `sklearn` est disponible. Voici la stratégie finale :
- **Exact** : correspondance par radical (Snowball stemmer français)
- **Similarité** : cosine TF-IDF sur le lexique de chaque dimension (pas besoin de modèle externe)
- Interface **Tkinter** complète avec matplotlib pour les graphiquesLe moteur fonctionne correctement — les radicaux capturent bien `susmentionnées → susmentionné` et `l'angoisse → angoisse`.L'app est prête. Voici ce qu'elle fait et comment la lancer.

---

**Installation (une seule fois)**
```bash
pip install spacy snowballstemmer scikit-learn matplotlib
```

**Lancement**
```bash
python3 semantic_projector.py
```

---

**Architecture de l'app**

`SemanticEngine` est le cœur :

- **Méthode exacte** — chaque token du texte est radicalisé avec le stemmer Snowball français, puis comparé aux radicaux du lexique. `susmentionnées` → `susmentionn` matche `susmentionné`. Robuste et rapide.
- **Méthode similarité** — TF-IDF sur n-grammes de caractères (2 à 4), puis cosine similarity entre les tokens du texte et les mots du lexique. Attrape les variantes orthographiques, les termes proches sans être identiques. Seuil à 0.35 (ajustable).

**8 dimensions prédéfinies** : émotions positives/négatives, registre formel/familier, temporalité passé/futur, valeurs morales, champ technique.

**3 vues de résultats** :
- Graphique — barres horizontales triées par score, chaque dimension a sa couleur
- Détail — tableau mot du texte / correspondance lexique / occurrences / méthode
- Classement — tous les mots capturés, triés par fréquence, avec les dimensions qui les ont reconnus

**Éditeur de dimension** — fenêtre modale pour créer/modifier : nom, méthode (exacte ou similarité), couleur, liste de mots du lexique.

**Export** — graphique en PNG/PDF/SVG, résultats en JSON structuré.

