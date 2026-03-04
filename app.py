import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="Go Noise Trend Commander", layout="wide")
st.title("📈 Go Noise: Multi-Month Trend Engine")
st.caption("Tracking Performance: Guru (MH) | Dinesh (MPCG) | Julesh (GJ)")

# 2. Historical Data (Jan & Feb)
data = {
    "Month": ["Jan", "Jan", "Jan", "Feb", "Feb", "Feb"],
    "Region": ["MAHARASHTRA", "MP/CG", "GUJARAT", "MAHARASHTRA", "MP/CG", "GUJARAT"],
    "Lead": ["GURU", "DINESH", "JULESH", "GURU", "DINESH", "JULESH"],
    "Total_Revenue": [36585517, 7500000, 18357833, 29915548, 8500000, 21383926],
    "Watch_Sales": [24787218, 5500000, 10837587, 18936557, 6200000, 15286214]
}
df = pd.DataFrame(data)

# 3. Sidebar: Select Comparison Months
st.sidebar.header("Trend Settings")
month_a = st.sidebar.selectbox("Base Month", df['Month'].unique(), index=0)
month_b = st.sidebar.selectbox("Comparison Month", df['Month'].unique(), index=1)

# 4. Comparison Logic
df_a = df[df['Month'] == month_a].set_index('Lead')
df_b = df[df['Month'] == month_b].set_index('Lead')

# Calculation of Variance
variance = (df_b['Total_Revenue'] - df_a['Total_Revenue'])
growth_pct = (variance / df_a['Total_Revenue']) * 100

# 5. Trend Analysis View
st.header(f"Comparing {month_a} vs {month_b}")

col1, col2, col3 = st.columns(3)
# Show Metrics for Guru, Dinesh, Julesh
for i, lead in enumerate(['GURU', 'DINESH', 'JULESH']):
    cols = [col1, col2, col3]
    cols[i].metric(
        label=f"{lead} ({df_b.loc[lead, 'Region']})",
        value=f"₹{df_b.loc[lead, 'Total_Revenue']:,}",
        delta=f"{growth_pct.loc[lead]:.1f}% Growth"
    )

# 6. Visualizing the Velocity
st.markdown("---")
st.subheader("Revenue Velocity: Monthly Comparison")
fig = px.bar(df[df['Month'].isin([month_a, month_b])], 
             x="Lead", y="Total_Revenue", color="Month", 
             barmode="group", text_auto='.2s',
             color_discrete_map={'Jan': '#2E4053', 'Feb': '#F4D03F'})
st.plotly_chart(fig, use_container_width=True)

# 7. AI Insight for Trends
st.subheader("🧠 AI Trend Insight")
top_growth_lead = growth_pct.idxmax()
st.info(f"AI Analysis: **{top_growth_lead}** is showing the highest positive velocity between {month_a} and {month_b}. Suggest analyzing their current field strategy for replication in other zones.")
