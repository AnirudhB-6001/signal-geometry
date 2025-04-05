# main.py

from src.model import Node, Signal
from src.graph_utils import (
    build_graph,
    visualize_graph,
    compute_power_index,
    calculate_truth_drift,
    compute_narrative_stability_index
)
from src.export_utils import (
    export_signals_to_csv,
    export_nodes_to_csv,
    export_graph_to_json
)
from src.signal_collector import collect_signals_from_reddit
from src.visual_stats import (
    plot_avg_entropy_by_subreddit,
    plot_avg_nsi_by_subreddit
)

import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime

# 0. Prompt user for subreddits
input_str = input("Enter subreddits to scan (comma-separated): ")
subreddits_to_scan = [s.strip() for s in input_str.split(",") if s.strip()]
if not subreddits_to_scan:
    print("No subreddits provided. Exiting.")
    exit()

# 1. Define graph nodes
nodes = [
    Node(id="elon_musk", type="influencer", metadata={"platform": "Twitter"}),
    Node(id="nyt", type="institution", metadata={"category": "media"}),
    Node(id="user_1", type="router"),
    Node(id="user_2", type="router"),
    Node(id="reddit_thread", type="platform", metadata={"category": "social"}),
    Node(id="think_tank", type="institution", metadata={"category": "policy"})
]

# 2. Collect signals
signals = collect_signals_from_reddit(subreddits=subreddits_to_scan, limit=20)

# 3. Build influence graph
graph = build_graph(nodes, signals)

# 4. Print graph stats
print("Nodes:", graph.nodes(data=True))
print("Edges:", graph.edges(data=True))

# 5. Feedback loop detection
def detect_loops(graph):
    loops = list(nx.simple_cycles(graph))
    print("\nFeedback loops detected:")
    for loop in sorted(loops, key=lambda l: l[0]):
        print(" → ".join(loop))

detect_loops(graph)

# 6. Visualize influence graph
visualize_graph(graph)

# 7. Entropy over time plot
def plot_entropy_over_time(signals):
    signals_sorted = sorted(signals, key=lambda s: s.timestamp)
    times = [datetime.strptime(s.timestamp, "%Y-%m-%dT%H:%M:%SZ") for s in signals_sorted]
    entropy_vals = [s.entropy for s in signals_sorted]

    plt.figure(figsize=(8, 4))
    plt.plot(times, entropy_vals, marker='o', linestyle='-', color='blue')
    plt.title("Signal Entropy Over Time")
    plt.xlabel("Timestamp")
    plt.ylabel("Entropy")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("entropy_over_time.png")
    print("Entropy trend saved as entropy_over_time.png")

plot_entropy_over_time(signals)

# 8. Power + drift + NSI analysis
power_scores = compute_power_index(graph)
calculate_truth_drift(signals)
compute_narrative_stability_index(graph, signals, power_scores)

# 9. Subreddit profiling charts
plot_avg_entropy_by_subreddit(signals)
plot_avg_nsi_by_subreddit(signals)

# 10. Export results
export_signals_to_csv(signals)
export_nodes_to_csv(graph, power_scores)
export_graph_to_json(graph)