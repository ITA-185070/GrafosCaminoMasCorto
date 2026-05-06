class Colors:
    DEFAULT_VERTEX = "white"
    REACHED_VERTEX = "#E0F7FA"  # (alcanzados)
    CLOSED_VERTEX = "#C8E6C9"  # (S-set en Dijkstra)
    ACTIVE_VERTEX = "#FFF176"  # (nodo u actual)
    ERROR_VERTEX = "#FFCDD2"  # (ciclo negativo)

    DEFAULT_EDGE = "#9E9E9E"
    TREE_EDGE = "#2196F3"  # (Shortest Path Tree)
    RELAX_SUCCESS = "#D32F2F"  # (actualización de distancia)
    RELAX_CHECK = "#F57C00"  # (comprobación sin cambios)


def get_html_table(G, state):
    """Genera una tabla HTML con las estimaciones d y los predecesores pi."""
    inf_sym = "\u221e"
    rows = []
    for v in sorted(G.vertices()):
        dist = state["d"][v]
        dist_str = inf_sym if dist == float("inf") else str(dist)
        pred = str(state["pi"][v]) if state["pi"][v] is not None else "NIL"
        rows.append(f"<tr><td>{v}</td><td>{dist_str}</td><td>{pred}</td></tr>")

    return fr"""
    <table border="1" style="width:100%; max-width:300px; text-align:center; font-family:sans-serif; border-collapse: collapse;">
        <tr style="background:#f2f2f2;">
            <th style="padding: 5px;">Vértice</th>
            <th style="padding: 5px;">$d$</th>
            <th style="padding: 5px;">$\pi$</th>
        </tr>
        {"".join(rows)}
    </table>
    """
