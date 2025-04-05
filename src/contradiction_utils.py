# src/contradiction_utils.py

from src.model import Signal
from itertools import combinations

# Simple keyword list indicating potential contradiction or refutation
CONTRADICTION_KEYWORDS = [
    "not", "no", "never", "false", "fake", "hoax", "debunked", "refuted", "misleading", "incorrect"
]

def is_contradictory(content_a: str, content_b: str) -> bool:
    """
    Heuristic: If one mentions a keyword and the other doesn't, flag as contradiction.
    You can later improve this using NLP-based stance detection.
    """
    a = content_a.lower()
    b = content_b.lower()
    has_contra_a = any(word in a for word in CONTRADICTION_KEYWORDS)
    has_contra_b = any(word in b for word in CONTRADICTION_KEYWORDS)
    return has_contra_a != has_contra_b

def detect_contradictions(signals: list[Signal]) -> list[tuple[Signal, Signal]]:
    contradictory_pairs = []
    # Pairwise comparison
    for s1, s2 in combinations(signals, 2):
        if s1.subreddit != s2.subreddit and is_contradictory(s1.content, s2.content):
            contradictory_pairs.append((s1, s2))
            s1.is_contradiction = True
            s2.is_contradiction = True
    return contradictory_pairs

def analyze_contradictions(signals: list[Signal]):
    contradictory_pairs = detect_contradictions(signals)
    print("\nContradiction Analysis:")
    if not contradictory_pairs:
        print("No contradictory signal pairs detected.")
    else:
        for s1, s2 in contradictory_pairs:
            print(f"- {s1.subreddit}_{s1.id} ⟷ {s2.subreddit}_{s2.id}")
            print(f"  → A: {s1.content[:80]}...")
            print(f"  → B: {s2.content[:80]}...\n")
    return contradictory_pairs