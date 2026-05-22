from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx


GRAPHML_PATH = Path("data/br101_colapsados_analise.graphml")
ASSETS_DIR = Path("assets")


def normalize_sizes(values: dict[str, float], minimum: float, maximum: float) -> list[float]:
    raw_values = list(values.values())
    low = min(raw_values)
    high = max(raw_values)

    if high == low:
        return [minimum for _ in raw_values]

    scale = maximum - minimum
    return [minimum + ((value - low) / (high - low)) * scale for value in raw_values]


def build_node_color_map(graph: nx.Graph) -> list[float]:
    return [float(graph.nodes[node]["kcore"]) for node in graph.nodes]


def draw_graph(
    graph: nx.Graph,
    positions: dict[str, tuple[float, float]],
    output_path: Path,
    title: str,
    highlight_top_betweenness: bool = True,
) -> None:
    degrees = {node: float(graph.nodes[node]["degree"]) for node in graph.nodes}
    node_order = list(graph.nodes)
    normalized_sizes = normalize_sizes(degrees, minimum=18, maximum=240)
    size_map = {node: size for node, size in zip(node_order, normalized_sizes, strict=True)}
    node_sizes = [size_map[node] for node in node_order]
    node_colors = build_node_color_map(graph)

    plt.figure(figsize=(14, 14))
    nx.draw_networkx_edges(graph, positions, edge_color="#BFC5CC", width=0.4, alpha=0.45)
    nodes = nx.draw_networkx_nodes(
        graph,
        positions,
        node_size=node_sizes,
        node_color=node_colors,
        cmap=plt.cm.plasma,
        linewidths=0,
        alpha=0.9,
    )

    if highlight_top_betweenness:
        top_nodes = sorted(
            graph.nodes,
            key=lambda node: float(graph.nodes[node]["betweenness"]),
            reverse=True,
        )[:10]
        nx.draw_networkx_nodes(
            graph,
            positions,
            nodelist=top_nodes,
            node_size=[max(90.0, size_map[node] * 1.3) for node in top_nodes],
            node_color="#D62828",
            edgecolors="white",
            linewidths=0.8,
        )

    plt.colorbar(nodes, label="K-Core")
    plt.title(title)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.close()


def main() -> None:
    ASSETS_DIR.mkdir(exist_ok=True)
    graph = nx.read_graphml(GRAPHML_PATH)

    geographic_positions = {
        node: (float(graph.nodes[node]["x"]), float(graph.nodes[node]["y"])) for node in graph.nodes
    }
    draw_graph(
        graph,
        geographic_positions,
        ASSETS_DIR / "gephi_preview_geografico.png",
        "Prévia geográfica do grafo colapsado",
    )

    try:
        structural_positions = nx.spring_layout(graph, seed=42, k=0.18, iterations=150)
    except ModuleNotFoundError:
        structural_positions = nx.random_layout(graph, seed=42)
    draw_graph(
        graph,
        structural_positions,
        ASSETS_DIR / "gephi_preview_estrutural.png",
        "Prévia estrutural do grafo colapsado",
    )

    filtered_nodes = [
        node
        for node in graph.nodes
        if float(graph.nodes[node]["degree"]) >= 8 or float(graph.nodes[node]["kcore"]) >= 6
    ]
    filtered_graph = graph.subgraph(filtered_nodes).copy()
    filtered_positions = {
        node: (float(filtered_graph.nodes[node]["x"]), float(filtered_graph.nodes[node]["y"]))
        for node in filtered_graph.nodes
    }
    draw_graph(
        filtered_graph,
        filtered_positions,
        ASSETS_DIR / "gephi_preview_filtro.png",
        "Prévia filtrada: grau >= 8 ou k-core >= 6",
    )

    print("Prévias exportadas em assets/")


if __name__ == "__main__":
    main()
