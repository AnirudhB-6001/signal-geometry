# src/model.py

from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class Node:
    id: str
    type: str  # 'influencer', 'platform', 'institution', 'router'
    metadata: Optional[Dict[str, str]] = None

@dataclass
class Signal:
    id: str
    content: str
    source: str                # The originating node ID (e.g., subreddit, 'newsapi', etc.)
    timestamp: str             # ISO format
    entropy: float
    velocity: float
    impact: float
    route: List[str]           # Ordered list of node IDs the signal passed through
    subreddit: Optional[str] = None  # Source subreddit, if applicable

    # Optional fields used in recursion/contradiction analysis
    is_recursive: bool = False
    recursive_depth: int = 0