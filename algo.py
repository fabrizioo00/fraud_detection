import random
import math


class GrapheAleatoire:
    """
    Graphe aléatoire G(n, p) — Modèle d'Erdős–Rényi.
    Pour chaque paire de sommets, une arête est créée avec probabilité p.
    Le nombre d'arêtes est donc aléatoire, d'espérance p × n(n-1)/2.
    Connexité garantie : p est forcé à max(p, ln(n)/n).
    """

    def __init__(self, n: int, p: float):
        self.n = n
        # Seuil de connexité : p > ln(n)/n
        seuil = math.log(n) / n if n > 1 else 1.0
        self.p = max(p, seuil)
        self.adjacence = {i: set() for i in range(n)}
        self.aretes = []
        self._generer()

    def _generer(self):
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if random.random() < self.p:
                    self.adjacence[i].add(j)
                    self.adjacence[j].add(i)
                    self.aretes.append((i, j))

    def degre(self, sommet: int) -> int:
        return len(self.adjacence[sommet])

    def __repr__(self):
        return f"G(n={self.n}, p={self.p}, arêtes={len(self.aretes)})"


if __name__ == "__main__":
    G = GrapheAleatoire(n=10, p=0.3)
    print(G)
    for i in range(G.n):
        print(f"  sommet {i} → voisins {sorted(G.adjacence[i])}")
