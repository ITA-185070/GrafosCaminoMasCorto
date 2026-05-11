from sage.all import DiGraph, Graph


def get_clrs_graph():
    data = {
        "a": {"b": 5, "c": 10},
        "b": {"a": 5, "c": 15, "d": 5, "f": 6},
        "c": {"a": 10, "b": 15, "d": 7, "g": 12, "e": 30},
        "d": {"b": 5, "c": 7, "f": 9, "g": 8},
        "e": {"g": 20, "c": 30},
        "f": {"b": 6, "d": 9, "g": 14},
        "g": {"f": 14, "d": 8, "c": 12, "e": 20},
    }
    G = Graph(data, weighted=True)
    return G, "a"


def get_simple_triangle():
    data = {"A": {"B": 1, "C": 5}, "B": {"C": 2}}
    G = DiGraph(data, weighted=True)
    return G, "A"


def get_path_vs_shortcut():
    data = {"Start": {"A": 1, "End": 10}, "A": {"B": 1}, "B": {"C": 1}, "C": {"End": 1}}
    G = DiGraph(data, weighted=True)
    return G, "Start"


def get_negative_edge_graph():
    data = {
        "s": {"a": 6, "b": 7},
        "a": {"b": 8, "d": -4, "c": 5},
        "b": {"c": -3, "d": 9},
        "c": {"b": -2},
        "d": {"c": 7, "s": 2},
    }
    G = DiGraph(data, weighted=True)
    return G, "s"


def get_all_graphs():
    return {
        "Ejemplo de la guia": get_clrs_graph(),
        "Triango": get_simple_triangle(),
        "Pentagono": get_path_vs_shortcut(),
        "Pesos Negativos": get_negative_edge_graph(),
    }
