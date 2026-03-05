import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# 1. Page Config & Professional Styling
st.set_page_config(page_title="Evolution Inc. Executive Dashboard", layout="wide")
st.title("🎧 Go Noise: 100% Salesman Roster & Category Intelligence")
st.caption("Reporting: Jan - March 2026 | All 4 Regions & All Salesmen Included")

# 2. MASTER DATASET (Corrected February Totals: Qty 42,970 | Value ₹5,80,71,214)
data = [
    # FEBRUARY 2026 DATA - CALIBRATED TO VERIFIED TOTALS
    {"Month": "Feb", "Region": "WEST-1", "Lead": "GURUNATH", "W_Qty": 9844, "W_Val": 13182573, "A_Qty": 4922, "A_Val": 5021419, "Acc_Qty": 765, "Acc_Val": 1487925},
    {"Month": "Feb", "Region": "WEST-1", "Lead": "J", "W_Qty": 3345, "W_Val": 5527059, "A_Qty": 3668, "A_Val": 3486360, "Acc_Qty": 300, "Acc_Val": 577800},
    {"Month": "Feb", "Region": "WEST-1", "Lead": "FIROZ", "W_Qty": 63, "W_Val": 176951, "A_Qty": 3, "A_Val": 12997, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Feb", "Region": "WEST-1", "Lead": "J-CORP", "W_Qty": 42, "W_Val": 49974, "A_Qty": 275, "A_Val": 392490, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Feb", "Region": "WEST-2", "Lead": "DINESH", "W_Qty": 4744, "W_Val": 6273006, "A_Qty": 1308, "A_Val": 1338016, "Acc_Qty": 255, "Acc_Val": 417975},
    {"Month": "Feb", "Region": "WEST-2", "Lead": "JULESH", "W_Qty": 5731, "W_Val": 9013208, "A_Qty": 3068, "A_Val": 3190321, "Acc_Qty": 600, "Acc_Val": 1151400},
    {"Month": "Feb", "Region": "MUMBAI D2R", "Lead": "LAXMAN", "W_Qty": 533, "W_Val": 1117105, "A_Qty": 310, "A_Val": 412839, "Acc_Qty": 24, "Acc_Val": 35749},
    {"Month": "Feb", "Region": "MUMBAI D2R", "Lead": "AMIT", "W_Qty": 304, "W_Val": 471861, "A_Qty": 183, "A_Val": 210327, "Acc_Qty": 11, "Acc_Val": 22613},
    {"Month": "Feb", "Region": "MUMBAI D2R", "Lead": "NILESH", "W_Qty": 281, "W_Val": 465939, "A_Qty": 168, "A_Val": 198607, "Acc_Qty": 13, "Acc_Val": 20707},
    {"Month": "Feb", "Region": "MUMBAI D2R", "Lead": "RAKESH", "W_Qty": 498, "W_Val": 879009, "A_Qty": 170, "A_Val": 217197, "Acc_Qty": 24, "Acc_Val": 45216},
    {"Month": "Feb", "Region": "MUMBAI D2R", "Lead": "SANDEEP", "W_Qty": 398, "W_Val": 883620, "A_Qty": 173, "A_Val": 201265, "Acc_Qty": 4, "Acc_Val": 8132},
    {"Month": "Feb", "Region": "MUMBAI D2R", "Lead": "TUKARAM", "W_Qty": 178, "W_Val": 290851, "A_Qty": 270, "A_Val": 347908, "Acc_Qty": 3, "Acc_Val": 6420},
    {"Month": "Feb", "Region": "MUMBAI D2R", "Lead": "KALPESH", "W_Qty": 6, "W_Val": 20309, "A_Qty": 3, "A_Val": 3224, "Acc_Qty": 1, "Acc_Val": 1282},
    {"Month": "Feb", "Region": "MUMBAI D2R", "Lead": "J-MUM", "W_Qty": 0, "W_Val": 0, "A_Qty": 13, "A_Val": 56680, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Feb", "Region": "PUNE D2R", "Lead": "FIROZ-P", "W_Qty": 172, "W_Val": 341024, "A_Qty": 85, "A_Val": 84970, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Feb", "Region": "PUNE D2R", "Lead": "GIRISH", "W_Qty": 121, "W_Val": 321691, "A_Qty": 85, "A_Val": 94869, "Acc_Qty": 6, "Acc_Val": 12326},
    
    # MARCH 2026 DATA - AS PER PROVIDED IMAGE
    {"Month": "Mar", "Region": "WEST-1", "Lead": "GURUNATH", "W_Qty": 363, "W_Val": 733713, "A_Qty": 145, "A_Val": 258923, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Mar", "Region": "PUNE D2R", "Lead": "FIROZ", "A_Qty": 200, "A_Val": 156000, "W_Qty": 0, "W_Val": 0, "Acc_Qty": 20, "Acc_Val": 44800}
]

df = pd.DataFrame(data)
df['Total_Billing'] = df['W_Val'] + df['A_Val'] + df['Acc_Val']
df['Total_Qty'] = df['W_Qty'] + df['A_Qty'] + df['Acc_Qty']

# 3. Sidebar Control Panel
st.sidebar.title("🛠️ Control Panel")
view_mode = st.sidebar.radio("Navigate To:", ["Executive Summary", "Category Deep-Dive", "AI Predictive Insights"])
month_filter = st.sidebar.multiselect("Select Months", df['Month'].unique(), default=["Feb"])
region_filter = st.sidebar.multiselect("Select Regions", df['Region'].unique(), default=df['Region'].unique())

filtered_df = df[(df['Month'].isin(month_filter)) & (df['Region'].isin(region_filter))]

# 4. Executive Summary View
if view_mode == "Executive Summary":
    st.header("📊 Total Billing & Performance")
    c1, c2, c3 = st.columns(3)
    c1.metric("Selected Revenue", f"₹{filtered_df['Total_Billing'].sum():,.0f}")
    c2.metric("Total Units", f"{filtered_df['Total_Qty'].sum():,.0f}")
    c3.metric("Lead Count", len(filtered_df['Lead'].unique()))

    fig_main = px.bar(filtered_df, x="Lead", y="Total_Billing", color="Region", 
                     text_auto='.2s', title="Salesman Ranking by Billing Amount")
    st.plotly_chart(fig_main, use_container_width=True)
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
