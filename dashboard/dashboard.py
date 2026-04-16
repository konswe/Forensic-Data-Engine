import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Forensic Data Engine", layout="wide", initial_sidebar_state="expanded")
st.title("Forensic System Logs Dashboard")

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = "localhost"
DB_NAME = "forensic_logs"

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

@st.cache_data(ttl=60)
def load_data():
    engine = create_engine(DB_URL)
    query = "SELECT * FROM windows_events ORDER BY \"TimeCreated\" DESC;"
    return pd.read_sql(query, engine)

try:
    df = load_data()

    st.sidebar.title("Threat Filters")
    st.sidebar.markdown("Configure search parameters to narrow down the results.")

    with st.sidebar.expander("Target Environment", expanded=True):
        selected_computer = st.multiselect(
            "Target Computers",
            options=df["Computer"].unique(),
            default=df["Computer"].unique(),
            help="Select specific computers (hosts) to investigate for signs of compromise."
        )

    with st.sidebar.expander("Event Signatures", expanded=True):
        selected_event_id = st.multiselect(
            "Event IDs",
            options=df["EventID"].unique(),
            default=df["EventID"].unique(),
            help="Key IDs to track: 104 (Log cleared), 4624 (Successful logon), 4799 (Group enumeration)."
        )

    with st.sidebar.expander("Evidence Files (Source)", expanded=False):
        selected_source = st.multiselect(
            "Source .evtx files",
            options=df["SourceFile"].unique(),
            default=df["SourceFile"].unique(),
            help="Select a specific log package collected as evidence."
        )

    mask = (
        df["Computer"].isin(selected_computer) &
        df["EventID"].isin(selected_event_id) &
        df["SourceFile"].isin(selected_source)
    )
    df_filtered = df[mask]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Events", len(df_filtered))
    col2.metric("Affected Machines", df_filtered['Computer'].nunique())
    col3.metric("Critical Alerts", len(df_filtered[df_filtered['EventID'].isin(['104', '1102'])]))

    st.markdown("---")

    tab1, tab2 = st.tabs(["Visual Analytics", "Raw Evidence Logs"])

    with tab1:
        st.subheader("Event ID Distribution")
        if not df_filtered.empty:
            event_counts = df_filtered['EventID'].value_counts()
            st.bar_chart(event_counts)
        else:
            st.info("No data available for selected filters.")

    with tab2:
        st.subheader("Detailed Logs")
        st.dataframe(df_filtered, use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"Database connection error: {e}")
