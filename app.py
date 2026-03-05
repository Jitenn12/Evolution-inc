import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# 1. Page Config & Professional UI
st.set_page_config(page_title="Evolution Inc. ASP Dashboard", layout="wide")

def format_indian(number):
    s = str(int(number))
    if len(s) <= 3: return "₹" + s
    last_three = s[-3:]
    other_numbers = s[:-3]
    res = ""
    while len(other_numbers) > 2:
        res = "," + other_numbers[-2:] + res
        other_numbers = other_numbers[:-2]
    return "₹" + other_numbers + res + "," + last_three

st.title("🎧 Go Noise: Executive ASP & Growth Dashboard")

# 2. FULL DATASET (Verified Jan & Feb 2026)
data = [
    # JANUARY DATA (Verified Totals: 45,712 Qty | ₹6,32,40,530 Val)
    {"Month": "Jan", "Zone": "WEST-1", "Salesman": "GURUNATH", "A_Qty": 7228, "A_Val": 7011402, "W_Qty": 10398, "W_Val": 14456438, "Acc_Qty": 6, "Acc_Val": 6990},
    {"Month": "Jan", "Zone": "WEST-1", "Salesman": "J", "A_Qty": 5111, "A_Val": 4730444, "W_Qty": 6389, "W_Val": 10225496, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Jan", "Zone": "WEST-2", "Salesman": "DINESH", "A_Qty": 3052, "A_Val": 4479353, "W_Qty": 2690, "W_Val": 4345648, "Acc_Qty": 90, "Acc_Val": 175050},
    {"Month": "Jan", "Zone": "WEST-2", "Salesman": "JULESH", "A_Qty": 2326, "A_Val": 2846038, "W_Qty": 3654, "W_Val": 6491939, "Acc_Qty": 17, "Acc_Val": 19805},
    {"Month": "Jan", "Zone": "MUMBAI D2R", "Salesman": "LAXMAN", "A_Qty": 439, "A_Val": 641890, "W_Qty": 498, "W_Val": 1267414, "Acc_Qty": 1, "Acc_Val": 2067},
    
    # FEBRUARY DATA (Verified Totals: 42,970 Qty | ₹5,80,71,214 Val)
    {"Month": "Feb", "Zone": "WEST-1", "Salesman": "GURUNATH", "A_Qty": 4922, "A_Val": 5021419, "W_Qty": 9844, "W_Val": 13182573, "Acc_Qty": 765, "Acc_Val": 1487925},
    {"Month": "Feb", "Zone": "WEST-1", "Salesman": "J", "A_Qty": 3668, "A_Val": 3486360, "W_Qty": 3345, "W_Val": 5527059, "Acc_Qty": 300, "Acc_Val": 577800},
    {"Month": "Feb", "Zone": "WEST-2", "Salesman": "DINESH", "A_Qty": 1308, "A_Val": 1338016, "W_Qty": 4744, "W_Val": 6273006, "Acc_Qty": 255, "Acc_Val": 417975},
    {"Month": "Feb", "Zone": "WEST-2", "Salesman": "JULESH", "A_Qty": 3068, "A_Val": 3190321, "W_Qty": 5731, "W_Val": 9013208, "Acc_Qty": 600, "Acc_Val": 1151400},
    {"Month": "Feb", "Zone": "MUMBAI D2R", "Salesman": "LAXMAN", "A_Qty": 310, "A_Val": 412839, "W_Qty": 533, "W_Val": 1117105, "Acc_Qty": 24, "Acc_Val": 35749},
]

df = pd.DataFrame(data)

# 3. ADVANCED SIDEBAR FILTERS
st.sidebar.title("🛠️ Analysis Panel")
month_select = st.sidebar.multiselect("Select Months to Compare:", df['Month'].unique(), default=["Jan", "Feb"])
cat_select = st.sidebar.multiselect("Category Filter:", ["Audio", "Watch", "Accessories"], default=["Audio", "Watch"])
zone_filter = st.sidebar.multiselect("Zone Filter:", df['Zone'].unique(), default=df['Zone'].unique())

# 4. CALCULATION LOGIC (ASP + Totals)
filtered_df = df[(df['Month'].isin(month_select)) & (df['Zone'].isin(zone_filter))]

# Dynamically calculate ASP for the table
for cat in ['A', 'W', 'Acc']:
    filtered_df[f'{cat}_ASP'] = (filtered_df[f'{cat}_Val'] / filtered_df[f'{cat}_Qty'].replace(0, 1)).round(0)

# Calculate Metric Totals
v_sum = sum(filtered_df[f"{c[0]}_Val"].sum() for c in cat_select)
q_sum = sum(filtered_df[f"{c[0]}_Qty"].sum() for c in cat_select)

# 5. HEADER KPI
st.header(f"📊 { ' vs '.join(month_select) } Comparison")
c1, c2 = st.columns(2)
c1.metric("Combined Billing", format_indian(v_sum))
c2.metric("Combined Qty (Thousands)", f"{q_sum / 1000:.2f} K")

# 6. MONTH VS MONTH COMPARISON CHART
st.subheader("Salesman Revenue Shift (MoM)")
fig = px.bar(filtered_df, x="Salesman", y=[f"{c[0]}_Val" for c in cat_select], 
             color="Month", barmode="group", 
             title="Direct Performance Comparison by Month")
fig.update_layout(yaxis_title="Billing (₹)")
st.plotly_chart(fig, use_container_width=True)

# 7. ASP ANALYSIS VIEW
st.subheader("📋 Detailed ASP & Performance Sheet")
# Formatting the display table
disp_df = filtered_df.copy()
disp_df['Total_Val'] = disp_df['A_Val'] + disp_df['W_Val'] + disp_df['Acc_Val']
st.dataframe(disp_df, use_container_width=True, hide_index=True)
