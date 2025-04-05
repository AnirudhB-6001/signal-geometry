# src/signal_collector.py

import praw
from datetime import datetime
from typing import List
from src.model import Signal

REDDIT_CLIENT_ID = "N_p_oD5ZWxjKaB51-saONA"
REDDIT_CLIENT_SECRET = "TJI-C3DluHTmMNZXOf-syKhcHsP3EQ"
REDDIT_USER_AGENT = "signal-geometry-bot:v1.0 (by u/Alchemist6001)"

def estimate_entropy(upvotes: int, comments: int) -> float:
    raw = comments / (upvotes + 1)
    return min(round(raw, 2), 1.0)

def estimate_velocity(score: int, hours_old: float) -> float:
    if hours_old == 0:
        return 1.0
    v = score / hours_old
    return min(round(v / 100.0, 2), 1.0)

def collect_signals_from_reddit(subreddits: List[str], limit=5) -> List[Signal]:
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )

    signals = []

    for subreddit in subreddits:
        posts = reddit.subreddit(subreddit).hot(limit=limit)
        for post in posts:
            hours_old = (datetime.utcnow() - datetime.utcfromtimestamp(post.created_utc)).total_seconds() / 3600
            entropy = estimate_entropy(post.score, post.num_comments)
            velocity = estimate_velocity(post.score, hours_old)

            signal = Signal(
                id=f"{subreddit}_{post.id}",
                content=post.title,
                source=subreddit,
                timestamp=datetime.utcfromtimestamp(post.created_utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                entropy=entropy,
                velocity=velocity,
                impact=round(min(1.0, (post.upvote_ratio or 0.8)), 2),
                route=["reddit_thread", "user_1", "user_2", "elon_musk"],
                subreddit=subreddit  # ✅ NEW
            )
            signals.append(signal)

    return signals