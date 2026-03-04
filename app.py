import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Go Noise Growth Intelligence", layout="wide")
st.title("🎧 Go Noise: Product Category Growth")
st.caption("Strategic Trend Analysis: Jan vs Feb 2026")

# 2. Data with Category Breakdown (Corrected Figures)
data = {
    "Month": ["Jan", "Jan", "Jan", "Jan", "Jan", "Feb", "Feb", "Feb", "Feb", "Feb"],
    "Lead/Entity": ["GURUNATH", "DINESH", "JULESH", "MUMBAI-D2R", "PUNE-D2R", 
                   "GURUNATH", "DINESH", "JULESH", "MUMBAI-D2R", "PUNE-D2R"],
    "Region": ["MAHARASHTRA", "MP/CG", "GUJARAT", "MUMBAI D2R", "PUNE D2R",
               "MAHARASHTRA", "MP/CG", "GUJARAT", "MUMBAI D2R", "PUNE D2R"],
    "Watch_Sales": [15531000, 6200000, 6500000, 4128694, 662715, 13182573, 5800000, 9500000, 3900000, 420000],
    "Audio_Sales": [5582913, 2500000, 2400000, 2370780, 1045111, 6017427, 2000000, 3400000, 1951860, 410000],
    "Accessory_Sales": [360917, 300051, 457782, 65000, 24880, 491917, 228997, 454929, 65000, 24880]
}
df = pd.DataFrame(data)

# 3. Growth Calculation Logic
df_jan = df[df['Month'] == "Jan"].groupby('Month').sum(numeric_only=True)
df_feb = df[df['Month'] == "Feb"].groupby('Month').sum(numeric_only=True)

watch_growth = ((df_feb['Watch_Sales'].values[0] - df_jan['Watch_Sales'].values[0]) / df_jan['Watch_Sales'].values[0]) * 100
audio_growth = ((df_feb['Audio_Sales'].values[0] - df_jan['Audio_Sales'].values[0]) / df_jan['Audio_Sales'].values[0]) * 100
acc_growth = ((df_feb['Accessory_Sales'].values[0] - df_jan['Accessory_Sales'].values[0]) / df_jan['Accessory_Sales'].values[0]) * 100

# 4. KPI Growth Ribbon
st.header("📈 Overall Category Growth (MoM)")
c1, c2, c3 = st.columns(3)
c1.metric("Watch Growth", f"{watch_growth:.1f}%", delta=f"{watch_growth:.1f}%")
c2.metric("Audio Growth", f"{audio_growth:.1f}%", delta=f"{audio_growth:.1f}%")
c3.metric("Accessories Growth", f"{acc_growth:.1f}%", delta=f"{acc_growth:.1f}%")

st.markdown("---")

# 5. Visualizing Lead-wise Category Trends
st.subheader("Category Performance Shift by Lead")
view_cat = st.radio("Select Category to Analyze Trend:", ["Watch_Sales", "Audio_Sales", "Accessory_Sales"])

fig_trend = px.bar(df, x="Lead/Entity", y=view_cat, color="Month", barmode="group",
                   title=f"{view_cat} Comparison by Territory",
                   color_discrete_map={'Jan': '#2E4053', 'Feb': '#F4D03F'}, text_auto='.2s')
st.plotly_chart(fig_trend, use_container_width=True)

# 6. AI Strategic Table (Growth Detail)
st.subheader("📋 Detailed Growth Table")
# Creating a growth view per lead
leads = df['Lead/Entity'].unique()
lead_growth_list = []
for lead in leads:
    l_jan = df[(df['Lead/Entity'] == lead) & (df['Month'] == "Jan")].iloc[0]
    l_feb = df[(df['Lead/Entity'] == lead) & (df['Month'] == "Feb")].iloc[0]
    lead_growth_list.append({
        "Lead": lead,
        "Watch Growth %": ((l_feb['Watch_Sales'] - l_jan['Watch_Sales']) / l_jan['Watch_Sales']) * 100,
        "Audio Growth %": ((l_feb['Audio_Sales'] - l_jan['Audio_Sales']) / l_jan['Audio_Sales']) * 100
    })

st.dataframe(pd.DataFrame(lead_growth_list), hide_index=True, use_container_width=True)
