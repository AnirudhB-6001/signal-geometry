# src/visual_stats.py

import matplotlib.pyplot as plt
from collections import defaultdict
from src.model import Signal

def plot_avg_entropy_by_subreddit(signals):
    subreddit_entropy = defaultdict(list)

    for s in signals:
        subreddit_entropy[s.source].append(s.entropy)

    avg_entropy = {k: sum(v)/len(v) for k, v in subreddit_entropy.items()}

    plt.figure(figsize=(7, 4))
    plt.bar(avg_entropy.keys(), avg_entropy.values(), color='crimson')
    plt.title("Average Entropy per Subreddit")
    plt.ylabel("Entropy")
    plt.xlabel("Subreddit")
    plt.tight_layout()
    plt.savefig("avg_entropy_by_subreddit.png")
    print("Saved: avg_entropy_by_subreddit.png")

def plot_avg_nsi_by_subreddit(signals):
    subreddit_nsi = defaultdict(list)

    for s in signals:
        if hasattr(s, "nsi_score"):
            subreddit_nsi[s.source].append(s.nsi_score)

    avg_nsi = {k: sum(v)/len(v) for k, v in subreddit_nsi.items()}

    plt.figure(figsize=(7, 4))
    plt.bar(avg_nsi.keys(), avg_nsi.values(), color='teal')
    plt.title("Average NSI per Subreddit")
    plt.ylabel("Narrative Stability Index")
    plt.xlabel("Subreddit")
    plt.tight_layout()
    plt.savefig("avg_nsi_by_subreddit.png")
    print("Saved: avg_nsi_by_subreddit.png")