# src/graph_utils.py

import networkx as nx
from typing import List
from src.model import Node, Signal
import matplotlib.pyplot as plt

def build_graph(nodes: List[Node], signals: List[Signal]) -> nx.DiGraph:
    G = nx.DiGraph()

    for node in nodes:
        G.add_node(node.id, type=node.type, **(node.metadata or {}))

    for signal in signals:
        # Add signal route as directed edges
        for i in range(len(signal.route) - 1):
            source = signal.route[i]
            target = signal.route[i + 1]
            G.add_edge(source, target, signal_id=signal.id, velocity=signal.velocity, entropy=signal.entropy)

    return G

def visualize_graph(G):
    pos = nx.spring_layout(G, seed=42)  # Consistent layout
    
    # Get node colors by type
    node_colors = []
    for node, data in G.nodes(data=True):
        if data['type'] == 'influencer':
            node_colors.append('orange')
        elif data['type'] == 'institution':
            node_colors.append('skyblue')
        elif data['type'] == 'platform':
            node_colors.append('lightgreen')
        else:
            node_colors.append('gray')

    # Get edge weights (based on velocity) and colors (based on entropy)
    edge_weights = []
    edge_colors = []
    for u, v, data in G.edges(data=True):
        edge_weights.append(data['velocity'] * 3)  # scale for visibility
        entropy = data.get('entropy', 0.5)
        # map entropy to color
        if entropy < 0.3:
            edge_colors.append('green')  # stable
        elif entropy < 0.7:
            edge_colors.append('orange')  # mixed
        else:
            edge_colors.append('red')  # volatile

    # Draw
    plt.figure(figsize=(10, 7))
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=800)
    nx.draw_networkx_edges(G, pos, width=edge_weights, edge_color=edge_colors, arrows=True)
    nx.draw_networkx_labels(G, pos, font_size=9, font_family="sans-serif")

    # Legend
    import matplotlib.patches as mpatches
    patches = [
        mpatches.Patch(color='orange', label='Influencer'),
        mpatches.Patch(color='skyblue', label='Institution'),
        mpatches.Patch(color='lightgreen', label='Platform'),
        mpatches.Patch(color='gray', label='Router'),
        mpatches.Patch(color='green', label='Low Entropy'),
        mpatches.Patch(color='orange', label='Mid Entropy'),
        mpatches.Patch(color='red', label='High Entropy')
    ]
    plt.legend(handles=patches, loc='upper left')
    plt.title("Signal Geometry: Influence Graph")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig("influence_graph.png")
    print("Graph saved as influence_graph.png")

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

        # Drift is a synthetic score: more nodes + more entropy = more drift
        drift = round(entropy * (route_len - 1) * velocity, 4)
        signal.drift_score = drift

        print(f"- {signal.id}: Drift = {drift} | Entropy = {entropy} | Route Length = {route_len}")

def compute_narrative_stability_index(graph, signals, power_scores):
    print("\nNarrative Stability Index (NSI):")

    for signal in signals:
        entropy_term = 1 - signal.entropy
        drift_term = 1 / (1 + signal.drift_score)
        power_term = power_scores.get(signal.source, 1)

        # Raw NSI formula
        nsi = entropy_term * drift_term * power_term
        signal.nsi_score = round(nsi * 10, 4)  # Scaled to 0-10

        print(f"- {signal.id}: NSI = {signal.nsi_score} | Source = {signal.source}")
