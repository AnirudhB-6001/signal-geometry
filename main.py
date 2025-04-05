# dashboard.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Signal Geometry Dashboard", layout="wide")

st.title("📊 Signal Geometry — Live Dashboard")
st.markdown("A visual exploration of entropy, influence, and recursion dynamics.")

# Load data
signals_df = pd.read_csv("signals.csv")
nodes_df = pd.read_csv("nodes.csv")

# Section 1: Summary Stats
st.header("🔍 Quick Stats")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Signals", len(signals_df))
with col2:
    st.metric("Avg. Entropy", f"{signals_df['entropy'].mean():.2f}")
with col3:
    st.metric("Total Nodes", len(nodes_df))

# Section 2: Entropy Over Time
st.header("📈 Entropy Over Time")
fig1, ax1 = plt.subplots(figsize=(10, 4))
signals_df["timestamp"] = pd.to_datetime(signals_df["timestamp"])
signals_df = signals_df.sort_values("timestamp")
ax1.plot(signals_df["timestamp"], signals_df["entropy"], marker="o", linestyle="-")
ax1.set_xlabel("Time")
ax1.set_ylabel("Entropy")
ax1.grid(True)
st.pyplot(fig1)

# Section 3: Entropy & NSI by Subreddit
st.header("🧭 Subreddit Patterns")

col4, col5 = st.columns(2)
with col4:
    st.subheader("Avg. Entropy by Subreddit")
    fig2, ax2 = plt.subplots()
    sns.barplot(
        data=signals_df,
        x="avg_entropy_by_subreddit" if "avg_entropy_by_subreddit" in signals_df.columns else "subreddit",
        y="entropy",
        ax=ax2
    )
    plt.xticks(rotation=45)
    st.pyplot(fig2)

with col5:
    st.subheader("Avg. NSI by Subreddit")
    if "nsi" in signals_df.columns:
        fig3, ax3 = plt.subplots()
        sns.barplot(data=signals_df, x="subreddit", y="nsi", ax=ax3)
        plt.xticks(rotation=45)
        st.pyplot(fig3)
    else:
        st.warning("NSI column not found in signals.csv")

# Section 4: Node Influence Table
st.header("🧠 Influence Nodes Table")
st.dataframe(nodes_df.sort_values("power_score", ascending=False))

st.caption("All visualizations are generated from your local outputs. Refresh the dashboard after each run.")