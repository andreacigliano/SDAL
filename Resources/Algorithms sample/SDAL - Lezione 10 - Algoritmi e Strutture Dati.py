# =================================================
# CORSO DI ALGORIMI E STRUTTURE DATI
# Lezione 10
# =================================================
# ALGORIMS AND DATA STRUCTURES COURSE
# Lesson 10
# =================================================
# Prof. Andrea Cigliano
# =================================================

from collections import deque
from math import inf

# ======================================================================
# Rete di Flusso, Rete Residua e utilità comuni
# ======================================================================

class Edge:
    """
    Arco orientato con capacità e puntatore all'arco residuo (reverse).
    - to: nodo di arrivo
    - cap: capacità residua corrente
    - rev: indice dell'arco inverso nella lista di adiacenza del nodo 'to'
    Nota: Non memorizziamo esplicitamente il "flusso"; il flusso è implicito
    nella coppia (cap forward, cap backward) della rete residua.
    """
    __slots__ = ("to", "cap", "rev")
    def __init__(self, to, cap, rev):
        self.to = to
        self.cap = cap
        self.rev = rev

class FlowNetwork:
    """
    Struttura dati per una Rete di Flusso:
    - grafo orientato con capacità >= 0
    - costruiamo direttamente la Rete Residua (archi forward + backward).
    """
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n)]  # lista di adiacenza di Edge

    def add_edge(self, u, v, c):
        """
        Aggiunge un arco u -> v di capacità c e il relativo arco inverso v -> u di capacità 0.
        L'arco inverso serve per "stornare" flusso in fase di miglioramento (rete residua).
        """
        assert c >= 0
        fwd = Edge(v, c, len(self.adj[v]))    # arco forward residuo
        rev = Edge(u, 0, len(self.adj[u]))    # arco backward residuo
        self.adj[u].append(fwd)
        self.adj[v].append(rev)

    # --------------------------- Utilità debug (facoltative) ---------------------------
    def residual_cap(self, u, i):
        """Capacità residua dell'i-esimo arco uscente da u."""
        return self.adj[u][i].cap

# ======================================================================
# Ford–Fulkerson (schema generale con DFS per trovare cammini aumentanti)
# ======================================================================

def ford_fulkerson_max_flow(net: FlowNetwork, s: int, t: int):
    """
    Implementazione DFS-pure (ricerca in profondità) dei cammini aumentanti.
    - Corretta se le capacità sono intere (evita cicli infiniti per incrementi frazionari).
    - Complessità: O(E * max_flow) nel caso peggiore (dipende dagli incrementi).
    """
    n = net.n
    max_flow = 0

    def dfs(u, t, f, seen):
        """Trova un cammino aumentante con DFS, restituendo il flusso incrementale possibile."""
        if u == t:
            return f
        seen[u] = True
        for i, e in enumerate(net.adj[u]):
            if e.cap > 0 and not seen[e.to]:
                # flusso incrementale limitato dalla capacità residua dell'arco
                pushed = dfs(e.to, t, min(f, e.cap), seen)
                if pushed > 0:
                    # Aggiorna rete residua: diminuisci cap forward, aumenta cap backward
                    e.cap -= pushed
                    net.adj[e.to][e.rev].cap += pushed
                    return pushed
        return 0

    while True:
        seen = [False]*n
        pushed = dfs(s, t, inf, seen)
        if pushed == 0:
            break  # nessun cammino aumentante residuo
        max_flow += pushed

    return max_flow

# ======================================================================
# Edmonds–Karp (Ford–Fulkerson con BFS: cammini aumentanti più corti in archi)
# ======================================================================

def edmonds_karp_max_flow(net: FlowNetwork, s: int, t: int):
    """
    Edmonds–Karp usa BFS sulla rete residua per trovare il cammino aumentante
    più corto in numero di archi.
    - Complessità: O(V * E^2) nel caso peggiore.
    - Vantaggio: tempo polinomiale garantito e semplice da implementare.
    """
    n = net.n
    max_flow = 0

    while True:
        # BFS per trovare cammino aumentante
        parent = [(-1, -1)] * n  # (predecessore, indice_arco_su_predecessore)
        parent[s] = (s, -1)
        q = deque([s])
        while q and parent[t][0] == -1:
            u = q.popleft()
            for i, e in enumerate(net.adj[u]):
                if e.cap > 0 and parent[e.to][0] == -1:
                    parent[e.to] = (u, i)
                    q.append(e.to)
                    if e.to == t:
                        break

        if parent[t][0] == -1:
            break  # nessun cammino aumentante

        # Calcola il collo di bottiglia (bottleneck) lungo il cammino trovato
        bottleneck = inf
        v = t
        while v != s:
            u, i = parent[v]
            bottleneck = min(bottleneck, net.adj[u][i].cap)
            v = u

        # Aggiorna le capacità residue lungo il cammino
        v = t
        while v != s:
            u, i = parent[v]
            e = net.adj[u][i]
            e.cap -= bottleneck
            net.adj[e.to][e.rev].cap += bottleneck
            v = u

        max_flow += bottleneck

    return max_flow

