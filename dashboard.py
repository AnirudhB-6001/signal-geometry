# dashboard.py

import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("🧠 Signal Geometry Dashboard")

# --- Section 1: Full Raw Signal Data Table ---
st.header("📄 Raw Signal Dataset")

# Load enriched signal.csv
try:
    df = pd.read_csv("signals.csv")
except FileNotFoundError:
    st.error("signals.csv not found. Please run main.py to generate data.")
    st.stop()

# Define expected columns (order + categories)
columns = [
    "id", "title", "subreddit", "source",                    # Basic
    "entropy", "velocity", "impact",                         # Core
    "route", "route_length",                                 # Propagation
    "drift_score", "nsi_score",                              # Narrative/Truth
    "recursion_score", "recursive_depth",                    # Feedback Loop
    "power_index", "seed_node"                               # Influence
]

# Ensure all fields are present and format table
def format_cell(val):
    if pd.isna(val) or val == "":
        return "❌"
    return val

styled_df = df[columns].style.format(format_cell)
st.dataframe(styled_df, use_container_width=True, height=500)

# --- Section 2: Metric Legend (no nesting error) ---
st.markdown("---")
st.header("📘 Signal Geometry Metric Definitions")

metrics_info = {
    "Entropy": {
        "status": True,
        "summary": "Unpredictability or randomness in content.",
        "what": "Measures how chaotic a signal is. High entropy = low coherence.",
        "why": "Detects noise vs. structured information.",
        "system": "Used in impact score and truth drift.",
        "range": "0–0.3: Stable | 0.3–0.7: Moderate | 0.7+: Chaotic"
    },
    "Velocity": {
        "status": True,
        "summary": "Speed of propagation through the graph.",
        "what": "Measures how fast a signal spreads from origin.",
        "why": "Detects virality potential.",
        "system": "Used in impact score + edge weighting.",
        "range": "0–0.2: Slow | 0.2–0.7: Moderate | 0.7+: Fast"
    },
    "Impact Score": {
        "status": True,
        "summary": "Entropy + Velocity (capped at 2.0)",
        "what": "Quick snapshot of total disruption potential.",
        "why": "Combines disorder and speed for priority ranking.",
        "system": "Used to filter urgent signals and rank.",
        "range": "<1.0: Low | 1.0–1.5: Medium | >1.5: High"
    },
    "Route": {
        "status": True,
        "summary": "List of nodes the signal passed through.",
        "what": "Shows actual signal trajectory across graph.",
        "why": "Understand how ideas flow.",
        "system": "Used for truth drift, recursion checks.",
        "range": "Varies by hop count and graph structure."
    },
    "Route Length": {
        "status": True,
        "summary": "Hop count from source to destination.",
        "what": "Length of the path the signal followed.",
        "why": "Short = direct transmission, long = layered diffusion.",
        "system": "Input to truth drift, NSI, recursion logic.",
        "range": "1–2: Direct | 3–4: Multi-hop | 5+: Viral cascade"
    },
    "Truth Drift": {
        "status": True,
        "summary": "How much the signal deviated from its origin.",
        "what": "Deviation between origin vs. final node view.",
        "why": "Tracks distortion over hops.",
        "system": "Used to detect manipulations and polarization.",
        "range": "0.0: Perfect | >0.5: Severe distortion"
    },
    "NSI Score": {
        "status": True,
        "summary": "Narrative Stability Index.",
        "what": "How consistent is the story as it spreads?",
        "why": "Low NSI = narrative breakdown.",
        "system": "Used to evaluate coherence of clusters.",
        "range": "0–3: Unstable | 3–7: Moderate | 7–10: Stable"
    },
    "Recursion Score": {
        "status": True,
        "summary": "How much the signal loops back.",
        "what": "Looping or self-reinforcing content indicator.",
        "why": "Detects echo chambers.",
        "system": "Highlighted during feedback loop detection.",
        "range": "0: None | 1+: Repetition / Recursive"
    },
    "Recursive Depth": {
        "status": True,
        "summary": "Levels of nesting in recursion.",
        "what": "How deep the loop chain runs.",
        "why": "More levels = stronger feedback bubble.",
        "system": "Used for highlighting propagation patterns.",
        "range": "0: Not recursive | 1–2: Shallow | 3+: Deep"
    },
    "Power Index": {
        "status": True,
        "summary": "Node influence based on graph centrality.",
        "what": "How strong a node's broadcasting capability is.",
        "why": "Identify leaders or super-spreaders.",
        "system": "Used for prioritizing origin sources.",
        "range": "0–1: Weak | 1–3: Moderate | 3+: Influential"
    },
    "Seed Node": {
        "status": True,
        "summary": "Original node that launched the signal.",
        "what": "Root or initiator of propagation.",
        "why": "Source attribution.",
        "system": "Logged in route and graph edges.",
        "range": "Varies depending on platform or user."
    }
}

for metric, meta in metrics_info.items():
    icon = "✅" if meta["status"] else "❌"
    with st.expander(f"{icon} **{metric}** – {meta['summary']}", expanded=False):
        st.markdown(f"**What:** {meta['what']}")
        st.markdown(f"**Why:** {meta['why']}")
        st.markdown(f"**System Use:** {meta['system']}")
        st.markdown(f"**Range:** {meta['range']}")

st.divider()

# --- Section 3: Static Visuals ---
st.markdown("---")
st.header("📊 Visual Insights")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Entropy Over Time")
    st.image("entropy_over_time.png")

with col2:
    st.subheader("Average Entropy by Subreddit")
    st.image("avg_entropy_by_subreddit.png")

col3, col4 = st.columns(2)
with col3:
    st.subheader("Average NSI by Subreddit")
    st.image("avg_nsi_by_subreddit.png")

with col4:
    st.subheader("Influence Graph")
    st.image("influence_graph.png")
