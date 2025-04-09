import tweepy
import os
from datetime import datetime
from dotenv import load_dotenv
from src.model import Signal
from src.twitter_handles import twitter_handles

load_dotenv()
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

client = tweepy.Client(bearer_token=BEARER_TOKEN)

def estimate_entropy(retweets: int, likes: int) -> float:
    raw = retweets / (likes + 1)
    return min(round(raw, 2), 1.0)

def estimate_velocity(likes: int, hours_old: float) -> float:
    if hours_old == 0:
        return 1.0
    return min(round((likes / hours_old) / 100.0, 2), 1.0)

def collect_signals_from_twitter(limit=10):
    signals = []

    # Prompt user for handles
    input_str = input("\nEnter up to 3 Twitter nodes to fetch (comma-separated, e.g., elon_musk, trump, bbc): ")
    selected_nodes = [s.strip().lower() for s in input_str.split(",") if s.strip()][:3]

    if not selected_nodes:
        print("No Twitter nodes provided. Skipping Twitter collection.")
        return []

    for node_id in selected_nodes:
        handle = twitter_handles.get(node_id)
        if not handle:
            print(f"⚠️ No Twitter handle found for '{node_id}' in twitter_handles.py")
            continue

        try:
            user_data = client.get_user(username=handle)
            tweets = client.get_users_tweets(
                id=user_data.data.id,
                max_results=limit,
                tweet_fields=["created_at", "public_metrics"]
            )

            if not tweets.data:
                print(f"ℹ️ No tweets found for {handle}")
                continue

            for tweet in tweets.data:
                metrics = tweet.public_metrics
                likes = metrics.get("like_count", 0)
                retweets = metrics.get("retweet_count", 0)
                timestamp = tweet.created_at
                hours_old = (datetime.utcnow() - timestamp.replace(tzinfo=None)).total_seconds() / 3600

                entropy = estimate_entropy(retweets, likes)
                velocity = estimate_velocity(likes, hours_old)

                # Build route (seed → user) only if valid seed node
                route = [node_id]
                seed_node = node_id

                # Optional: simulate one router hop if needed (commented out)
                # route.append(f"user_{random.randint(1, 5)}")

                signal = Signal(
                    id=f"{node_id}_{tweet.id}",
                    content=tweet.text,
                    title=tweet.text[:80],
                    source="twitter",
                    timestamp=timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    entropy=entropy,
                    velocity=velocity,
                    impact=round(min(1.0, (likes + 1) / 1000.0), 2),
                    node=node_id,
                    route=route,
                    seed_node=seed_node
                )

                if len(route) < 2:
                    print(f"⚠️ Incomplete route for signal {signal.id}. Downstream nodes missing. Skipping extra hops.")

                signals.append(signal)

        except Exception as e:
            print(f"❌ Error fetching for {handle}: {e}")

    return signals