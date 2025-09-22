# =================================================
# CORSO DI ALGORIMI E STRUTTURE DATI
# Lezione 4
# =================================================
# ALGORIMS AND DATA STRUCTURES COURSE
# Lesson 4 
# =================================================
# Prof. Andrea Cigliano
# =================================================

from collections import deque, defaultdict
import math
import heapq

# ============================================================
# Rappresentazione consigliata del grafo pesato:
# graph[u][v] = peso dell'arco u->v  (dizionario di dizionari)
# Per BFS/DFS (non pesati) si può usare graph_simple[u] = [v1, v2, ...]
# ============================================================


# ------------------------------------------------------------
# DIJKSTRA: cammini minimi da una sorgente con pesi NON negativi
# ------------------------------------------------------------
def dijkstra(graph, source):
    """
    graph: dict[str, dict[str, float]]  es. graph['A']['B'] = 3.5
    source: nodo sorgente
    Ritorna:
      dist:  dict nodo -> distanza minima da source
      prev:  dict nodo -> predecessore sul cammino minimo (per ricostruire il path)
    Complessità: O((V+E) log V) con min-heap
    """
    dist = {u: math.inf for u in graph}
    prev = {u: None for u in graph}
    dist[source] = 0.0

    # coda di priorità: (distanza, nodo)
    pq = [(0.0, source)]
    visited = set()

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)

        # Se il nodo non ha uscenti, .get evita KeyError
        for v, w in graph.get(u, {}).items():
            if w < 0:
                raise ValueError("Dijkstra richiede pesi non negativi.")
            nd = d + w
            if nd < dist.get(v, math.inf):
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))

    return dist, prev


