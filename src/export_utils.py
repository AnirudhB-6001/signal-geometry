# src/export_utils.py

import networkx as nx
import csv
import json
from typing import List, Dict

def export_signals_to_csv(signals, filename="signals.csv"):
    fields = [
        "id", "title", "subreddit", "source", "entropy", "velocity", "impact",
        "route", "drift_score", "nsi_score", "recursion_score"
    ]
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for s in signals:
            writer.writerow({
                "id": s.id,
                "title": getattr(s, "title", ""),
                "subreddit": getattr(s, "subreddit", "unknown"),
                "source": s.source,
                "entropy": round(s.entropy, 4),
                "velocity": s.velocity,
                "impact": s.impact,
                "route": " → ".join(s.route),
                "drift_score": round(getattr(s, "drift_score", 0.0), 4),
                "nsi_score": round(getattr(s, "nsi_score", 0.0), 4),
                "recursion_score": round(getattr(s, "recursion_score", 0.0), 4)
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

def export_propagation_timeline(timeline: List[Dict], filename="timeline.csv"):
    import csv
    with open(filename, "w", newline="") as csvfile:
        # Dynamically detect all fieldnames from the first item
        fieldnames = timeline[0].keys() if timeline else ["signal_id", "node", "arrival_time"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in timeline:
            writer.writerow(row)