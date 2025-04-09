# main.py

from src.news_collector import collect_signals_from_news
from src.seed_nodes import seed_nodes as nodes
from src.graph_utils import (
    build_graph,
    visualize_graph,
    visualize_structured_graph,
    compute_power_index,
    calculate_truth_drift,
    compute_narrative_stability_index,
    resolve_missing_route,
    load_co_occurrence_map,
    detect_cross_platform_bridges,
    reinforce_cross_platform_bridges  # ✅ NEW
)
from src.export_utils import (
    export_signals_to_csv,
    export_nodes_to_csv,
    export_graph_to_json,
    export_propagation_timeline,
    export_co_occurrence_map
)
from src.signal_collector import collect_signals_from_reddit
from src.twitter_collector import collect_signals_from_twitter
from src.visual_stats import (
    plot_avg_entropy_by_subreddit,
    plot_avg_nsi_by_subreddit
)
from src.recursion_utils import analyze_recursions, detect_recursion
from src.simulator import simulate_propagation
from src.co_occurrence import track_co_occurrence

import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime
import json

# 0. Prompt user for subreddits
input_str = input("Enter subreddits to scan (comma-separated): ")
subreddits_to_scan = [s.strip() for s in input_str.split(",") if s.strip()]

# 1. Collect signals
reddit_signals = []
if subreddits_to_scan:
    try:
        print("\n🔍 Collecting signals from Reddit...")
        reddit_signals = collect_signals_from_reddit(subreddits=subreddits_to_scan, limit=20)
    except Exception as e:
        print(f"⚠️ Reddit signal collection failed: {e}")
else:
    print("⚠️ No subreddits provided. Skipping Reddit.")

# 2. Collect from NewsAPI
input_topics = input("Enter news topics to scan (comma-separated, e.g., Ukraine, AI): ")
news_topics = [t.strip() for t in input_topics.split(",") if t.strip()]
news_signals = collect_signals_from_news(news_topics, limit=10)

# 3. Twitter
print("🔍 Collecting signals from Twitter...")
twitter_signals = collect_signals_from_twitter(limit=10)

# ✅ 4. Merge all
signals = reddit_signals + twitter_signals + news_signals
print(f"✅ Total signals collected: {len(signals)}")
if not signals:
    print("❌ No signals collected. Exiting.")
    exit()

# 4b. Track co-occurrence
print("🔎 Tracking co-occurrence relationships...")
co_occurrence_map = track_co_occurrence(signals)
export_co_occurrence_map(co_occurrence_map)

# ✅ Save updated map to JSON for memory-based enrichment
with open("co_occurrence_map.json", "w") as f:
    json.dump(co_occurrence_map, f, indent=2)

# 4c. Auto-resolve missing or short routes
print("🧠 Enriching routes using co-occurrence and platform memory...")
memory = load_co_occurrence_map()
transition_map, bridge_nodes = detect_cross_platform_bridges(signals, nodes)

for signal in signals:
    if not signal.route or len(signal.route) <= 1:
        old_id = signal.id
        resolve_missing_route(signal, memory, transition_map, bridge_nodes)
        reinforce_cross_platform_bridges(signal, transition_map, bridge_nodes)  # ✅ New
        if signal.route and len(signal.route) > 1:
            print(f"⚙️ Final enriched route for {old_id} → {signal.route}")
        else:
            print(f"❌ Still incomplete: {old_id}")

# 5. Build graph
graph = build_graph(nodes, signals)
print("✅ Influence graph constructed.")
print("📊 Nodes:", graph.nodes(data=True))
print("📊 Edges:", graph.edges(data=True))

# 6. Detect feedback loops
def detect_loops(graph):
    loops = list(nx.simple_cycles(graph))
    print("\n🔁 Feedback loops detected:")
    for loop in sorted(loops, key=lambda l: l[0]):
        print(" → ".join(loop))

detect_loops(graph)

# 7. Recursion detection
recursive_nodes = detect_recursion(signals)
analyze_recursions(signals)

# 8. Graph visualizations
visualize_graph(graph, recursion_signals=recursive_nodes)
visualize_structured_graph(graph)

# 9. Entropy chart
def plot_entropy_over_time(signals):
    try:
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

    except Exception as e:
        print(f"⚠️ Failed to plot entropy over time: {e}")

plot_entropy_over_time(signals)

# 10. Power & narrative analysis
power_scores = compute_power_index(graph)
calculate_truth_drift(signals)
# ⚙️ Patch: Reassign Reddit signal source to actual final node in route
for signal in signals:
    if signal.source == "reddit" and signal.route and len(signal.route) > 1:
        old_source = signal.source
        signal.source = signal.route[-1]
        print(f"🔄 Reassigned Reddit signal source: {signal.id} → {signal.source}")
compute_narrative_stability_index(graph, signals, power_scores)

# 11. Subreddit profile charts
plot_avg_entropy_by_subreddit(signals)
plot_avg_nsi_by_subreddit(signals)

# 12. Export outputs
export_signals_to_csv(signals)
export_nodes_to_csv(graph, power_scores)
export_graph_to_json(graph)

# 13. Propagation simulation
timeline = simulate_propagation(signals)
export_propagation_timeline(timeline)
print("✅ Propagation timeline exported to timeline.csv")