# 🔍 Fraud Detection — Analyse structurelle de graphes

Détection de structures suspectes dans un réseau modélisé par un **graphe aléatoire d'Erdős–Rényi**, à l'aide d'algorithmes classiques de théorie des graphes.

## 📋 Description

Ce projet construit un graphe aléatoire **connexe, non-orienté et sans boucle** selon le modèle $G(n, p)$, puis applique trois algorithmes de classification pour identifier des sous-structures d'intérêt (composantes connexes, communautés, cliques maximales) dans le contexte de la détection de fraude.

## 🧠 Algorithmes implémentés

| Algorithme | Objectif | Complexité |
|---|---|---|
| **Erdős–Rényi** $G(n, p)$ | Génération du graphe aléatoire connexe | $O(n^2)$ |
| **DFS** (Parcours en profondeur) | Identification des composantes connexes | $O(n + m)$ |
| **Louvain** | Détection de communautés par optimisation de la modularité $Q$ | $O(n \cdot k)$ |
| **Bron-Kerbosch** (avec pivot) | Énumération des cliques maximales (sous-graphes complets) | $O(3^{n/3})$ pire cas |

### Garantie de connexité

La probabilité $p$ est automatiquement ajustée au seuil minimal :

$$p_{\text{effectif}} = \max\left(p,\; \frac{\ln n}{n}\right)$$

Ce seuil garantit la connexité presque sûrement (théorème d'Erdős–Rényi).

## 📁 Structure du projet

```
fraud_detection/
├── algo.py       # Implémentation des algorithmes (graphe + classification)
├── doc.tex       # Documentation technique (LaTeX)
└── README.md
```

## 🚀 Utilisation

### Prérequis

- **Python 3.8+** (aucune dépendance externe, uniquement `random` et `math`)

### Exécution

```bash
python algo.py
```

### Utilisation comme module

```python
from algo import GrapheAleatoire, classifier

```

## 🔬 Détails techniques

### Génération du graphe (`GrapheAleatoire`)

Pour chaque paire $(i, j)$ avec $i < j$, une arête est créée avec probabilité $p$. Cette construction garantit :
- **Sans boucle** — la boucle interne assure $i \neq j$
- **Non-orienté** — chaque arête est ajoutée dans les deux sens
- **Sans multi-arêtes** — chaque paire n'est parcourue qu'une fois, stockée dans des `set()`

### Classification (`classifier`)

La fonction `classifier(G)` exécute les trois algorithmes et retourne un dictionnaire

## 👤 Auteur

**RAKOTOMALALA Andrianina Fabrizio**

## 📜 Licence

Ce projet est développé dans un cadre académique.
