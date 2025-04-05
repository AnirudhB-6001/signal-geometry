# src/seed_nodes.py

from src.model import Node

seed_nodes = [
    # Influencers
    Node(id="elon_musk", type="influencer", metadata={"region": "global", "platform": "Twitter"}),
    Node(id="xi", type="influencer", metadata={"region": "china", "platform": "Weibo"}),
    Node(id="putin", type="influencer", metadata={"region": "russia", "platform": "RT"}),
    Node(id="zelensky", type="influencer", metadata={"region": "ukraine", "platform": "Twitter"}),
    Node(id="trump", type="influencer", metadata={"region": "us", "platform": "TruthSocial"}),
    Node(id="modi", type="influencer", metadata={"region": "india", "platform": "Twitter"}),

    # Institutions - Media
    Node(id="nyt", type="institution", metadata={"region": "us", "category": "media"}),
    Node(id="bbc", type="institution", metadata={"region": "uk", "category": "media"}),
    Node(id="al_jazeera", type="institution", metadata={"region": "qatar", "category": "media"}),
    Node(id="global_times", type="institution", metadata={"region": "china", "category": "media"}),
    Node(id="washington_post", type="institution", metadata={"region": "us", "category": "media"}),
    Node(id="toi", type="institution", metadata={"region": "india", "category": "media"}),

    # Institutions - Think Tanks
    Node(id="rand_corp", type="institution", metadata={"region": "us", "category": "think_tank"}),
    Node(id="brookings", type="institution", metadata={"region": "us", "category": "think_tank"}),
    Node(id="orfonline", type="institution", metadata={"region": "india", "category": "think_tank"}),
    Node(id="csis", type="institution", metadata={"region": "us", "category": "think_tank"}),
    Node(id="carnegie", type="institution", metadata={"region": "us", "category": "think_tank"}),

    # Users
    Node(id="user_1", type="router"),
    Node(id="user_2", type="router"),
    Node(id="user_3", type="router"),
    Node(id="user_4", type="router"),

    # Platforms
    Node(id="reddit", type="platform", metadata={"region": "global", "category": "social"}),
    Node(id="twitter", type="platform", metadata={"region": "global", "category": "social"}),
    Node(id="youtube", type="platform", metadata={"region": "global", "category": "social"}),
    Node(id="facebook", type="platform", metadata={"region": "global", "category": "social"}),
    Node(id="whatsapp", type="platform", metadata={"region": "global", "category": "social"}),
    Node(id="tiktok", type="platform", metadata={"region": "global", "category": "social"}),

    # Machines
    Node(id="chatgpt", type="machine", metadata={"region": "global", "vendor": "openai"}),
    Node(id="fb_newsfeed", type="machine", metadata={"region": "global", "vendor": "meta"}),
    Node(id="youtube_recommendation", type="machine", metadata={"region": "global", "vendor": "google"}),
    Node(id="twitter_trending", type="machine", metadata={"region": "global", "vendor": "x-corp"}),
    Node(id="news_aggregator_ai", type="machine", metadata={"region": "global", "vendor": "unknown"}),
]

Node(id="reddit_thread", type="router"),