# ======================================================================
# Dinic (livelli + DFS per blocking flow)
# ======================================================================

class Dinic:
    """
    Dinic costruisce livelli con BFS e invia flusso con DFS "current arc" fino a blocking flow.
    - Complessità: O(E * V^2) in generale;
      O(E * sqrt(V)) per grafi bipartiti; O(E * V^(2/3)) con capacità unità (risultati classici).
    - Praticamente spesso molto più veloce di EK.
    """
    def __init__(self, net: FlowNetwork, s: int, t: int):
        self.net = net
        self.s = s
        self.t = t
        self.level = [-1]*net.n
        self.it = [0]*net.n  # "current arc" optimization

    def bfs_level_graph(self) -> bool:
        """Costruisce il grafo dei livelli (rete residua in termini di distanze da s)."""
        self.level = [-1]*self.net.n
        q = deque([self.s])
        self.level[self.s] = 0
        while q:
            u = q.popleft()
            for e in self.net.adj[u]:
                if e.cap > 0 and self.level[e.to] < 0:
                    self.level[e.to] = self.level[u] + 1
                    q.append(e.to)
        return self.level[self.t] >= 0  # t raggiungibile?

    def dfs_blocking_flow(self, u, f) -> int:
        """Invia flusso lungo il grafo dei livelli fino a raggiungere un 'blocking flow'."""
        if u == self.t:
            return f
        for i in range(self.it[u], len(self.net.adj[u])):
            self.it[u] = i  # ricordiamo dove eravamo (current arc)
            e = self.net.adj[u][i]
            if e.cap > 0 and self.level[u] + 1 == self.level[e.to]:
                pushed = self.dfs_blocking_flow(e.to, min(f, e.cap))
                if pushed > 0:
                    e.cap -= pushed
                    self.net.adj[e.to][e.rev].cap += pushed
                    return pushed
        return 0

    def max_flow(self) -> int:
        flow = 0
        # Ripeti: costruisci livelli e invia blocking flows
        while self.bfs_level_graph():
            self.it = [0]*self.net.n
            while True:
                pushed = self.dfs_blocking_flow(self.s, inf)
                if pushed == 0:
                    break
                flow += pushed
        return flow

# ======================================================================
# Esempio d'uso (scommenta per provare)
# ======================================================================
if __name__ == "__main__":
    # Grafo di esempio:
    # s=0 -> 1(cap 10), 2(cap 5)
    # 1 -> 2(15), 3(10)
    # 2 -> 4(10)
    # 3 -> t=5 (10)
    # 4 -> 3(15), 5(10)
    n = 6
    s, t = 0, 5

    # Prova Ford–Fulkerson
    net1 = FlowNetwork(n)
    net1.add_edge(0,1,10); net1.add_edge(0,2,5)
    net1.add_edge(1,2,15); net1.add_edge(1,3,10)
    net1.add_edge(2,4,10)
    net1.add_edge(4,3,15); net1.add_edge(3,5,10); net1.add_edge(4,5,10)
    print("Ford–Fulkerson max flow:", ford_fulkerson_max_flow(net1, s, t))

    # Prova Edmonds–Karp
    net2 = FlowNetwork(n)
    net2.add_edge(0,1,10); net2.add_edge(0,2,5)
    net2.add_edge(1,2,15); net2.add_edge(1,3,10)
    net2.add_edge(2,4,10)
    net2.add_edge(4,3,15); net2.add_edge(3,5,10); net2.add_edge(4,5,10)
    print("Edmonds–Karp max flow:", edmonds_karp_max_flow(net2, s, t))

    # Prova Dinic
    net3 = FlowNetwork(n)
    net3.add_edge(0,1,10); net3.add_edge(0,2,5)
    net3.add_edge(1,2,15); net3.add_edge(1,3,10)
    net3.add_edge(2,4,10)
    net3.add_edge(4,3,15); net3.add_edge(3,5,10); net3.add_edge(4,5,10)
    print("Dinic max flow:", Dinic(net3, s, t).max_flow())
