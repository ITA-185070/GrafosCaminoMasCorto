from sage.all import DiGraph, Graph

GRAPH_DEFINITIONS = {
    "Ejemplo de la guia": {
        "type": Graph,
        "start": "a",
        "data": {
            "a": {"b": 5, "c": 10},
            "b": {"a": 5, "c": 15, "d": 5, "f": 6},
            "c": {"a": 10, "b": 15, "d": 7, "g": 12, "e": 30},
            "d": {"b": 5, "c": 7, "f": 9, "g": 8},
            "e": {"g": 20, "c": 30},
            "f": {"b": 6, "d": 9, "g": 14},
            "g": {"f": 14, "d": 8, "c": 12, "e": 20},
        },
    },
    "Triangulo": {
        "type": DiGraph,
        "start": "A",
        "data": {"A": {"B": 1, "C": 5}, "B": {"C": 2}},
    },
    "Pentagono": {
        "type": DiGraph,
        "start": "Start",
        "data": {
            "Start": {"A": 1, "End": 10},
            "A": {"B": 1},
            "B": {"C": 1},
            "C": {"End": 1},
        },
    },
    "Pesos Negativos": {
        "type": DiGraph,
        "start": "s",
        "data": {
            "s": {"a": 6, "b": 7},
            "a": {"b": 8, "d": -4, "c": 5},
            "b": {"c": -3, "d": 9},
            "c": {"b": -2},
            "d": {"c": 7, "s": 2},
        },
    },
    "Peeper": {
        "type": Graph,
        "start": "a",
        "data": [
            ["a", "b", "c", "d", "e", "f", "g", "h"],
            [
                ("a", "b", 4),
                ("a", "c", 8),
                ("b", "d", 3),
                ("c", "e", 2),
                ("b", "f", 7),
                ("c", "f", 1),
                ("f", "g", 5),
                ("f", "h", 6),
                ("g", "h", 2),
            ],
        ],
    },
    "Grafo 1": {
        "type": Graph,
        "start": "A",
        "data": [
            ["A", "B", "C", "D", "E", "F", "G", "H", "I"],
            [
                ("A", "B", 2),
                ("B", "A", 2),
                ("A", "D", 2),
                ("D", "A", 2),
                ("A", "C", 5),
                ("B", "E", 1),
                ("E", "B", 1),
                ("B", "C", 3),
                ("C", "B", 3),
                ("D", "C", 3),
                ("C", "D", 3),
                ("D", "G", 2),
                ("G", "D", 2),
                ("C", "E", 1),
                ("E", "C", 1),
                ("C", "F", 1),
                ("F", "C", 1),
                ("C", "H", 1),
                ("H", "C", 1),
                ("E", "I", 7),
                ("G", "F", 2),
                ("F", "G", 2),
                ("F", "H", 3),
                ("H", "F", 3),
                ("H", "I", 1),
            ],
        ],
    },
    "Grafo 2": {
        "type": DiGraph,
        "start": "A",
        "data": [
            ["A", "B", "C", "D", "E"],
            [
                ("A", "B", 5),
                ("B", "C", 2),
                ("B", "D", 8),
                ("C", "E", 4),
                ("D", "A", 7),
                ("E", "D", 10),
            ],
        ],
    },
    "Grafo 3": {
        "type": DiGraph,
        "start": "A",
        "data": [
            ["A", "B", "C", "D", "E", "F", "G", "H"],
            [
                ("A", "D", 8),
                ("A", "E", 4),
                ("B", "A", 2),
                ("B", "F", 11),
                ("C", "F", 0),
                ("C", "G", 1),
                ("D", "B", 6),
                ("D", "H", 9),
                ("F", "G", 0),
                ("F", "H", 2),
                ("G", "C", 4),
                ("G", "E", 5),
                ("H", "F", 3),
            ],
        ],
    },
    "Grafo 4": {
        "type": DiGraph,
        "start": "A",
        "data": [
            ["A", "B", "C", "D", "E", "F", "G", "H"],
            [
                ("A", "C", 4),
                ("A", "F", 7),
                ("B", "E", 9),
                ("B", "H", 3),
                ("C", "D", 3),
                ("C", "F", 2),
                ("C", "G", 9),
                ("D", "E", 3),
                ("D", "G", 7),
                ("E", "G", 2),
                ("E", "H", 7),
                ("F", "G", 8),
                ("G", "H", 3),
            ],
        ],
    },
}


def _create_graph(name):
    config = GRAPH_DEFINITIONS[name]
    return config["type"](config["data"], weighted=True), config["start"]


def get_clrs_graph():
    return _create_graph("Ejemplo de la guia")


def get_simple_triangle():
    return _create_graph("Triangulo")


def get_path_vs_shortcut():
    return _create_graph("Pentagono")


def get_negative_edge_graph():
    return _create_graph("Pesos Negativos")


def get_peeper_graph():
    return _create_graph("Peeper")


def get_graph_1():
    return _create_graph("Grafo 1")


def get_graph_2():
    return _create_graph("Grafo 2")


def get_graph_3():
    return _create_graph("Grafo 3")


def get_graph_4():
    return _create_graph("Grafo 4")


def get_all_graphs():
    return {name: _create_graph(name) for name in GRAPH_DEFINITIONS}


def get_ejercicios_graphs():
    return {
        "Peeper": get_peeper_graph(),
        "Grafo 1": get_graph_1(),
        "Grafo 2": get_graph_2(),
        "Grafo 3": get_graph_3(),
        "Grafo 4": get_graph_4(),
    }


def get_custom_layouts():
    """Returns custom visual layouts for specific graphs."""
    return {
        "Peeper": {
            "a": (0, 0),
            "b": (1, 1.5),
            "c": (1, -1.5),
            "d": (1.5, 3),
            "e": (1.5, -3),
            "f": (3.5, 0),
            "g": (5, 1.2),
            "h": (5, -1.2),
        }
    }
