from __future__ import annotations

import json
from pathlib import Path

import networkx as nx
import osmnx as ox
from shapely.geometry import LineString, Polygon
from shapely.ops import linemerge


COORDS = [
    (-5.918514, -35.277890),
    (-5.973278, -35.273041),
    (-5.973449, -35.188755),
    (-5.959791, -35.130390),
    (-5.874716, -35.167426),
    (-5.838087, -35.213432),
    (-5.883595, -35.265617),
]

DATA_DIR = Path("data")
GRAPHML_PATH = DATA_DIR / "br101_colapsados_analise.graphml"
SUMMARY_PATH = DATA_DIR / "br101_colapsados_resumo.json"


def build_boundary_polygon() -> Polygon:
    polygon_coords = [(lon, lat) for lat, lon in COORDS]
    return Polygon(polygon_coords)


def build_collapsed_graph() -> nx.MultiDiGraph:
    ox.settings.use_cache = True
    base_graph = ox.graph_from_polygon(build_boundary_polygon(), network_type="drive")

    collapsed_graph = nx.MultiDiGraph()
    edges_by_name: dict[str, list[tuple[int, int, LineString]]] = {}

    for u, v, _, data in base_graph.edges(keys=True, data=True):
        name = data.get("name")
        if name is None:
            continue

        if isinstance(name, list):
            street_name = " | ".join(sorted(map(str, name)))
        else:
            street_name = str(name)

        geometry = data.get("geometry")
        if geometry is None:
            geometry = LineString(
                [
                    (base_graph.nodes[u]["x"], base_graph.nodes[u]["y"]),
                    (base_graph.nodes[v]["x"], base_graph.nodes[v]["y"]),
                ]
            )

        edges_by_name.setdefault(street_name, []).append((u, v, geometry))

    visited = set()
    node_lookup: dict[int, set[int]] = {}
    component_id = 0

    for street_name, same_edges in edges_by_name.items():
        subgraph = nx.Graph()
        subgraph.add_edges_from(
            (a, b, {"geometry": geometry}) for a, b, geometry in same_edges
        )

        for component in nx.connected_components(subgraph):
            edges = list(subgraph.subgraph(component).edges(data=True))
            if not edges:
                continue

            first_edge = frozenset((edges[0][0], edges[0][1]))
            if first_edge in visited:
                continue

            component_id += 1
            merged_geometry = linemerge([edge_data["geometry"] for _, _, edge_data in edges])
            centroid = merged_geometry.centroid

            collapsed_graph.add_node(
                component_id,
                street_name=street_name,
                geometry=merged_geometry,
                original_nodes=",".join(map(str, sorted(component))),
                x=float(centroid.x),
                y=float(centroid.y),
            )

            for a, b, _ in edges:
                visited.add(frozenset((a, b)))

            for original_node in component:
                node_lookup.setdefault(original_node, set()).add(component_id)

    edge_id = 0
    for collapsed_nodes in node_lookup.values():
        nodes = sorted(collapsed_nodes)
        for index, source in enumerate(nodes):
            for target in nodes[index + 1 :]:
                if source == target or collapsed_graph.has_edge(source, target):
                    continue

                edge_id += 1
                line = LineString(
                    [
                        (collapsed_graph.nodes[source]["x"], collapsed_graph.nodes[source]["y"]),
                        (collapsed_graph.nodes[target]["x"], collapsed_graph.nodes[target]["y"]),
                    ]
                )
                collapsed_graph.add_edge(
                    source,
                    target,
                    key=edge_id,
                    geometry=line,
                    length=line.length,
                )

    collapsed_graph.graph["crs"] = base_graph.graph["crs"]
    return collapsed_graph


def serialize_graph(graph: nx.Graph) -> nx.Graph:
    serialized = graph.copy()

    for _, _, data in serialized.edges(data=True):
        for key, value in list(data.items()):
            if key == "geometry" and hasattr(value, "wkt"):
                data[key] = value.wkt
            elif isinstance(value, list):
                data[key] = ", ".join(map(str, value))

    for _, data in serialized.nodes(data=True):
        for key, value in list(data.items()):
            if key == "geometry" and hasattr(value, "wkt"):
                data[key] = value.wkt
            elif isinstance(value, list):
                data[key] = ", ".join(map(str, value))

    return serialized


def top_named_items(values: dict[int, float], graph: nx.Graph, limit: int = 10) -> list[dict[str, float | str]]:
    top_items = sorted(values.items(), key=lambda item: item[1], reverse=True)[:limit]
    return [
        {
            "node": node_id,
            "street_name": str(graph.nodes[node_id].get("street_name", node_id)),
            "value": float(value),
        }
        for node_id, value in top_items
    ]


def distribution(values: dict[int, int]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in values.values():
        counts[str(value)] = counts.get(str(value), 0) + 1
    return dict(sorted(counts.items(), key=lambda item: int(item[0])))


def build_summary(graph: nx.Graph) -> dict[str, object]:
    degree = dict(graph.degree())
    betweenness = nx.betweenness_centrality(graph, normalized=True)
    closeness = nx.closeness_centrality(graph)

    simple_graph = nx.Graph(graph)
    simple_graph.remove_edges_from(nx.selfloop_edges(simple_graph))
    kcore = nx.core_number(simple_graph)

    nx.set_node_attributes(graph, degree, "degree")
    nx.set_node_attributes(graph, betweenness, "betweenness")
    nx.set_node_attributes(graph, closeness, "closeness")
    nx.set_node_attributes(graph, kcore, "kcore")

    top_degree_ids = {item["node"] for item in top_named_items(degree, graph)}
    top_betweenness_ids = {item["node"] for item in top_named_items(betweenness, graph)}
    overlap = sorted(top_degree_ids & top_betweenness_ids)

    degree_threshold_index = max(int(len(degree) * 0.9) - 1, 0)
    degree_values_sorted = sorted(degree.values())
    top_10_percent_degree_threshold = degree_values_sorted[degree_threshold_index]

    high_k = 6 if max(kcore.values()) >= 6 else max(kcore.values())
    high_k_count = sum(1 for value in kcore.values() if value >= high_k)

    return {
        "node_count": graph.number_of_nodes(),
        "edge_count": graph.number_of_edges(),
        "max_degree": max(degree.values()),
        "avg_degree": sum(degree.values()) / len(degree),
        "max_kcore": max(kcore.values()),
        "top_degree": top_named_items(degree, graph),
        "top_betweenness": top_named_items(betweenness, graph),
        "top_closeness": top_named_items(closeness, graph),
        "kcore_distribution": distribution(kcore),
        "top_degree_top_betweenness_overlap": [
            {
                "node": node_id,
                "street_name": str(graph.nodes[node_id].get("street_name", node_id)),
            }
            for node_id in overlap
        ],
        "top_10_percent_degree_threshold": top_10_percent_degree_threshold,
        "high_k_suggestion": {
            "k": high_k,
            "node_count": high_k_count,
        },
    }


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)

    collapsed_graph = build_collapsed_graph()
    undirected_graph = collapsed_graph.to_undirected()
    summary = build_summary(undirected_graph)

    serialized = serialize_graph(undirected_graph)
    nx.write_graphml(serialized, GRAPHML_PATH)
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")

    print(f"Grafo exportado para {GRAPHML_PATH}")
    print(f"Resumo exportado para {SUMMARY_PATH}")
    print(
        "Nós: {node_count} | Arestas: {edge_count} | K-core máximo: {max_kcore}".format(
            **summary
        )
    )


if __name__ == "__main__":
    main()
