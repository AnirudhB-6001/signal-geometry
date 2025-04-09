# src/graph_utils.py

import networkx as nx
from typing import List
from src.model import Node, Signal
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import json
from collections import defaultdict
from src.co_occurrence import decay_weighted_lookup

def build_graph(nodes: List[Node], signals: List[Signal]) -> nx.DiGraph:
    G = nx.DiGraph()
    for node in nodes:
        G.add_node(node.id, type=node.type, **(node.metadata or {}))

    for signal in signals:
        for i in range(len(signal.route) - 1):
            source = signal.route[i]
            target = signal.route[i + 1]

            if source not in G.nodes:
                G.add_node(source, type='router')
            if target not in G.nodes:
                G.add_node(target, type='router')

            if i == 0:
                G.nodes[source]["signal"] = {
                    "id": signal.id,
                    "entropy": signal.entropy,
                    "title": getattr(signal, "title", ""),
                    "subreddit": getattr(signal, "subreddit", ""),
                }

            G.add_edge(
                source,
                target,
                signal_id=signal.id,
                velocity=signal.velocity,
                entropy=signal.entropy,
                is_recursive=signal.is_recursive if hasattr(signal, "is_recursive") else False
            )

    return G


def visualize_graph(G, recursion_signals=None, contradiction_pairs=None):
    pos = nx.spring_layout(G, seed=42)
    node_colors = []
    node_borders = []

    for node, data in G.nodes(data=True):
        node_type = data.get("type", "router")
        is_recursive = recursion_signals and node in recursion_signals

        color = (
            "orange" if node_type == "influencer" else
            "skyblue" if node_type == "institution" else
            "lightgreen" if node_type == "platform" else
            "violet" if node_type == "machine" else
            "gray"
        )

        node_colors.append(color)
        node_borders.append("black" if is_recursive else "none")

    edge_weights = []
    edge_colors = []
    for u, v, data in G.edges(data=True):
        edge_weights.append(data["velocity"] * 3)
        entropy = data.get("entropy", 0.5)
        is_recursive = data.get("is_recursive", False)

        edge_color = (
            "purple" if is_recursive else
            "green" if entropy < 0.3 else
            "orange" if entropy < 0.7 else
            "red"
        )
        edge_colors.append(edge_color)

    plt.figure(figsize=(10, 7))
    nx.draw_networkx_nodes(G, pos,
                           node_color=node_colors,
                           node_size=800,
                           edgecolors=node_borders,
                           linewidths=2)
    nx.draw_networkx_edges(G, pos,
                           width=edge_weights,
                           edge_color=edge_colors,
                           arrows=True)
    nx.draw_networkx_labels(G, pos, font_size=9, font_family="sans-serif")

    legend = [
        mpatches.Patch(color="orange", label="Influencer"),
        mpatches.Patch(color="skyblue", label="Institution"),
        mpatches.Patch(color="lightgreen", label="Platform"),
        mpatches.Patch(color="violet", label="Machine"),
        mpatches.Patch(color="gray", label="Router"),
        mpatches.Patch(facecolor="white", edgecolor="black", label="Recursive Node"),
        mpatches.Patch(color="purple", label="Recursive Edge"),
        mpatches.Patch(color="green", label="Low Entropy Edge"),
        mpatches.Patch(color="orange", label="Mid Entropy Edge"),
        mpatches.Patch(color="red", label="High Entropy Edge"),
    ]
    plt.legend(handles=legend, loc="upper left")
    plt.title("Signal Geometry: Influence Graph (Recursion Enhanced)")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("influence_graph.png")
    print("Graph saved as influence_graph.png (recursion enhanced)")


