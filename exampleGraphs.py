from sage.all import DiGraph, Graph

GRAPH_DEFINITIONS = {
    "Ejemplo de la guía": {
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
    "Triángulo": {
        "type": DiGraph,
        "start": "A",
        "data": {"A": {"B": 1, "C": 5}, "B": {"C": 2}},
    },
    "Pentágono": {
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
    "Basic exercise": {
        "type": Graph,
        "start": "A",
        "data": [
            ["A", "B", "C", "D"],
            [("A", "B", 4), ("A", "C", 2), ("B", "C", 1), ("B", "D", 5), ("C", "D", 8)],
        ],
    },
    "Intermediate exercise": {
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
    "Advanced exercise": {
        "type": DiGraph,
        "start": "A",
        "data": [
            ["A", "B", "C", "D", "E", "F", "G"],
            [
                ("A", "B", 3),
                ("A", "C", 1),
                ("B", "D", 4),
                ("B", "F", 6),
                ("C", "B", 2),
                ("C", "E", 5),
                ("D", "E", 2),
                ("D", "G", 7),
                ("E", "F", 1),
                ("F", "G", 3),
                ("G", "A", 8),
            ],
        ],
    },
    "Hard exercise": {
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
}


def _create_graph(name):
    config = GRAPH_DEFINITIONS[name]
    return config["type"](config["data"], weighted=True), config["start"]


def get_clrs_graph():
    return _create_graph("Ejemplo de la guía")


def get_simple_triangle():
    return _create_graph("Triángulo")


def get_path_vs_shortcut():
    return _create_graph("Pentágono")


def get_negative_edge_graph():
    return _create_graph("Pesos Negativos")


def get_peeper_graph():
    return _create_graph("Peeper")


def get_basic_exercise():
    return _create_graph("Basic exercise")


def get_intermediate_exercise():
    return _create_graph("Intermediate exercise")


def get_advanced_exercise():
    return _create_graph("Advanced exercise")


def get_challenge_exercise():
    return _create_graph("Hard exercise")


def get_all_graphs():
    return {name: _create_graph(name) for name in GRAPH_DEFINITIONS}


def get_ejercicios_graphs():
    return {
        "Ejercicio 1": get_basic_exercise(),
        "Ejercicio 2": get_intermediate_exercise(),
        "Ejercicio 3": get_peeper_graph(),
        "Ejercicio 4": get_advanced_exercise(),
        "Ejercicio 5": get_challenge_exercise(),
    }


def get_custom_layouts():
    peeper_layout = {
        "a": (0, 0),
        "b": (1, 1.5),
        "c": (1, -1.5),
        "d": (1.5, 3),
        "e": (1.5, -3),
        "f": (3.5, 0),
        "g": (5, 1.2),
        "h": (5, -1.2),
    }
    return {
        "Peeper": peeper_layout,
        "Ejercicio 3": peeper_layout,
    }
