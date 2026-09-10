# =================================================
# CORSO DI ALGORIMI E STRUTTURE DATI
# Lezione 9
# =================================================
# ALGORIMS AND DATA STRUCTURES COURSE
# Lesson 9
# =================================================
# Prof. Andrea Cigliano
# =================================================

# ============================================================
# 1) TEMPLATE GENERICO PER ALGORITMI GREEDY + ESEMPIO PRATICO
# ============================================================

from typing import List, Callable, Any, Tuple
import heapq

def greedy_template(items: List[Any],
                    is_feasible: Callable[[List[Any], Any], bool],
                    score: Callable[[Any], Any],
                    choose_best: bool = True) -> List[Any]:
    """
    Template generico per un algoritmo Greedy:
    - items: insieme di elementi candidati
    - is_feasible(soluzione_parziale, item): vincolo di ammissibilità
    - score(item): funzione obiettivo locale (chiave di ordinamento)
    - choose_best: se True prende gli item con score massimo (o minimo se False)

    Strategia:
    1) ordina i candidati secondo una chiave "locale" (score)
    2) itera aggiungendo ogni volta l'elemento "migliore" che mantiene la fattibilità
    """
    # ordiniamo gli item per la scelta golosa
    items_sorted = sorted(items, key=score, reverse=choose_best)

    solution = []
    for x in items_sorted:
        if is_feasible(solution, x):
            solution.append(x)
    return solution


# --- ESEMPIO GREEDY: Activity Selection (massimo numero di intervalli compatibili) ---

def activity_selection(intervals: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Dato un insieme di intervalli (start, end), seleziona un sottoinsieme massimo
    di intervalli a coppie disgiunti (classico problema greedy).

    Strategia greedy: ordina per tempo di fine crescente e seleziona ogni attività
    che non sovrappone l'ultima scelta.
    """
    # ordina per tempo di fine
    intervals_sorted = sorted(intervals, key=lambda x: x[1])

    selected = []
    last_end = -float("inf")
    for s, e in intervals_sorted:
        if s >= last_end:
            selected.append((s, e))
            last_end = e
    return selected


# ============================================================
# 2) MINIMO ALBERO RICOPRENTE (MST)
#    - KRUSKAL (con Union-Find)
#    - PRIM (con coda di priorità)
# ============================================================

# ------------------
# 2.1) KRUSKAL MST
# ------------------

class UnionFind:
    """ Struttura Union-Find (Disjoint Set Union) per supportare Kruskal. """
    def __init__(self, n: int):
        # parent[i] = padre del nodo i; inizialmente ogni nodo è padre di sé stesso
        self.parent = list(range(n))
        # rank (o size) per unione bilanciata
        self.rank = [0] * n

    def find(self, x: int) -> int:
        # path compression: collega direttamente il nodo alla radice
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: int, b: int) -> bool:
        # unisce gli insiemi contenenti a e b; ritorna True se unione effettuata
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        # unione per rank
        if self.rank[ra] < self.rank[rb]:
            self.parent[ra] = rb
        elif self.rank[ra] > self.rank[rb]:
            self.parent[rb] = ra
        else:
            self.parent[rb] = ra
            self.rank[ra] += 1
        return True


def kruskal_mst(n: int, edges: List[Tuple[int, int, float]]) -> Tuple[float, List[Tuple[int, int, float]]]:
    """
    Kruskal:
    - Input: numero di vertici n (0..n-1), lista di archi (u, v, w)
    - Output: (peso_totale, lista_archi_MST)

    Passi:
    1) ordina gli archi per peso crescente
    2) scorri gli archi, aggiungi l'arco se collega componenti disgiunte (Union-Find)
    3) termina quando hai n-1 archi
    """
    uf = UnionFind(n)
    mst = []
    total = 0.0

    # ordina per peso
    edges_sorted = sorted(edges, key=lambda e: e[2])

    for u, v, w in edges_sorted:
        if uf.union(u, v):
            mst.append((u, v, w))
            total += w
            if len(mst) == n - 1:  # un MST per un grafo connesso ha n-1 archi
                break
    return total, mst


# -------------
# 2.2) PRIM MST
# -------------

def prim_mst(n: int, adj: List[List[Tuple[int, float]]], start: int = 0) -> Tuple[float, List[Tuple[int, int, float]]]:
    """
    Prim:
    - Input: numero di vertici n, lista di adiacenza (per ogni u: lista di (v, peso)), vertice di partenza
    - Output: (peso_totale, lista_archi_MST)

    Passi:
    1) parti da un nodo e metti in una min-heap tutti gli archi in uscita
    2) estrai l'arco minimo che collega un nuovo nodo non ancora visitato
    3) aggiungi gli archi del nuovo nodo e continua finché non hai n-1 archi

    Nota: funziona bene con grafi sparsi usando una priority queue.
    """
    visited = [False] * n
    min_heap = []  # heap di (peso, u, v)
    mst = []
    total = 0.0

    def add_edges(u: int):
        """ Aggiunge tutti gli archi (u -> v) verso nodi non visitati nella min-heap. """
        visited[u] = True
        for v, w in adj[u]:
            if not visited[v]:
                heapq.heappush(min_heap, (w, u, v))

    # inizializza con il nodo di partenza
    add_edges(start)

    while min_heap and len(mst) < n - 1:
        w, u, v = heapq.heappop(min_heap)
        if visited[v]:
            continue  # scarta archi che puntano a nodi già inclusi
        # aggiungi l'arco (u, v)
        mst.append((u, v, w))
        total += w
        add_edges(v)

    return total, mst


# ============================================================
# ESEMPIO DI UTILIZZO
# ============================================================

if __name__ == "__main__":
    # --- Esempio Activity Selection ---
    intervals = [(1, 4), (3, 5), (0, 6), (5, 7), (8, 9), (5, 9)]
    print("Attività selezionate (greedy - fine crescente):", activity_selection(intervals))

    # --- Grafo per MST ---
    # Vertici: 0..4
    # Lista archi (u, v, w) non orientati
    edges = [
        (0, 1, 2.0),
        (0, 3, 6.0),
        (1, 2, 3.0),
        (1, 3, 8.0),
        (1, 4, 5.0),
        (2, 4, 7.0),
        (3, 4, 9.0),
    ]
    n = 5

    # KRUSKAL
    tot_k, mst_k = kruskal_mst(n, edges)
    print(f"MST (Kruskal): peso totale = {tot_k}, archi = {mst_k}")

    # PRIM: costruiamo la lista di adiacenza da edges (grafo non orientato)
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    tot_p, mst_p = prim_mst(n, adj, start=0)
    print(f"MST (Prim):    peso totale = {tot_p}, archi = {mst_p}")
