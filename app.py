import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Go Noise Strategy Engine", layout="wide")
st.title("🎧 Go Noise: Executive Strategy & Trends")
st.caption("Verified Data: Guru (MH) | Dinesh (MPCG) | Julesh (GJ) | D2R Units")

# 2. Corrected Historical Data (Direct from your uploaded reports)
data = {
    "Month": ["Jan", "Jan", "Jan", "Jan", "Jan", "Feb", "Feb", "Feb", "Feb", "Feb"],
    "Lead": ["GURUNATH", "DINESH", "JULESH", "MUMBAI-D2R", "PUNE-D2R", 
             "GURUNATH", "DINESH", "JULESH", "MUMBAI-D2R", "PUNE-D2R"],
    "Revenue": [21474830, 9000051, 9357782, 6564474, 1732706, 
                19691917, 8028997, 13354929, 5916860, 854880]
}
df = pd.DataFrame(data)

# 3. Trend Calculations
df_jan = df[df['Month'] == "Jan"].set_index('Lead')
df_feb = df[df['Month'] == "Feb"].set_index('Lead')
growth = ((df_feb['Revenue'] - df_jan['Revenue']) / df_jan['Revenue']) * 100

# 4. AI Strategic Analysis
st.header("🧠 AI Market Strategy")
col_s1, col_s2 = st.columns(2)

with col_s1:
    st.success(f"📈 **Expansion Strategy (JULESH):** With a 42.7% growth, Gujarat is your 'Power Hub'. Recommendation: Increase stock allocation for premium Watches here.")
    st.warning(f"📉 **Retention Strategy (GURUNATH):** A -8.3% dip in Maharashtra suggests market fatigue. Action: Launch 'Audio Combo' offers to revive volume.")

with col_s2:
    st.error(f"🚨 **Recovery Strategy (PUNE D2R):** A -50.6% crash is critical. Action: Review distributor 'GIRISH' and check for local competitor aggression.")
    st.info(f"⚖️ **Stability Strategy (DINESH):** -10.8% in MPCG. Action: Focus on maintaining ASP above ₹1,600 to protect margins during the dip.")

# 5. Visual Trends
st.markdown("---")
st.subheader("Revenue Velocity: Jan vs Feb")
fig = px.bar(df, x="Lead", y="Revenue", color="Month", barmode="group",
             color_discrete_map={'Jan': '#2E4053', 'Feb': '#F4D03F'}, text_auto='.2s')
st.plotly_chart(fig, use_container_width=True)

# 6. Detailed Leaderboard
st.subheader("🎖️ Territory Leaderboard (February)")
feb_df = df_feb.copy()
feb_df['Growth_%'] = growth
st.dataframe(feb_df.sort_values("Revenue", ascending=False), use_container_width=True)
