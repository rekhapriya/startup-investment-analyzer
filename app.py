"""
Startup Investment Analyzer
----------------------------
An interactive Streamlit application that helps an investment company
store, explore, and analyze startup data before making investment decisions.

Author: Rekha Priya
Course: AI & ML — Wenchwise (Evening Batch)
Assignment 6
"""

import streamlit as st
import pandas as pd

# ----------------------------------------------------------------------
# PAGE CONFIG — must be the first Streamlit command
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Startup Investment Analyzer",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------
# CUSTOM STYLING
# ----------------------------------------------------------------------
st.markdown("""
<style>
    .main-header {
        font-size: 2.3rem;
        font-weight: 800;
        color: #1a1f36;
        margin-bottom: 0rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #6b7280;
        margin-bottom: 1.5rem;
    }
    div[data-testid="stMetric"] {
        background-color: #f8fafc;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 1rem;
    }
    div[data-testid="stMetricLabel"] {
        font-weight: 600;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 8px 16px;
        font-weight: 600;
    }
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# SESSION STATE — in-memory "database" of startups
# ----------------------------------------------------------------------
if "startups" not in st.session_state:
    # Preloaded sample data so the app is useful immediately on launch
    st.session_state.startups = pd.DataFrame([
        {"Startup Name": "NeoBank",        "Sector": "FinTech",     "Investment (₹L)": 250, "Founded Year": 2019, "Location": "Bengaluru"},
        {"Startup Name": "CropSense",      "Sector": "AgriTech",    "Investment (₹L)": 80,  "Founded Year": 2021, "Location": "Chennai"},
        {"Startup Name": "MediTrack",      "Sector": "HealthTech",  "Investment (₹L)": 420, "Founded Year": 2018, "Location": "Hyderabad"},
        {"Startup Name": "EduSpark",       "Sector": "EdTech",      "Investment (₹L)": 150, "Founded Year": 2020, "Location": "Pune"},
        {"Startup Name": "GreenGrid",      "Sector": "CleanTech",   "Investment (₹L)": 600, "Founded Year": 2017, "Location": "Mumbai"},
        {"Startup Name": "ShopEase",       "Sector": "E-commerce",  "Investment (₹L)": 35,  "Founded Year": 2022, "Location": "Delhi"},
        {"Startup Name": "AIVision Labs",  "Sector": "AI/ML",       "Investment (₹L)": 310, "Founded Year": 2020, "Location": "Bengaluru"},
    ])

df = st.session_state.startups

# ----------------------------------------------------------------------
# HEADER
# ----------------------------------------------------------------------
st.markdown('<p class="main-header">💼 Startup Investment Analyzer</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">A data-driven tool to help investment teams evaluate startups before making decisions.</p>', unsafe_allow_html=True)

# ----------------------------------------------------------------------
# SIDEBAR — Add Startup Form
# ----------------------------------------------------------------------
with st.sidebar:
    st.header("➕ Add New Startup")
    with st.form("add_startup_form", clear_on_submit=True):
        name = st.text_input("Startup Name")
        sector = st.selectbox(
            "Business Sector",
            ["FinTech", "AgriTech", "HealthTech", "EdTech", "CleanTech",
             "E-commerce", "AI/ML", "Logistics", "Other"]
        )
        investment = st.number_input("Investment Amount (₹ in Lakhs)", min_value=0.0, step=1.0)
        year = st.number_input("Founded Year", min_value=1990, max_value=2026, value=2022, step=1)
        location = st.text_input("Location (City)")

        submitted = st.form_submit_button("Add Startup", use_container_width=True)

        if submitted:
            if name.strip() == "":
                st.error("Startup name cannot be empty.")
            else:
                new_row = pd.DataFrame([{
                    "Startup Name": name.strip(),
                    "Sector": sector,
                    "Investment (₹L)": investment,
                    "Founded Year": int(year),
                    "Location": location.strip() if location else "Not specified",
                }])
                st.session_state.startups = pd.concat(
                    [st.session_state.startups, new_row], ignore_index=True
                )
                st.success(f"✅ '{name}' added successfully!")
                st.rerun()

    st.divider()
    st.caption("💡 Tip: Add a few startups, then explore the tabs to see instant analysis.")

# Refresh reference after any additions
df = st.session_state.startups

# ----------------------------------------------------------------------
# KEY METRICS (Total / Average / Highest / Lowest)
# ----------------------------------------------------------------------
if not df.empty:
    total_investment = df["Investment (₹L)"].sum()
    avg_investment = df["Investment (₹L)"].mean()
    highest_row = df.loc[df["Investment (₹L)"].idxmax()]
    lowest_row = df.loc[df["Investment (₹L)"].idxmin()]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Investment", f"₹{total_investment:,.0f}L")
    c2.metric("Average Investment", f"₹{avg_investment:,.1f}L")
    c3.metric("🏆 Highest Funded", highest_row["Startup Name"], f"₹{highest_row['Investment (₹L)']:,.0f}L")
    c4.metric("📉 Lowest Funded", lowest_row["Startup Name"], f"₹{lowest_row['Investment (₹L)']:,.0f}L")
else:
    st.info("No startup data yet. Add a startup using the sidebar to get started.")

st.divider()

# ----------------------------------------------------------------------
# TABS — organizes the 8 required features cleanly
# ----------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 All Startups", "🔍 Search", "🏆 Top & Bottom", "📊 Sector Analysis"
])

# --- TAB 1: Display all startups -----------------------------------------
with tab1:
    st.subheader("All Registered Startups")
    if df.empty:
        st.warning("No startups to display yet.")
    else:
        st.dataframe(
            df.sort_values("Investment (₹L)", ascending=False),
            use_container_width=True,
            hide_index=True,
        )
        st.caption(f"Showing {len(df)} startup(s).")

# --- TAB 2: Search for a startup -------------------------------------------
with tab2:
    st.subheader("Search for a Startup")
    search_term = st.text_input("Enter startup name or sector to search", placeholder="e.g. FinTech or NeoBank")

    if search_term:
        results = df[
            df["Startup Name"].str.contains(search_term, case=False, na=False) |
            df["Sector"].str.contains(search_term, case=False, na=False)
        ]
        if results.empty:
            st.error(f"No startups found matching '{search_term}'.")
        else:
            st.success(f"Found {len(results)} result(s) for '{search_term}'.")
            st.dataframe(results, use_container_width=True, hide_index=True)
    else:
        st.caption("Start typing to search across startup names and sectors.")

# --- TAB 3: Highest & Lowest investment -------------------------------------
with tab3:
    st.subheader("Investment Extremes")
    if df.empty:
        st.warning("No data available.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🏆 Highest Investment")
            st.dataframe(df.loc[[df["Investment (₹L)"].idxmax()]], use_container_width=True, hide_index=True)
        with col2:
            st.markdown("#### 📉 Lowest Investment")
            st.dataframe(df.loc[[df["Investment (₹L)"].idxmin()]], use_container_width=True, hide_index=True)

        st.markdown("#### Investment Distribution")
        chart_df = df.set_index("Startup Name")["Investment (₹L)"].sort_values(ascending=False)
        st.bar_chart(chart_df)

# --- TAB 4: Sector-wise analysis --------------------------------------------
with tab4:
    st.subheader("Analysis by Business Sector")
    if df.empty:
        st.warning("No data available.")
    else:
        sector_summary = df.groupby("Sector").agg(
            Startup_Count=("Startup Name", "count"),
            Total_Investment=("Investment (₹L)", "sum"),
            Average_Investment=("Investment (₹L)", "mean"),
        ).reset_index().rename(columns={
            "Startup_Count": "Number of Startups",
            "Total_Investment": "Total Investment (₹L)",
            "Average_Investment": "Average Investment (₹L)",
        }).sort_values("Total Investment (₹L)", ascending=False)

        st.dataframe(sector_summary, use_container_width=True, hide_index=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Total Investment by Sector")
            st.bar_chart(sector_summary.set_index("Sector")["Total Investment (₹L)"])
        with col2:
            st.markdown("#### Number of Startups by Sector")
            st.bar_chart(sector_summary.set_index("Sector")["Number of Startups"])

# ----------------------------------------------------------------------
# FOOTER
# ----------------------------------------------------------------------
st.divider()
st.caption("Built with Python & Streamlit | Assignment 6 — Startup Investment Analyzer")
