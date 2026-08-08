import streamlit as st
from tools import market_analysis, forecasting, kpi_dashboard

st.set_page_config(
    page_title="PulseMetrics",
    page_icon="📊",
    layout="wide"
)

st.sidebar.title("📊 PulseMetrics")
st.sidebar.markdown("AI-Powered Business Analytics")

tool = st.sidebar.radio(
    "Choose a tool",
    ["Market Analysis", "Demand Forecasting", "Business KPI Dashboard"]
)

st.title(tool)

if tool == "Market Analysis":
    market_analysis.run()
elif tool == "Demand Forecasting":
    forecasting.run()
elif tool == "Business KPI Dashboard":
    kpi_dashboard.run()