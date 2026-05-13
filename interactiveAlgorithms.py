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
        algo_default="Dijkstra",
        show_selectors=True,
    ):
        self.graphs = graphs
        self.G = G_default
        self.s = s_default
        self.show_selectors = show_selectors
        self.layout_cache = {}
        self.steps = []

        self._setup_widgets(algo_default)
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

        # Contenedores para alineación horizontal sin bordes
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
             
             if self.source_drop.value is None or self.source_drop.value not in self.G.vertices():
                 self.source_drop.value = self.s if self.s in self.G.vertices() else current_vertices[0]

        self.s = self.source_drop.value

        if graph_key not in self.layout_cache:
            from exampleGraphs import get_custom_layouts

            custom_layouts = get_custom_layouts()
            if graph_key in custom_layouts:
                self.layout_cache[graph_key] = custom_layouts[graph_key]
            else:
                self.layout_cache[graph_key] = self.G.layout(layout="spring")

        # Determinar generador según algoritmo
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
        reset = (change["owner"] == self.graph_drop)
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

        # 1. Arista Activa (en proceso de relajación)
        if u and v:
            color = Colors.RELAX_SUCCESS if state.get("relaxed") else Colors.RELAX_CHECK
            active_edges = self._get_matching_edges(u, v)
            e_colors[color] = active_edges

        # 2. Aristas del Árbol (predecesores π)
        tree_edges = []
        active_pairs = [e[:2] for e in active_edges]
        for dst, src in state["pi"].items():
            if src is not None:
                matches = self._get_matching_edges(src, dst)
                if matches:
                    edge = matches[0]
                    # Solo añadir si no es la arista activa
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
        """Muestra el panel de control completo."""
        ui_header = []
        if self.show_selectors:
            row = [self.graph_drop] if self.graphs else []
            # Row including Source and Algorithm selectors
            ui_header.append(
                widgets.HBox(row + [self.source_drop, self.algo_drop], layout={"border": "none"})
            )
        else:
            # If show_selectors is False, we might still want to show the source selector
            # depending on the context, but for now we'll stick to the requested behavior.
            ui_header.append(
                widgets.HBox([self.source_drop, self.algo_drop], layout={"border": "none"})
            )

        # El desc_label está separado del output del plot
        # Quitamos bordes del VBox principal para evitar el cuadro externo
        main_box = widgets.VBox(
            ui_header + [self.step_slider, self.desc_label, self.viz_container],
            layout={"border": "none"},
        )
        display(main_box)


def launch_case(G_in=None, s_in=None, algo_name="Dijkstra", graphs=None):
    viz = AlgorithmVisualizer(
        graphs=graphs,
        G_default=G_in,
        s_default=s_in,
        algo_default=algo_name,
        show_selectors=(graphs is not None),
    )
    viz.display()


def launch_visualizer(graphs):
    launch_case(graphs=graphs)
