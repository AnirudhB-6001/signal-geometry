import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title("🧠 Signal Geometry Dashboard")

# Section: Signal Data Table
st.header("📄 Raw Signal Data")
try:
    df = pd.read_csv("signals.csv")
    st.dataframe(df[["id", "title", "subreddit", "entropy", "nsi_score", "recursion_score"]])
except FileNotFoundError:
    st.warning("signals.csv not found. Please run main.py first.")

# Section: Charts
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