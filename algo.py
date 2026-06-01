import random
import math


class GrapheAleatoire:
    """
    Graphe aléatoire G(n, p) — Modèle d'Erdős–Rényi.
    Pour chaque paire de sommets, une arête est créée avec probabilité p.
    Le nombre d'arêtes est donc aléatoire
    Connexité garantie : p est forcé à max(p, ln(n)/n).
    """

    def __init__(self, n: int, p: float):
        self.n = n
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


# Composantes connexes (DFS)

def composantes_connexes(graphe):
    """DFS : trouve les parties déconnectées du graphe."""
    visite = set()
    composantes = []
    for s in range(graphe.n):
        if s not in visite:
            comp = []
            pile = [s]  # pile au lieu de file
            while pile:
                v = pile.pop()  # pop() = dernier élément = DFS
                if v in visite:
                    continue
                visite.add(v)
                comp.append(v)
                for voisin in graphe.adjacence[v]:
                    if voisin not in visite:
                        pile.append(voisin)
            composantes.append(sorted(comp))
    return composantes


# Communautés (Louvain)

def _modularite(graphe, communaute_de):
    """Calcule la modularité Q du partitionnement actuel."""
    m = len(graphe.aretes)
    if m == 0:
        return 0.0
    q = 0.0
    for i, j in graphe.aretes:
        if communaute_de[i] == communaute_de[j]:
            ki = len(graphe.adjacence[i])
            kj = len(graphe.adjacence[j])
            q += 1 - (ki * kj) / (2 * m)
    return q / m


def communautes(graphe):
    """Louvain : optimise la modularité en déplaçant les nœuds."""
    m = len(graphe.aretes)
    if m == 0:
        return [[s] for s in range(graphe.n)]

    # chaque sommet dans sa propre communauté
    comm = {s: s for s in range(graphe.n)}
    amelioration = True

    while amelioration:
        amelioration = False
        ordre = list(range(graphe.n))
        random.shuffle(ordre)
        for s in ordre:
            # communautés voisines
            comms_voisines = set()
            for v in graphe.adjacence[s]:
                comms_voisines.add(comm[v])

            meilleur_gain = 0.0
            meilleure_comm = comm[s]
            ancien = comm[s]

            for c in comms_voisines:
                if c == ancien:
                    continue
                # gain de modularité si on déplace s vers c
                gain = 0.0
                ki = len(graphe.adjacence[s])
                for v in graphe.adjacence[s]:
                    if comm[v] == c:
                        gain += 1 - (ki * len(graphe.adjacence[v])) / (2 * m)
                    if comm[v] == ancien and v != s:
                        gain -= 1 - (ki * len(graphe.adjacence[v])) / (2 * m)
                if gain > meilleur_gain:
                    meilleur_gain = gain
                    meilleure_comm = c

            if meilleure_comm != ancien:
                comm[s] = meilleure_comm
                amelioration = True

    # grouper par communauté
    groupes = {}
    for s, c in comm.items():
        groupes.setdefault(c, []).append(s)
    return [sorted(g) for g in groupes.values()]


# Cliques maximales (Bron-Kerbosch)

def cliques_maximales(graphe):
    """Bron-Kerbosch : trouve tous les sous-graphes complets maximaux."""
    resultats = []

    def bron_kerbosch(r, p, x):
        if not p and not x:
            if len(r) >= 2:
                resultats.append(sorted(r))
            return
        pivot = max(p | x, key=lambda v: len(graphe.adjacence[v] & p))
        for v in list(p - graphe.adjacence[pivot]):
            voisins = graphe.adjacence[v]
            bron_kerbosch(r | {v}, p & voisins, x & voisins)
            p.remove(v)
            x.add(v)

    bron_kerbosch(set(), set(range(graphe.n)), set())
    return sorted(resultats, key=len, reverse=True)


def classifier(graphe):
    """classification en sous-graphes interessants """
    return {
        "composantes": composantes_connexes(graphe),
        "communautes": communautes(graphe),
        "cliques": cliques_maximales(graphe),
    }


if __name__ == "__main__":
    
    G = GrapheAleatoire(n=15, p=0.25)

    resultats = classifier(G)

    print(f"COMPOSANTES CONNEXES : ({len(resultats['composantes'])})")

    print(f"\nCOMMUNAUTÉS : ({len(resultats['communautes'])})")

    print(f"\nCLIQUES MAXIMALES : ({len(resultats['cliques'])})")