def compute_power_index(graph):
    import operator
    print("\nNode Power Index (Influence Ranking):")

    in_deg = dict(graph.in_degree())
    out_deg = dict(graph.out_degree())
    between = nx.betweenness_centrality(graph)
    close = nx.closeness_centrality(graph)

    print("\n🔍 DEGREE DIAGNOSTICS:")
    for node in graph.nodes():
        print(f"{node}: in={in_deg.get(node, 0)}, out={out_deg.get(node, 0)}, between={round(between.get(node, 0), 4)}, close={round(close.get(node, 0), 4)}")

    scores = {}
    for node in graph.nodes():
        score = (
            in_deg.get(node, 0) * 1.0 +
            out_deg.get(node, 0) * 1.2 +
            between.get(node, 0) * 2.0 +
            close.get(node, 0) * 1.5
        )
        scores[node] = round(score, 4)

    ranked = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)

    for i, (node, score) in enumerate(ranked, 1):
        print(f"{i}. {node}: {score}")

    return scores


def calculate_truth_drift(signals):
    print("\nTruth Drift Report:")
    for signal in signals:
        route_len = len(signal.route)
        entropy = signal.entropy
        velocity = signal.velocity
        drift = round(entropy * (route_len - 1) * velocity, 4)
        signal.drift_score = drift
        print(f"- {signal.id}: Drift = {drift} | Entropy = {entropy} | Route Length = {route_len}")


def compute_narrative_stability_index(graph, signals, power_scores):
    print("\nNarrative Stability Index (NSI):")
    for signal in signals:
        entropy_term = 1 - signal.entropy
        drift_term = 1 / (1 + signal.drift_score)
        power_term = power_scores.get(signal.source, 0.0)  # Use 0.0 if node isn't scored

        signal.nsi_score = round(entropy_term * drift_term * power_term * 10, 4)
        print(f"- {signal.id}: NSI = {signal.nsi_score} | Source = {signal.source}")


def visualize_structured_graph(G):
    from collections import defaultdict
    layer_y = {
        "influencer": 2,
        "institution": 1.5,
        "platform": 1,
        "machine": 0.5,
        "router": 0
    }
    type_groups = defaultdict(list)
    for node, data in G.nodes(data=True):
        node_type = data.get("type", "router")
        type_groups[node_type].append(node)
    pos = {}
    for node_type, y in layer_y.items():
        nodes = type_groups.get(node_type, [])
        count = len(nodes)
        for i, node in enumerate(nodes):
            x = i - count / 2
            pos[node] = (x, y)
    node_colors = []
    node_borders = []
    for node, data in G.nodes(data=True):
        node_type = data.get("type", "router")
        color = (
            "orange" if node_type == "influencer" else
            "skyblue" if node_type == "institution" else
            "lightgreen" if node_type == "platform" else
            "violet" if node_type == "machine" else
            "gray"
        )
        node_colors.append(color)
        node_borders.append("black")
    edge_weights = [data.get("velocity", 0.5) * 3 for _, _, data in G.edges(data=True)]
    edge_colors = []
    for _, _, data in G.edges(data=True):
        entropy = data.get("entropy", 0.5)
        is_recursive = data.get("is_recursive", False)
        if is_recursive:
            edge_colors.append("purple")
        elif entropy < 0.3:
            edge_colors.append("green")
        elif entropy < 0.7:
            edge_colors.append("orange")
        else:
            edge_colors.append("red")
    plt.figure(figsize=(12, 8))
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=800, edgecolors=node_borders, linewidths=2)
    nx.draw_networkx_edges(G, pos, width=edge_weights, edge_color=edge_colors, arrows=True)
    nx.draw_networkx_labels(G, pos, font_size=9, font_family="sans-serif")
    legend = [
        mpatches.Patch(color="orange", label="Influencer"),
        mpatches.Patch(color="skyblue", label="Institution"),
        mpatches.Patch(color="lightgreen", label="Platform"),
        mpatches.Patch(color="violet", label="Machine"),
        mpatches.Patch(color="gray", label="Router"),
        mpatches.Patch(color="purple", label="Recursive Edge"),
        mpatches.Patch(color="green", label="Low Entropy Edge"),
        mpatches.Patch(color="orange", label="Mid Entropy Edge"),
        mpatches.Patch(color="red", label="High Entropy Edge"),
    ]
    plt.legend(handles=legend, loc="upper left")
    plt.title("Structured Signal Propagation Graph")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("influence_graph_structured.png")
    print("📌 Structured graph saved as influence_graph_structured.png")

