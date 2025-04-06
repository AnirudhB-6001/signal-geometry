from datetime import datetime, timedelta
from typing import List, Dict
from src.model import Signal

def simulate_propagation(signals: List[Signal]) -> List[Dict]:
    timeline = []

    for signal in signals:
        base_time = datetime.strptime(signal.timestamp, "%Y-%m-%dT%H:%M:%SZ")
        delay_factor = (1.0 - signal.velocity + signal.entropy) / 2.0
        delay_factor = max(0.1, delay_factor)  # prevent zero or negative delays

        for i, node in enumerate(signal.route):
            delay = timedelta(seconds=int(i * 30 * delay_factor))
            arrival = base_time + delay
            timeline.append({
                "signal_id": signal.id,
                "node": node,
                "arrival_time": arrival.strftime("%Y-%m-%dT%H:%M:%SZ")
            })

    return timeline