# test_collector.py

from src.signal_collector import collect_signals_from_reddit

signals = collect_signals_from_reddit("worldnews", limit=3)

for s in signals:
    print(f"{s.id} | Entropy: {s.entropy} | Velocity: {s.velocity} | Impact: {s.impact}")
    print(f"→ {s.content}")
