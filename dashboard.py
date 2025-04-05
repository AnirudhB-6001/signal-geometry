# dashboard.py

import streamlit as st
import pandas as pd
from signal import Signal
from analyzer import SignalAnalyzer
from main import run_signal_geometry  # assumes your main logic is here and returns data
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide", page_title="Signal Geometry Dashboard")

st.title("📡 Signal Geometry - Live Dashboard")
st.markdown("Real-time narrative signal monitoring from Reddit and other sources")

# Sidebar
st.sidebar.header("⚙️ Configuration")
subreddits_input = st.sidebar.text_input("Enter subreddits (comma-separated)", "politics,worldnews")
refresh = st.sidebar.button("🔄 Run Signal Geometry")

if refresh:
    with st.spinner("Fetching and analyzing signals..."):
        subreddit_list = [s.strip() for s in subreddits_input.split(",") if s.strip()]
        results_df, charts = run_signal_geometry(subreddit_list)

        # Show raw data
        st.subheader("📊 Signal Summary Table")
        st.dataframe(results_df, use_container_width=True)

        # Show plots
        st.subheader("📈 Entropy & Drift by Subreddit")
        col1, col2 = st.columns(2)

        with col1:
            st.pyplot(charts["entropy_plot"])
        with col2:
            st.pyplot(charts["drift_plot"])

        # Show NSI summary
        st.subheader("🧠 Narrative Synchronization Index (NSI)")
        st.metric(label="NSI (Normalized)", value=round(results_df["nsi"].mean(), 3))

        # Show contradiction report
        st.subheader("❗ Contradiction Alerts")
        contradiction_summary = "\n".join(results_df["contradiction_notes"].dropna().tolist())
        st.code(contradiction_summary or "No contradictions found.")

else:
    st.info("Enter subreddits and press 'Run Signal Geometry' to begin.")