# === Route Enrichment Logic (Weighted Path Recall + Cross-Platform Memory) ===
def load_co_occurrence_map(path='co_occurrence_map.json'):
    with open(path, 'r') as f:
        return json.load(f)


def infer_route_from_memory(signal, co_map):
    title_content = (signal.title + ' ' + signal.content).lower()
    inferred = decay_weighted_lookup(title_content, co_map)
    if inferred:
        return ['user_1', 'user_2'] + inferred[:1]  # prioritize top weighted node
    return []


def resolve_cross_platform_hop(signal, transition_map, bridge_nodes):
    if not signal.route or len(signal.route) < 2:
        return signal

    src_platform = signal.source.lower()
    candidate_jumps = [(a, b) for (a, b) in transition_map.keys() if a == src_platform]

    if not candidate_jumps:
        return signal

    # Pick most common transition
    most_common_jump = max(candidate_jumps, key=lambda k: transition_map[k])
    _, target_platform = most_common_jump

    # Add bridge node if exists
    bridge = next((b for b in bridge_nodes if b not in signal.route), None)
    if bridge:
        signal.route.append(bridge)
    signal.route.append(target_platform)

    return signal


def resolve_missing_route(signal, co_map, transition_map=None, bridge_nodes=None):
    if not signal.route or len(signal.route) <= 1:
        enriched_route = infer_route_from_memory(signal, co_map)
        if enriched_route:
            signal.route = enriched_route

    if transition_map and bridge_nodes:
        signal = resolve_cross_platform_hop(signal, transition_map, bridge_nodes)

    return signal


def detect_cross_platform_bridges(signals, nodes):
    platform_nodes = {node.id: node.metadata.get("region", "") for node in nodes if node.type == "platform"}
    platform_routes = defaultdict(list)
    bridge_nodes = set()
    transition_map = defaultdict(int)

    for signal in signals:
        platforms_in_route = []
        for node_id in signal.route:
            if node_id in platform_nodes:
                platforms_in_route.append(node_id)

        for i in range(len(platforms_in_route) - 1):
            src = platforms_in_route[i]
            dst = platforms_in_route[i + 1]
            if src != dst:
                transition_map[(src, dst)] += 1

        for i in range(len(signal.route) - 2):
            if signal.route[i] in platform_nodes and signal.route[i + 2] in platform_nodes:
                bridge_nodes.add(signal.route[i + 1])

    print("\n🌉 Cross-Platform Transitions:")
    for (src, dst), count in transition_map.items():
        print(f"{src} → {dst}: {count} times")

    print("\n🔗 Bridge Nodes Across Platforms:")
    for node in bridge_nodes:
        print(f"- {node}")

    return transition_map, bridge_nodes

def reinforce_cross_platform_bridges(signal, transition_map, bridge_nodes):
    # Check if signal jumps platforms
    route = signal.route or []
    if len(route) < 2:
        return signal

    # Find known platform transitions in this route
    enriched = False
    for i in range(len(route) - 1):
        src = route[i]
        dst = route[i + 1]

        if (src, dst) in transition_map:
            # If there's no bridge in between, insert one from the known bridge list
            if i + 2 >= len(route) or route[i + 2] not in bridge_nodes:
                for bridge in bridge_nodes:
                    # Insert the bridge node if it hasn't already been used
                    if bridge not in route:
                        signal.route = route[:i + 1] + [bridge] + route[i + 1:]
                        enriched = True
                        break
            if enriched:
                break

    return signal