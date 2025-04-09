from collections import defaultdict
from src.model import Signal
from src.seed_nodes import seed_nodes


def track_co_occurrence(signals: list[Signal]) -> dict:
    raw_counts = defaultdict(lambda: defaultdict(int))
    context_totals = defaultdict(int)

    # Valid influencer + institution nodes
    valid_nodes = [node.id for node in seed_nodes if node.type in ("influencer", "institution")]

    for signal in signals:
        text = f"{signal.title} {signal.content}".lower()
        present_nodes = set()

        for node_id in valid_nodes:
            if node_id.lower() in text:
                present_nodes.add(node_id)

        # Increase pairwise counts
        present_nodes = list(present_nodes)
        context_totals[signal.id] = len(present_nodes)

        for i in range(len(present_nodes)):
            for j in range(i + 1, len(present_nodes)):
                a, b = present_nodes[i], present_nodes[j]
                raw_counts[a][b] += 1
                raw_counts[b][a] += 1

    # Compute weighted memory map
    weighted_memory = {}
    for a, neighbors in raw_counts.items():
        weighted_memory[a] = {}
        max_count = max(neighbors.values()) if neighbors else 1
        for b, count in neighbors.items():
            weight = count / max_count
            weighted_memory[a][b] = {
                "count": count,
                "weight": round(weight, 4)
            }

    return weighted_memory


# === New: Decay-Aware Lookup ===

def decay_weighted_lookup(text, co_occurrence_map, decay=0.85):
    """
    Returns a list of nodes weighted by co-occurrence strength with decay applied.
    """
    weighted_scores = defaultdict(float)
    words = text.lower().split()

    for word in words:
        if word in co_occurrence_map:
            for target, entry in co_occurrence_map[word].items():
                weight = entry.get("weight", 0)
                weighted_scores[target] += weight * decay

    sorted_nodes = sorted(weighted_scores.items(), key=lambda x: -x[1])
    return [node for node, _ in sorted_nodes]