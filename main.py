from src.news_collector import collect_signals_from_news
from src.seed_nodes import seed_nodes as nodes
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
    export_graph_to_json,
    export_propagation_timeline
)
from src.signal_collector import collect_signals_from_reddit
from src.twitter_collector import collect_signals_from_twitter
from src.visual_stats import (
    plot_avg_entropy_by_subreddit,
    plot_avg_nsi_by_subreddit
)
from src.recursion_utils import analyze_recursions, detect_recursion
from src.simulator import simulate_propagation

import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime

# 0. Prompt user for subreddits
input_str = input("Enter subreddits to scan (comma-separated): ")
subreddits_to_scan = [s.strip() for s in input_str.split(",") if s.strip()]
if not subreddits_to_scan:
    print("No subreddits provided. Exiting.")
    exit()

# 1. Collect signals
print("\n🔍 Collecting signals from Reddit...")
reddit_signals = collect_signals_from_reddit(subreddits=subreddits_to_scan, limit=20)

# 2.5 Collect signals from NewsAPI (for selected topics)
input_topics = input("Enter news topics to scan (comma-separated, e.g., Ukraine, AI): ")
news_topics = [t.strip() for t in input_topics.split(",") if t.strip()]
news_signals = collect_signals_from_news(news_topics, limit=10)

print("🔍 Collecting signals from Twitter...")
twitter_signals = collect_signals_from_twitter(limit=10)

# ✅ 2. Merge all signals
signals = reddit_signals + twitter_signals + news_signals
print(f"✅ Total signals collected: {len(signals)}")

# 3. Build influence graph
graph = build_graph(nodes, signals)
print("✅ Influence graph constructed.")

# 4. Print graph info
print("📊 Nodes:", graph.nodes(data=True))
print("📊 Edges:", graph.edges(data=True))

# 5. Detect feedback loops
def detect_loops(graph):
    loops = list(nx.simple_cycles(graph))
    print("\n🔁 Feedback loops detected:")
    for loop in sorted(loops, key=lambda l: l[0]):
        print(" → ".join(loop))

detect_loops(graph)

# 6. Recursion detection
recursive_nodes = detect_recursion(signals)
analyze_recursions(signals)

# 7. Visualize graph with recursion coloring
visualize_graph(graph, recursion_signals=recursive_nodes)

# 8. Plot entropy over time
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
    print("📈 Entropy trend saved as entropy_over_time.png")

plot_entropy_over_time(signals)

# 9. Power & narrative analysis
power_scores = compute_power_index(graph)
calculate_truth_drift(signals)
compute_narrative_stability_index(graph, signals, power_scores)

# 10. Subreddit profile charts
plot_avg_entropy_by_subreddit(signals)
plot_avg_nsi_by_subreddit(signals)

# 11. Export core outputs
export_signals_to_csv(signals)
export_nodes_to_csv(graph, power_scores)
export_graph_to_json(graph)

# 12. Simulate signal propagation and export timeline
timeline = simulate_propagation(signals)
export_propagation_timeline(timeline)
print("✅ Propagation timeline exported to timeline.csv")