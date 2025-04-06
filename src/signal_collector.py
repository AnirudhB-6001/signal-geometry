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

def match_route(post_title: str, subreddit: str) -> List[str]:
    route = ["reddit_thread", "user_1"]
    title_lower = post_title.lower()

    # Influencer matches
    influencers = {
        "trump": "trump",
        "modi": "modi",
        "elon": "elon_musk",
        "putin": "putin",
        "xi": "xi",
        "zelensky": "zelensky"
    }
    for keyword, node_id in influencers.items():
        if keyword in title_lower:
            route.append("user_2")
            route.append(node_id)
            return route

    # Institution matches
    institutions = {
        "nyt": "nyt",
        "washington": "washington_post",
        "bbc": "bbc",
        "al jazeera": "al_jazeera",
        "global times": "global_times"
    }
    for keyword, node_id in institutions.items():
        if keyword in title_lower:
            route.append("user_2")
            route.append(node_id)
            return route

    # Subreddit-based logic
    subreddit_map = {
        "geopolitics": "csis",
        "worldnews": "bbc",
        "politics": "trump"
    }
    if subreddit.lower() in subreddit_map:
        route.append("user_2")
        route.append(subreddit_map[subreddit.lower()])
    else:
        route.append("user_2")
        route.append("elon_musk")  # fallback

    return route

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
            title = post.title
            route = match_route(title, subreddit)

            signal = Signal(
                id=f"{subreddit}_{post.id}",
                content=title,
                title=title,
                source=subreddit,
                timestamp=datetime.utcfromtimestamp(post.created_utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                entropy=entropy,
                velocity=velocity,
                impact=round(min(1.0, (post.upvote_ratio or 0.8)), 2),
                route=route,
                subreddit=subreddit
            )
            signals.append(signal)

    return signals