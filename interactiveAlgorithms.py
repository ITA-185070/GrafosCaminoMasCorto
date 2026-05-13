from IPython.display import display, HTML, clear_output
import ipywidgets as widgets
from visualConfigs import Colors, get_html_table
from stepByStepAlgorithms import dijkstra_step_by_step, bellman_ford_step_by_step


class AlgorithmVisualizer:
    def __init__(
        self,
        graphs=None,
        G_default=None,
        s_default=None,
        algo_default=None,
    ):
        self.graphs = graphs
        self.G = G_default
        self.s = s_default
        self.layout_cache = {}
        self.steps = []

        self.show_graph_selector = graphs is not None and G_default is None
        self.show_source_selector = s_default is None
        self.show_algo_selector = algo_default is None

        self._setup_widgets(algo_default or "Dijkstra")
        self._initialize_algorithm(reset_source=True)

    def _setup_widgets(self, algo_default):
        self.graph_drop = widgets.Dropdown(
            options=list(self.graphs.keys()) if self.graphs else [],
            description="Grafo:",
            style={"description_width": "initial"},
        )
        self.source_drop = widgets.Dropdown(
            options=[],
            description="Origen:",
            style={"description_width": "initial"},
        )
        self.algo_drop = widgets.Dropdown(
            options=["Dijkstra", "Bellman-Ford"],
            description="Algoritmo:",
            value=algo_default,
            style={"description_width": "initial"},
        )
        self.step_slider = widgets.IntSlider(
            min=0,
            max=0,
            description="Paso:",
            layout={"width": "100%", "max_width": "600px"},
            style={"description_width": "initial"},
        )
        self.desc_label = widgets.HTMLMath(
            value="", layout={"margin": "10px 0px 10px 0px"}
        )

        self.plot_out = widgets.Output(
            layout={"flex": "2", "min_height": "400px", "border": "none"}
        )
        self.table_out = widgets.Output(
            layout={"flex": "1", "padding": "10px 0px 0px 10px", "border": "none"}
        )
        self.viz_container = widgets.HBox(
            [self.plot_out, self.table_out],
            layout={"width": "100%", "align_items": "flex-start", "border": "none"},
        )

        # Observadores
        self.graph_drop.observe(self._on_config_change, names="value")
        self.source_drop.observe(self._on_source_change, names="value")
        self.algo_drop.observe(self._on_config_change, names="value")
        self.step_slider.observe(self._render_current_step, names="value")

    def _initialize_algorithm(self, reset_source=False):
        graph_key = self.graph_drop.value if self.graphs else id(self.G)

        if self.graphs:
            self.G, default_s = self.graphs[graph_key]

            current_vertices = sorted(list(self.G.vertices()))
            if list(self.source_drop.options) != current_vertices:
                self.source_drop.options = current_vertices

            if reset_source or self.source_drop.value not in self.G.vertices():
                self.source_drop.value = default_s

        elif self.G:
            current_vertices = sorted(list(self.G.vertices()))
            if list(self.source_drop.options) != current_vertices:
                self.source_drop.options = current_vertices

            if (
                self.source_drop.value is None
                or self.source_drop.value not in self.G.vertices()
            ):
                self.source_drop.value = (
                    self.s if self.s in self.G.vertices() else current_vertices[0]
                )

        self.s = self.source_drop.value

        if graph_key not in self.layout_cache:
            from exampleGraphs import get_custom_layouts

            custom_layouts = get_custom_layouts()

            # Match layout: Try exact match first, then substring match (e.g. "1. Peeper" -> "Peeper")
            layout = custom_layouts.get(graph_key)
            if not layout:
                for key, val in custom_layouts.items():
                    if key in str(graph_key):
                        layout = val
                        break

            if layout:
                self.layout_cache[graph_key] = layout
            else:
                self.layout_cache[graph_key] = self.G.layout(layout="spring")

        generator = (
            dijkstra_step_by_step
            if self.algo_drop.value == "Dijkstra"
            else bellman_ford_step_by_step
        )
        self.steps = list(generator(self.G, self.s))

        self.step_slider.max = len(self.steps) - 1
        self.step_slider.value = 0
        self._render_current_step()

    def _on_config_change(self, change):
        reset = change["owner"] == self.graph_drop
        self._initialize_algorithm(reset_source=reset)

    def _on_source_change(self, change):
        if change["new"] is not None:
            self._initialize_algorithm(reset_source=False)

    def _get_matching_edges(self, u, v):
        return [
            e
            for e in self.G.edges()
            if (e[0] == u and e[1] == v)
            or (not self.G.is_directed() and e[1] == u and e[0] == v)
        ]

    def _get_vertex_colors(self, state):
        v_colors = {Colors.DEFAULT_VERTEX: self.G.vertices()}
        reached = [v for v in self.G.vertices() if state["d"][v] < float("inf")]

        if reached:
            v_colors[Colors.REACHED_VERTEX] = reached
        if "S" in state:
            v_colors[Colors.CLOSED_VERTEX] = state["S"]
        if state.get("u"):
            v_colors[Colors.ACTIVE_VERTEX] = [state["u"]]
        if state.get("error"):
            v_colors[Colors.ERROR_VERTEX] = [state["v"]]

        return v_colors

    def _get_edge_colors(self, state):
        u, v = state.get("u"), state.get("v")
        e_colors = {}
        active_edges = []

        if u and v:
            color = Colors.RELAX_SUCCESS if state.get("relaxed") else Colors.RELAX_CHECK
            active_edges = self._get_matching_edges(u, v)
            e_colors[color] = active_edges

        tree_edges = []
        active_pairs = [e[:2] for e in active_edges]
        for dst, src in state["pi"].items():
            if src is not None:
                matches = self._get_matching_edges(src, dst)
                if matches:
                    edge = matches[0]
                    if edge[:2] not in active_pairs:
                        tree_edges.append(edge)

        if tree_edges:
            e_colors[Colors.TREE_EDGE] = tree_edges

        # 3. Aristas por Defecto (Gris)
        special_pairs = active_pairs + [e[:2] for e in tree_edges]
        other_edges = [
            e
            for e in self.G.edges()
            if e[:2] not in special_pairs
            and (self.G.is_directed() or (e[1], e[0]) not in special_pairs)
        ]

        if other_edges:
            e_colors[Colors.DEFAULT_EDGE] = other_edges

        return e_colors

    def _render_current_step(self, _=None):
        if not self.steps:
            return

        state = self.steps[self.step_slider.value]
        graph_key = self.graph_drop.value if self.graphs else id(self.G)

        self.desc_label.value = (
            f"<div style='font-size:16px; font-weight:bold;'>{state['desc']}</div>"
        )

        with self.plot_out:
            clear_output(wait=True)
            p = self.G.plot(
                pos=self.layout_cache[graph_key],
                vertex_colors=self._get_vertex_colors(state),
                edge_colors=self._get_edge_colors(state),
                edge_labels=True,
                vertex_size=600,
                talk=True,
            )
            display(p)

        with self.table_out:
            clear_output(wait=True)
            display(HTML(get_html_table(self.G, state)))

    def display(self):
        ui_header = []
        selectors = []
        if self.show_graph_selector:
            selectors.append(self.graph_drop)
        if self.show_source_selector:
            selectors.append(self.source_drop)
        if self.show_algo_selector:
            selectors.append(self.algo_drop)

        if selectors:
            ui_header.append(widgets.HBox(selectors, layout={"border": "none"}))

        main_box = widgets.VBox(
            ui_header + [self.step_slider, self.desc_label, self.viz_container],
            layout={"border": "none"},
        )
        display(main_box)


def launch_case(G_in=None, s_in=None, algo_name=None, graphs=None):
    viz = AlgorithmVisualizer(
        graphs=graphs,
        G_default=G_in,
        s_default=s_in,
        algo_default=algo_name,
    )
    viz.display()


def launch_visualizer(graphs_source):
    if callable(graphs_source):
        graphs = graphs_source()
    else:
        graphs = graphs_source
    launch_case(graphs=graphs)
