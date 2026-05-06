import heapq

"""
INITIALIZE-SINGLE-SOURCE(G, s) 
1  for each vertex v ∈ V[G] 
2       do d[v] ← ∞ 
3          π[v] ← NIL 
4  d[s] ← 0
"""


def initialize_single_source(V, s):
    d = {v: float("inf") for v in V}
    pi = {v: None for v in V}
    d[s] = 0
    return d, pi


"""
RELAX(u, v, w) 
1  if d[v] > d[u] + w(u, v) 
2     then d[v] ← d[u] + w(u, v) 
3          π[v] ← u
"""


def relax(u, v, w, d, pi):
    if d[v] > d[u] + w:
        d[v] = d[u] + w
        pi[v] = u
        return True
    return False


"""
DIJKSTRA(G, w, s) 
1  INITIALIZE-SINGLE-SOURCE(G, s) 
2  S ← Ø 
3  Q ← V[G] 
4  while Q ≠ Ø 
5      do u ← EXTRACT-MIN(Q) 
6         S ← S U {u} 
7         for each vertex v ∈ Adj[u] 
8             do RELAX(u, v, w)
"""


def dijkstra(V, Adj, s):
    d, pi = initialize_single_source(V, s)
    S = set()
    # Q is a priority queue of (distance, vertex)
    Q = [(d[v], v) for v in V]
    heapq.heapify(Q)
    while Q:
        # u = EXTRACT-MIN(Q)
        du, u = heapq.heappop(Q)
        # the distance is greater theres no reason to process it
        if du > d[u]:
            continue
        # S = S U {u}
        S.add(u)
        # for each vertex v in Adj[u]
        for v, weight in Adj.get(u, []):
            # RELAX(u, v, w)
            if relax(u, v, weight, d, pi):
                heapq.heappush(Q, (d[v], v))
    return d, pi


"""
BELLMAN-FORD(G, w, s) 
1  INITIALIZE-SINGLE-SOURCE(G, s) 
2  for i ← 1 to |V[G]| - 1 
3       do for each edge (u, v) ∈ E[G] 
4              do RELAX(u, v, w) 
5  for each edge (u, v) ∈ E[G] 
6       do if d[v] > d[u] + w(u, v) 
7             then return FALSE 
8  return TRUE
"""


def bellman_ford(V, E_weighted, s):
    d, pi = initialize_single_source(V, s)

    for i in range(len(V) - 1):
        for u, v, w in E_weighted:
            relax(u, v, w, d, pi)

    for u, v, w in E_weighted:
        if d[v] > d[u] + w:
            return False, d, pi
    return True, d, pi
