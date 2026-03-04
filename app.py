import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(page_title="Go Noise Sales Dashboard", layout="wide")

# Custom Styling for Mobile
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🎧 Go Noise Sales & Distribution")
st.subheader("Performance Tracker: Jan - Feb 2026")

# 2. Data Preparation (Extracted from your images)
# Note: In a real app, you would upload an Excel/CSV here.
data = {
    "Month": ["January", "February"],
    "Total_Billing": [63240530, 58071214],
    "Total_Qty": [45712, 42970],
    "Watch_Billing": [41371255, 39014180],
    "Audio_Billing": [18105740, 15269489]
}
df_monthly = pd.DataFrame(data)

salesman_data = pd.DataFrame({
    "Salesman": ["GURUNATH", "DINESH", "JULESH", "AMIT", "FIROZ", "LAXMAN"],
    "Zone": ["WEST-1", "WEST-2", "WEST-2", "WEST-1", "WEST-1", "MUMBAI D2R"],
    "Jan_Billing": [21474830, 9000051, 9357782, 704764, 134317, 1656000],
    "Feb_Billing": [19691917, 8028997, 13354929, 704801, 189948, 1560000],
    "Watch_ASP": [1339, 1322, 1573, 1552, 1520, 1480]
})

# 3. Sidebar Filters
st.sidebar.header("Dashboard Filters")
selected_month = st.sidebar.selectbox("View Data For:", ["February 2026", "January 2026"])
month_key = "Feb_Billing" if "February" in selected_month else "Jan_Billing"

# 4. Top KPI Ribbon
m_idx = 1 if "February" in selected_month else 0
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Billing", f"₹{df_monthly.iloc[m_idx]['Total_Billing']:,}")
with col2:
    st.metric("Total Qty", f"{df_monthly.iloc[m_idx]['Total_Qty']:,}")
with col3:
    growth = ((df_monthly.iloc[1]['Total_Billing'] - df_monthly.iloc[0]['Total_Billing']) / df_monthly.iloc[0]['Total_Billing']) * 100
    st.metric("MoM Growth", f"{growth:.1f}%", delta=f"{growth:.1f}%", delta_color="inverse")

st.markdown("---")

# 5. Salesman Comparison Tool
st.header("🤝 Salesman Comparison")
c1, c2 = st.columns(2)
with c1:
    s1 = st.selectbox("Select Salesman A", salesman_data["Salesman"].unique(), index=0)
with c2:
    s2 = st.selectbox("Select Salesman B", salesman_data["Salesman"].unique(), index=2)

s1_row = salesman_data[salesman_data["Salesman"] == s1].iloc[0]
s2_row = salesman_data[salesman_data["Salesman"] == s2].iloc[0]

fig_comp = go.Figure(data=[
    go.Bar(name=s1, x=["Billing", "Watch ASP"], y=[s1_row[month_key], s1_row["Watch_ASP"]]),
    go.Bar(name=s2, x=["Billing", "Watch ASP"], y=[s2_row[month_key], s2_row["Watch_ASP"]])
])
fig_comp.update_layout(barmode='group', height=400)
st.plotly_chart(fig_comp, use_container_width=True)

# 6. Regional Insights
st.header("📍 Regional Contribution")
fig_pie = px.pie(salesman_data, values=month_key, names='Zone', hole=0.4, 
                 color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(fig_pie, use_container_width=True)

st.success("Dashboard Updated with latest Go Noise February figures.")


