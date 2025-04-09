import requests
import os
from dotenv import load_dotenv
from datetime import datetime
from src.model import Signal

load_dotenv()
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

def estimate_entropy(text: str) -> float:
    length = len(text or "")
    return min(round(length / 1000.0, 2), 1.0)

def estimate_velocity(published_at: str) -> float:
    try:
        time_diff = (datetime.utcnow() - datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")).total_seconds() / 3600
        return min(round(1.0 / (time_diff + 1), 2), 1.0)
    except:
        return 0.0

def collect_signals_from_news(topics: list, limit=10):
    signals = []

    for topic in topics:
        url = (
            f"https://newsapi.org/v2/everything?"
            f"q={topic}&pageSize={limit}&sortBy=publishedAt&apiKey={NEWSAPI_KEY}"
        )

        try:
            response = requests.get(url)
            response.raise_for_status()
            articles = response.json().get("articles", [])

            for i, article in enumerate(articles):
                published_at = article.get("publishedAt", "")
                if not published_at:
                    continue

                try:
                    timestamp = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
                except ValueError:
                    continue

                content = (article.get("description") or article.get("content") or "").strip()
                title = (article.get("title") or "").strip()

                if not content:
                    continue  # skip empty signals

                entropy = estimate_entropy(content)
                velocity = estimate_velocity(published_at)

                # Temporary route: only includes AI node as source
                route = ["news_aggregator_ai"]

                if len(route) < 2:
                    print(f"⚠️ Incomplete route for signal {topic}_{i}. Downstream nodes missing. Skipping extra hops.")

                signal = Signal(
                    id=f"{topic}_{i}",
                    content=content,
                    title=title[:80],
                    source="newsapi",
                    timestamp=timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    entropy=entropy,
                    velocity=velocity,
                    impact=round(entropy + velocity, 2),
                    node="news_aggregator_ai",
                    route=route,
                    subreddit=topic,  # reuse this field to track original topic
                    is_recursive=False
                )
                signals.append(signal)

        except Exception as e:
            print(f"❌ Error fetching for topic '{topic}': {e}")

    return signals