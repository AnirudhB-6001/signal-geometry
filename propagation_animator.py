# src/propagation_animator.py

import json
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.animation as animation
import pandas as pd
from datetime import datetime
from pathlib import Path

# Load graph
with open("graph.json", "r") as f:
    data = json.load(f)
G = nx.node_link_graph(data)

# Load and preprocess timeline
df = pd.read_csv("timeline.csv")
df["parsed_time"] = pd.to_datetime(df["arrival_time"])
df = df.sort_values("parsed_time")

# Map timestamps to time steps
time_step_map = {t: i for i, t in enumerate(sorted(df["parsed_time"].unique()))}
df["time_step"] = df["parsed_time"].map(time_step_map)

# Build arrival lookup
arrival_time = {}
for _, row in df.iterrows():
    step = row["time_step"]
    arrival_time.setdefault(step, []).append(row["node"])

# Layout logic
type_colors = {
    "influencer": "#ff5733",
    "institution": "#33c1ff",
    "machine": "#8e44ad",
    "platform": "#27ae60",
    "router": "#7f8c8d"
}
layer_y = {
    "influencer": 3,
    "institution": 2,
    "router": 1,
    "platform": 0,
    "machine": -1
}
pos = {}
for i, node in enumerate(G.nodes):
    t = G.nodes[node].get("type", "router")
    pos[node] = (i % 10, layer_y.get(t, 1))

# Animation
fig, ax = plt.subplots(figsize=(12, 8), dpi=200)
plt.axis("off")

def update(frame):
    ax.clear()
    plt.title("Signal Propagation Over Time", fontsize=14)
    plt.axis("off")
    
    highlighted = set()
    for t in range(frame + 1):
        highlighted.update(arrival_time.get(t, []))

    node_colors = [
        "#e74c3c" if node in highlighted else "#d3d3d3"
        for node in G.nodes
    ]

    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=500, edgecolors="black", ax=ax)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=8)

    active_edges = []
    for t in range(frame + 1):
        for node in arrival_time.get(t, []):
            active_edges.extend([(src, node) for src, _ in G.in_edges(node)])
    
    nx.draw_networkx_edges(G, pos, edgelist=G.edges, edge_color="#c0c0c0", alpha=0.2, arrows=True, ax=ax)
    nx.draw_networkx_edges(G, pos, edgelist=active_edges, edge_color="#3498db", width=2, arrows=True, ax=ax)

ani = animation.FuncAnimation(fig, update, frames=max(arrival_time.keys()) + 1, interval=1000, repeat=False)

ani.save("propagation_highdef.gif", writer="pillow")
print("✅ Saved: propagation_highdef.gif")