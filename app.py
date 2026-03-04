import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# 1. Page Config & Professional Branding
st.set_page_config(page_title="Go Noise Tri-State Executive", layout="wide")
st.markdown("""
    <style>
    .stMetric { background-color: #ffffff; border-bottom: 4px solid #F4D03F; padding: 15px; border-radius: 10px; }
    .main { background-color: #f4f7f6; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎧 Go Noise: West & Central India")
st.caption("Operations: Maharashtra | Gujarat | MP/CG")

# 2. Multi-State Data Structure (Based on your January/February reports)
data = {
    "State": ["MAHARASHTRA", "MAHARASHTRA", "MAHARASHTRA", "MAHARASHTRA", "GUJARAT", "GUJARAT", "MP/CG", "MP/CG"],
    "Zone": ["WEST-1", "WEST-2", "MUMBAI D2R", "PUNE D2R", "WEST-1", "WEST-2", "INDORE D2R", "BHOPAL HUB"],
    "Salesman": ["GURUNATH", "JULESH", "LAXMAN", "GIRISH", "FIROZ", "DINESH", "RAJESH", "VIKRAM"],
    "Watch_Sales": [15531000, 9399000, 1145000, 450000, 150000, 6000000, 2200000, 1800000],
    "Audio_Sales": [3800000, 3500000, 350000, 380000, 35000, 1500000, 950000, 750000],
    "Accessory_Sales": [360917, 455929, 65000, 24880, 4948, 221997, 45000, 32000]
}

df = pd.DataFrame(data)
df['Total_Revenue'] = df['Watch_Sales'] + df['Audio_Sales'] + df['Accessory_Sales']

# 3. Sidebar Navigation & Export
st.sidebar.header("Geography Filters")
selected_states = st.sidebar.multiselect("Select States", options=df["State"].unique(), default=df["State"].unique())
view_mode = st.sidebar.radio("View By:", ["Revenue", "Category Mix"])

# Filter Logic
filtered_df = df[df["State"].isin(selected_states)]

# --- FIXED EXPORT FEATURE ---
def to_excel(df_to_save):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_to_save.to_excel(writer, index=False, sheet_name='Sales_Report')
    return output.getvalue()

if not filtered_df.empty:
    excel_data = to_excel(filtered_df)
    st.sidebar.markdown("---")
    st.sidebar.download_button(
        label="📥 Download Excel Report",
        data=excel_data,
        file_name='Go_Noise_Regional_Report.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

# 4. Top KPIs
total_rev = filtered_df['Total_Revenue'].sum()
watch_share = (filtered_df['Watch_Sales'].sum() / total_rev) * 100 if total_rev > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("Selected Revenue", f"₹{total_rev:,}")
col2.metric("Watch Contribution", f"{watch_share:.1f}%")
col3.metric("Active Salesmen", len(filtered_df))

# 5. Visualizing the Three Hubs
st.markdown("---")
if view_mode == "Revenue":
    st.subheader("State-wise Revenue Comparison")
    fig_rev = px.bar(filtered_df.groupby("State")["Total_Revenue"].sum().reset_index(), 
                     x="State", y="Total_Revenue", color="State", 
                     color_discrete_sequence=['#2E4053', '#F4D03F', '#E74C3C'])
    st.plotly_chart(fig_rev, use_container_width=True)
else:
    st.subheader("Category Distribution by State")
    melted = filtered_df.melt(id_vars=["State"], value_vars=["Watch_Sales", "Audio_Sales", "Accessory_Sales"])
    fig_mix = px.bar(melted, x="State", y="value", color="variable", barmode="group",
                     labels={"variable": "Category", "value": "Billing Amt"})
    st.plotly_chart(fig_mix, use_container_width=True)

# 6. Detailed Leaderboard
st.subheader("🎖️ Regional Leaderboard")
st.dataframe(filtered_df.sort_values("Total_Revenue", ascending=False), use_container_width=True, hide_index=True)
