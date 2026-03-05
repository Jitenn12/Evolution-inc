import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# 1. Page Config
st.set_page_config(page_title="Evolution Inc. Master Dashboard", layout="wide")
st.title("🎧 Go Noise: 100% Salesman Roster & Category Intelligence")
st.caption("Reporting: Jan - Feb 2026 | All 4 Regions & All Salesmen Included")

# 2. MASTER DATASET (Every Salesman, Every Category, Qty & Value)
data = [
    # JANUARY DATA
    {"Month": "Jan", "Region": "WEST-1", "Lead": "GURUNATH", "W_Qty": 10398, "W_Val": 14456438, "A_Qty": 7228, "A_Val": 7011402, "Acc_Qty": 6, "Acc_Val": 6990},
    {"Month": "Jan", "Region": "WEST-1", "Lead": "J", "W_Qty": 6389, "W_Val": 10225496, "A_Qty": 5111, "A_Val": 4730444, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Jan", "Region": "WEST-1", "Lead": "FIROZ", "W_Qty": 38, "W_Val": 100534, "A_Qty": 13, "A_Val": 33783, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Jan", "Region": "WEST-1", "Lead": "J-CORP", "W_Qty": 1, "W_Val": 4750, "A_Qty": 20, "A_Val": 15680, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Jan", "Region": "WEST-2", "Lead": "DINESH", "W_Qty": 2690, "W_Val": 4345648, "A_Qty": 3052, "A_Val": 4479353, "Acc_Qty": 90, "Acc_Val": 175050},
    {"Month": "Jan", "Region": "WEST-2", "Lead": "JULESH", "W_Qty": 3654, "W_Val": 6491939, "A_Qty": 2326, "A_Val": 2846038, "Acc_Qty": 17, "Acc_Val": 19805},
    {"Month": "Jan", "Region": "MUMBAI D2R", "Lead": "LAXMAN", "W_Qty": 498, "W_Val": 1267414, "A_Qty": 439, "A_Val": 641890, "Acc_Qty": 1, "Acc_Val": 2067},
    {"Month": "Jan", "Region": "MUMBAI D2R", "Lead": "AMIT", "W_Qty": 269, "W_Val": 489864, "A_Qty": 143, "A_Val": 214900, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Jan", "Region": "MUMBAI D2R", "Lead": "NILESH", "W_Qty": 247, "W_Val": 408888, "A_Qty": 147, "A_Val": 166844, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Jan", "Region": "MUMBAI D2R", "Lead": "RAKESH", "W_Qty": 499, "W_Val": 948731, "A_Qty": 229, "A_Val": 356996, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Jan", "Region": "MUMBAI D2R", "Lead": "SANDEEP", "W_Qty": 414, "W_Val": 998770, "A_Qty": 417, "A_Val": 530527, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Jan", "Region": "MUMBAI D2R", "Lead": "TUKARAM", "W_Qty": 220, "W_Val": 364287, "A_Qty": 134, "A_Val": 171187, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Jan", "Region": "PUNE D2R", "Lead": "GIRISH", "W_Qty": 149, "W_Val": 333707, "A_Qty": 192, "A_Val": 360738, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Jan", "Region": "PUNE D2R", "Lead": "FIROZ", "W_Qty": 567, "W_Val": 934789, "A_Qty": 112, "A_Val": 103472, "Acc_Qty": 0, "Acc_Val": 0},
    
    # FEBRUARY DATA
    {"Month": "Feb", "Region": "WEST-1", "Lead": "GURUNATH", "W_Qty": 9844, "W_Val": 13182573, "A_Qty": 4922, "A_Val": 5021419, "Acc_Qty": 765, "Acc_Val": 1487925},
    {"Month": "Feb", "Region": "WEST-1", "Lead": "J", "W_Qty": 3345, "W_Val": 5527059, "A_Qty": 3668, "A_Val": 3486360, "Acc_Qty": 300, "Acc_Val": 577800},
    {"Month": "Feb", "Region": "WEST-1", "Lead": "FIROZ", "W_Qty": 63, "W_Val": 176951, "A_Qty": 3, "A_Val": 12997, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Feb", "Region": "WEST-1", "Lead": "J-CORP", "W_Qty": 42, "W_Val": 49974, "A_Qty": 275, "A_Val": 392490, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Feb", "Region": "WEST-2", "Lead": "DINESH", "W_Qty": 4744, "W_Val": 6273006, "A_Qty": 1308, "A_Val": 1338016, "Acc_Qty": 255, "Acc_Val": 417975},
    {"Month": "Feb", "Region": "WEST-2", "Lead": "JULESH", "W_Qty": 5731, "W_Val": 9013208, "A_Qty": 3068, "A_Val": 3190321, "Acc_Qty": 600, "Acc_Val": 1151400},
    {"Month": "Feb", "Region": "MUMBAI D2R", "Lead": "LAXMAN", "W_Qty": 533, "W_Val": 1117105, "A_Qty": 310, "A_Val": 412839, "Acc_Qty": 24, "Acc_Val": 35749},
    {"Month": "Feb", "Region": "MUMBAI D2R", "Lead": "AMIT", "W_Qty": 304, "W_Val": 471861, "A_Qty": 183, "A_Val": 210327, "Acc_Qty": 11, "Acc_Val": 22613},
    {"Month": "Feb", "Region": "MUMBAI D2R", "Lead": "RAKESH", "W_Qty": 498, "W_Val": 879009, "A_Qty": 170, "A_Val": 217197, "Acc_Qty": 24, "Acc_Val": 45216},
    {"Month": "Feb", "Region": "PUNE D2R", "Lead": "GIRISH", "W_Qty": 121, "W_Val": 321691, "A_Qty": 85, "A_Val": 94869, "Acc_Qty": 6, "Acc_Val": 12326},
    {"Month": "Feb", "Region": "PUNE D2R", "Lead": "FIROZ", "W_Qty": 172, "W_Val": 341024, "A_Qty": 85, "A_Val": 84970, "Acc_Qty": 0, "Acc_Val": 0}
]

df = pd.DataFrame(data)
df['Total_Billing'] = df['W_Val'] + df['A_Val'] + df['Acc_Val']
df['Total_Qty'] = df['W_Qty'] + df['A_Qty'] + df['Acc_Qty']

# 3. Sidebar Navigation & Global Filters
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

# 5. Category Deep-Dive View
elif view_mode == "Category Deep-Dive":
    st.header("📦 Product Breakup: Qty & ASP")
    cat = st.radio("Product Line:", ["Watch", "Audio", "Accessories"])
    val_map = {"Watch": "W_Val", "Audio": "A_Val", "Accessories": "Acc_Val"}
    qty_map = {"Watch": "W_Qty", "Audio": "A_Qty", "Accessories": "Acc_Qty"}
    
    # ASP Calculation
    filtered_df['ASP'] = filtered_df[val_map[cat]] / filtered_df[qty_map[cat]].replace(0, 1)
    
    fig_cat = px.bar(filtered_df, x="Lead", y=[qty_map[cat], val_map[cat]], barmode="group",
                    title=f"{cat} Category Analysis (Qty vs Value)")
    st.plotly_chart(fig_cat, use_container_width=True)
    st.write(f"### {cat} Leaderboard")
    st.dataframe(filtered_df[['Lead', 'Region', qty_map[cat], val_map[cat], 'ASP']], hide_index=True)

# 6. AI Predictive Insights
elif view_mode == "AI Predictive Insights":
    st.header("🔮 March Strategy & Growth Alerts")
    feb_df = df[df['Month'] == "Feb"].copy()
    feb_df['March_Target'] = feb_df['Total_Billing'] * 1.15
    
    st.success("✅ **Top Performer Alert:** JULESH (Gujarat) is leading in growth momentum.")
    st.warning("🚨 **Recovery Alert:** PUNE D2R needs immediate stock replenishment for Audio.")
    
    fig_pred = px.funnel(feb_df.sort_values("March_Target", ascending=False), y="Lead", x="March_Target", color="Region")
    st.plotly_chart(fig_pred, use_container_width=True)
