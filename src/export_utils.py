
import networkx as nx
import csv
import json
from typing import List, Dict

def export_signals_to_csv(signals, filename="signals.csv"):
    fields = [
        "id", "title", "subreddit", "source",           # Basic
        "entropy", "velocity", "impact",                # Core Metrics
        "route", "route_length",                        # Propagation Metrics
        "drift_score", "nsi_score",                     # Truth & Narrative
        "recursion_score", "recursive_depth",           # Feedback Loops
        "power_index", "seed_node"                      # Influence
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
                "velocity": round(getattr(s, "velocity", 0.0), 4),
                "impact": round(getattr(s, "impact", 0.0), 4),
                "route": " → ".join(getattr(s, "route", [])),
                "route_length": len(getattr(s, "route", [])),
                "drift_score": round(getattr(s, "drift_score", 0.0), 4),
                "nsi_score": round(getattr(s, "nsi_score", 0.0), 4),
                "recursion_score": round(getattr(s, "recursion_score", 0.0), 4),
                "recursive_depth": getattr(s, "recursive_depth", 0),
                "power_index": round(getattr(s, "power_index", 0.0), 4),
                "seed_node": getattr(s, "seed_node", "")
            })
    print(f"✅ Signals exported to {filename} with all metrics.")

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
    print(f"✅ Nodes exported to {filename}")

def export_graph_to_json(graph, filename="graph.json"):
    data = nx.node_link_data(graph)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Graph structure exported to {filename}")

def export_propagation_timeline(timeline: List[Dict], filename="timeline.csv"):
    with open(filename, "w", newline="") as csvfile:
        fieldnames = timeline[0].keys() if timeline else ["signal_id", "node", "arrival_time"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in timeline:
            writer.writerow(row)
    print(f"✅ Propagation timeline exported to {filename}")

import json

def export_co_occurrence_map(co_occurrence_map, filepath="co_occurrence_map.json"):
    try:
        with open(filepath, "w") as f:
            json.dump(co_occurrence_map, f, indent=2)
        print(f"✅ Co-occurrence map exported to {filepath}")
    except Exception as e:
        print(f"❌ Failed to export co-occurrence map: {e}")