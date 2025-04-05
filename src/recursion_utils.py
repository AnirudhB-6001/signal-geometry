# src/recursion_utils.py

from src.model import Signal

# List of keywords that hint at platform self-reference or influencer-based recursion
PLATFORM_KEYWORDS = [
    "twitter", "reddit", "youtube", "facebook", "tiktok", "whatsapp",
    "elon musk", "tweet", "thread", "trending", "viral"
]

def is_recursive(signal: Signal) -> bool:
    """Returns True if the signal content references another platform or influencer."""
    text = signal.content.lower()
    return any(keyword in text for keyword in PLATFORM_KEYWORDS)

def assign_recursive_depth(signal: Signal):
    """
    Assigns a recursive depth score to a signal.
    - 0: original content (no platform mentions)
    - 1+: self-referential or meta-level reaction detected
    """
    depth = 0
    text = signal.content.lower()

    for keyword in PLATFORM_KEYWORDS:
        if keyword in text:
            depth += 1

    signal.recursive_depth = depth
    signal.is_recursive = depth > 0

def analyze_recursions(signals: list[Signal]):
    """Prints a summary of all recursive signals and their estimated depth."""
    print("\nRecursion Analysis:")

    for signal in signals:
        assign_recursive_depth(signal)

    recursive_signals = [s for s in signals if s.is_recursive]
    if not recursive_signals:
        print("No recursive signals detected.")
    else:
        for s in recursive_signals:
            print(f"- {s.id}: Depth = {s.recursive_depth} | Content = {s.content[:80]}...")

def detect_recursion(signals: list[Signal]) -> set:
    """
    Returns a set of node IDs that are part of recursive signal routes.
    Useful for graph color-coding or filtering.
    """
    recursive_nodes = set()

    for signal in signals:
        assign_recursive_depth(signal)
        if signal.is_recursive:
            recursive_nodes.update(signal.route)

    return recursive_nodes