# ------------------------------------------------------------
# BELLMAN–FORD: cammini minimi con pesi anche negativi
#                e rilevazione di cicli negativi raggiungibili
# ------------------------------------------------------------
def bellman_ford(graph, source):
    """
    graph: dict[str, dict[str, float]]
    source: nodo sorgente
    Ritorna:
      dist: dict nodo -> distanza minima
      prev: dict nodo -> predecessore
      has_negative_cycle: bool (True se esiste ciclo negativo raggiungibile)
    Complessità: O(V * E)
    """
    # Costruisco lista nodi e lista archi
    nodes = set(graph.keys())
    for u in graph:
        nodes.update(graph[u].keys())
    nodes = list(nodes)

    edges = []
    for u, nbrs in graph.items():
        for v, w in nbrs.items():
            edges.append((u, v, w))

    dist = {u: math.inf for u in nodes}
    prev = {u: None for u in nodes}
    dist[source] = 0.0

    # Relaxation ripetuta V-1 volte
    for _ in range(len(nodes) - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != math.inf and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                updated = True
        if not updated:
            break  # ottimizzazione

    # Controllo cicli negativi raggiungibili
    has_negative_cycle = False
    for u, v, w in edges:
        if dist[u] != math.inf and dist[u] + w < dist[v]:
            has_negative_cycle = True
            break

    return dist, prev, has_negative_cycle


# ------------------------------------------------------------
# FLOYD–WARSHALL: tutte le coppie di cammini minimi
#                 supporta pesi negativi (ma non cicli negativi)
# ------------------------------------------------------------
def floyd_warshall(graph):
    """
    graph: dict[str, dict[str, float]]
    Ritorna:
      dist[u][v]: distanza minima da u a v
      nxt[u][v]:  prossimo nodo dopo u sul cammino minimo verso v (per ricostruzione)
    Complessità: O(V^3), Spazio: O(V^2)
    """
    # Insieme nodi
    nodes = set(graph.keys())
    for u in graph:
        nodes.update(graph[u].keys())
    nodes = list(nodes)

    # Inizializzazione matrici dist e nxt
    dist = {u: {v: math.inf for v in nodes} for u in nodes}
    nxt  = {u: {v: None      for v in nodes} for u in nodes}

    for u in nodes:
        dist[u][u] = 0.0
        nxt[u][u] = u

    for u, nbrs in graph.items():
        for v, w in nbrs.items():
            if w < dist[u][v]:
                dist[u][v] = w
                nxt[u][v] = v

    # Dinamica: prova tutti i nodi come intermedi
    for k in nodes:
        for i in nodes:
            dik = dist[i][k]
            if dik == math.inf:
                continue
            for j in nodes:
                # Evita somme inutili se k->j infinito
                if dist[k][j] == math.inf:
                    continue
                nd = dik + dist[k][j]
                if nd < dist[i][j]:
                    dist[i][j] = nd
                    nxt[i][j] = nxt[i][k]

    # Facoltativo: controllo cicli negativi (dist[u][u] < 0)
    # Se serve agire, qui si potrebbe marcare coppie coinvolte.
    return dist, nxt


def reconstruct_path_fw(nxt, u, v):
    """
    Ricostruisce il cammino u->v usando 'nxt' di Floyd–Warshall.
    Ritorna lista di nodi [u, ..., v] oppure [] se non esiste.
    """
    if nxt.get(u, {}).get(v) is None:
        return []
    path = [u]
    while u != v:
        u = nxt[u][v]
        path.append(u)
    return path


# ------------------------------------------------------------
# BFS (Breadth-First Search) su grafo NON pesato
# ------------------------------------------------------------
def bfs(graph_simple, start):
    """
    graph_simple: dict[str, list[str]]  adiacenze (non pesate)
    start: nodo sorgente
    Ritorna:
      order: lista in ordine di visita
      parent: dict nodo -> padre nell'albero BFS (per cammini minimi in numero di archi)
    Complessità: O(V + E)
    """
    visited = set([start])
    parent = {start: None}
    order = []

    q = deque([start])
    while q:
        u = q.popleft()
        order.append(u)
        for v in graph_simple.get(u, []):
            if v not in visited:
                visited.add(v)
                parent[v] = u
                q.append(v)
    return order, parent


# ------------------------------------------------------------
# DFS (Depth-First Search) ricorsiva su grafo NON pesato
# ------------------------------------------------------------
def dfs(graph_simple, start):
    """
    graph_simple: dict[str, list[str]]
    start: nodo sorgente
    Ritorna:
      order: lista in ordine di visita (preorder)
      parent: dict nodo -> padre nell'albero DFS
    Complessità: O(V + E)
    """
    visited = set()
    parent = {start: None}
    order = []

    def _visit(u):
        visited.add(u)
        order.append(u)
        for v in graph_simple.get(u, []):
            if v not in visited:
                parent[v] = u
                _visit(v)

    _visit(start)
    return order, parent


# ------------------------------------------------------------
# ESEMPI D'USO RAPIDI
# ------------------------------------------------------------
if __name__ == "__main__":
    # Grafo pesato per Dijkstra / Bellman-Ford / Floyd–Warshall
    G = {
        'A': {'B': 4, 'C': 1},
        'B': {'C': 2, 'D': 5},
        'C': {'B': 1, 'D': 8, 'E': 10},
        'D': {'E': 2},
        'E': {}
    }

    # Dijkstra (pesi non negativi)
    dist_dij, prev_dij = dijkstra(G, 'A')
    print("Dijkstra distanze:", dist_dij)

    # Bellman–Ford (supporta pesi negativi)
    dist_bf, prev_bf, neg_cycle = bellman_ford(G, 'A')
    print("Bellman-Ford distanze:", dist_bf, "ciclo negativo:", neg_cycle)

    # Floyd–Warshall (tutte le coppie)
    dist_fw, nxt_fw = floyd_warshall(G)
    print("Floyd–Warshall A->E:", dist_fw['A']['E'], "path:", reconstruct_path_fw(nxt_fw, 'A', 'E'))

    # Grafo non pesato per BFS/DFS
    GU = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F'],
        'D': [],
        'E': ['F'],
        'F': []
    }
    order_bfs, parent_bfs = bfs(GU, 'A')
    print("BFS order:", order_bfs)

    order_dfs, parent_dfs = dfs(GU, 'A')
    print("DFS order:", order_dfs)
