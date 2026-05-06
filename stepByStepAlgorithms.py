def dijkstra_step_by_step(G, s):
    V = G.vertices()
    d = {v: float("inf") for v in V}
    pi = {v: None for v in V}
    d[s] = 0
    S, Q = [], list(V)

    yield {
        "d": d.copy(),
        "pi": pi.copy(),
        "S": list(S),
        "u": None,
        "v": None,
        "desc": rf"Inicio: $d[{s}]=0$.",
    }

    while Q:
        u = min(Q, key=lambda node: d[node])
        Q.remove(u)
        S.append(u)

        yield {
            "d": d.copy(),
            "pi": pi.copy(),
            "S": list(S),
            "u": u,
            "v": None,
            "desc": f"Activo: $u={u}$ (mínimo).",
        }

        for edge in G.edges_incident(u):
            u_edge, v_edge, w = edge
            neighbor = v_edge if u_edge == u else u_edge

            relaxed = d[neighbor] > d[u] + w
            if relaxed:
                d[neighbor] = d[u] + w
                pi[neighbor] = u

            yield {
                "d": d.copy(),
                "pi": pi.copy(),
                "S": list(S),
                "u": u,
                "v": neighbor,
                "relaxed": relaxed,
                "desc": f"Relax ({u},{neighbor}): "
                + ("Mejora" if relaxed else "Igual"),
            }

    yield {
        "d": d.copy(),
        "pi": pi.copy(),
        "S": list(S),
        "u": None,
        "v": None,
        "desc": "Fin: OK.",
    }


def bellman_ford_step_by_step(G, s):
    V = G.vertices()
    # Preparar lista de aristas dirigida (si el grafo es no dirigido, duplicamos cada arista)
    edges_to_relax = []
    for u_e, v_e, w_e in G.edges():
        edges_to_relax.append((u_e, v_e, w_e))
        if not G.is_directed():
            edges_to_relax.append((v_e, u_e, w_e))

    d = {v: float("inf") for v in V}
    pi = {v: None for v in V}
    d[s] = 0

    yield {
        "d": d.copy(),
        "pi": pi.copy(),
        "u": None,
        "v": None,
        "desc": f"Inicio: $d[{s}]=0$.",
    }

    for i in range(len(V) - 1):
        any_change = False
        for u, v, w in edges_to_relax:
            relaxed = d[v] > d[u] + w
            if relaxed:
                d[v] = d[u] + w
                pi[v] = u
                any_change = True

            yield {
                "d": d.copy(),
                "pi": pi.copy(),
                "u": u,
                "v": v,
                "relaxed": relaxed,
                "desc": f"Relax ({u},{v}): " + ("Mejora" if relaxed else "Igual"),
            }

        if not any_change:
            yield {
                "d": d.copy(),
                "pi": pi.copy(),
                "u": None,
                "v": None,
                "desc": "Fin: Convergencia.",
            }
            break

    # Comprobación de ciclos negativos
    for u, v, w in edges_to_relax:
        if d[v] > d[u] + w:
            yield {
                "d": d.copy(),
                "pi": pi.copy(),
                "u": u,
                "v": v,
                "error": True,
                "desc": "Error: Ciclo neg.",
            }
            return

    yield {"d": d.copy(), "pi": pi.copy(), "u": None, "v": None, "desc": "Fin: OK."}
