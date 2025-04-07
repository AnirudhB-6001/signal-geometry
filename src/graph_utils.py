
# src/graph_utils.py

import networkx as nx
from typing import List
from src.model import Node, Signal
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

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

            G.add_edge(source, target,
                       signal_id=signal.id,
                       velocity=signal.velocity,
                       entropy=signal.entropy,
                       is_recursive=signal.is_recursive if hasattr(signal, "is_recursive") else False)

    return G

def visualize_graph(G, recursion_signals=None, contradiction_pairs=None):
    import matplotlib.patches as mpatches

    pos = nx.spring_layout(G, seed=42)
    node_colors = []
    node_borders = []

    for node, data in G.nodes(data=True):
        node_type = data.get("type", "router")
        signal = data.get("signal")
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
        power_term = power_scores.get(signal.source, 1)
        nsi = entropy_term * drift_term * power_term
        signal.nsi_score = round(nsi * 10, 4)
        print(f"- {signal.id}: NSI = {signal.nsi_score} | Source = {signal.source}")

def visualize_structured_graph(G):
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from collections import defaultdict

    # Define y-layer positions
    layer_y = {
        "influencer": 2,
        "institution": 1.5,
        "platform": 1,
        "machine": 0.5,
        "router": 0
    }

    # Group nodes by type
    type_groups = defaultdict(list)
    for node, data in G.nodes(data=True):
        node_type = data.get("type", "router")
        type_groups[node_type].append(node)

    # Assign spaced horizontal x-positions
    pos = {}
    for node_type, y in layer_y.items():
        nodes = type_groups.get(node_type, [])
        count = len(nodes)
        for i, node in enumerate(nodes):
            x = i - count / 2  # center horizontally
            pos[node] = (x, y)

    # Node styling
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

    # Edge weights and colors
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

    # Plotting
    plt.figure(figsize=(12, 8))
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