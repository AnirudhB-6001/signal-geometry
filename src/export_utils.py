# src/export_utils.py

import networkx as nx
import csv
import json

def export_signals_to_csv(signals, filename="signals.csv"):
    fields = ["id", "source", "entropy", "velocity", "impact", "route", "drift_score", "nsi_score"]
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for s in signals:
            writer.writerow({
                "id": s.id,
                "source": s.source,
                "entropy": s.entropy,
                "velocity": s.velocity,
                "impact": s.impact,
                "route": " → ".join(s.route),
                "drift_score": s.drift_score,
                "nsi_score": s.nsi_score
            })
    print(f"Signals exported to {filename}")

def export_nodes_to_csv(graph, power_scores, filename="nodes.csv"):
    fields = ["id", "type", "power_score"]
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for node, data in graph.nodes(data=True):
            writer.writerow({
                "id": node,
                "type": data.get("type", "unknown"),
                "power_score": power_scores.get(node, 0)
            })
    print(f"Nodes exported to {filename}")

def export_graph_to_json(graph, filename="graph.json"):
    data = nx.node_link_data(graph)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Graph structure exported to {filename}")