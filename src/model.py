from dataclasses import dataclass, field
from typing import List, Optional, Dict

@dataclass
class Node:
    id: str
    type: str  # 'influencer', 'platform', 'institution', 'router'
    metadata: Optional[Dict[str, str]] = None

@dataclass
class Signal:
    id: str
    content: str
    title: str
    source: str
    timestamp: str
    entropy: float
    velocity: float
    impact: float

    # Optional fields to handle routing + platform specifics
    node: Optional[str] = None
    route: Optional[List[str]] = field(default_factory=list)
    subreddit: Optional[str] = None
    is_recursive: bool = False
    recursive_depth: int = 0
    seed_node: Optional[str] = None