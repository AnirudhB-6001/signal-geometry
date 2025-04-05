# src/model.py

from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Node:
    id: str
    type: str  # 'influencer', 'platform', 'institution', 'router'
    metadata: Dict[str, str] = None

@dataclass
class Signal:
    id: str
    content: str
    source: str  # Node ID
    timestamp: str
    entropy: float
    velocity: float
    impact: float
    route: List[str]  # Ordered list of node IDs it passed through
