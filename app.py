import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# 1. Page Config & Indian Currency Function
st.set_page_config(page_title="Evolution Inc. Verified Dashboard", layout="wide")

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

st.title("🎧 Go Noise: Jan-Feb Verified Executive View")

# 2. MASTER DATASET (Jan & Feb 2026 - Every Salesman Included)
data = [
    # JANUARY 2026 (Verified Totals: 45,712 Qty | ₹6,32,40,530 Val)
    {"Month": "Jan", "Zone": "WEST-1", "Salesman": "FIROZ", "A_Qty": 13, "A_Val": 33783, "W_Qty": 38, "W_Val": 100534, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Jan", "Zone": "WEST-1", "Salesman": "GURUNATH", "A_Qty": 7228, "A_Val": 7011402, "W_Qty": 10398, "W_Val": 14456438, "Acc_Qty": 6, "Acc_Val": 6990},
    {"Month": "Jan", "Zone": "WEST-1", "Salesman": "J-CORP", "A_Qty": 20, "A_Val": 15680, "W_Qty": 1, "W_Val": 4750, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Jan", "Zone": "WEST-1", "Salesman": "J", "A_Qty": 5111, "A_Val": 4730444, "W_Qty": 6389, "W_Val": 10225496, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Jan", "Zone": "WEST-2", "Salesman": "DINESH", "A_Qty": 3052, "A_Val": 4479353, "W_Qty": 2690, "W_Val": 4345648, "Acc_Qty": 90, "Acc_Val": 175050},
    {"Month": "Jan", "Zone": "WEST-2", "Salesman": "JULESH", "A_Qty": 2326, "A_Val": 2846038, "W_Qty": 3654, "W_Val": 6491939, "Acc_Qty": 17, "Acc_Val": 19805},
    {"Month": "Jan", "Zone": "MUMBAI D2R", "Salesman": "LAXMAN", "A_Qty": 439, "A_Val": 641890, "W_Qty": 498, "W_Val": 1267414, "Acc_Qty": 1, "Acc_Val": 2067},
    {"Month": "Jan", "Zone": "MUMBAI D2R", "Salesman": "AMIT", "A_Qty": 143, "A_Val": 214900, "W_Qty": 269, "W_Val": 489864, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Jan", "Zone": "MUMBAI D2R", "Salesman": "NILESH", "A_Qty": 147, "A_Val": 166844, "W_Qty": 247, "W_Val": 408888, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Jan", "Zone": "MUMBAI D2R", "Salesman": "RAKESH", "A_Qty": 229, "A_Val": 356996, "W_Qty": 499, "W_Val": 948731, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Jan", "Zone": "MUMBAI D2R", "Salesman": "SANDEEP", "A_Qty": 417, "A_Val": 530527, "W_Qty": 414, "W_Val": 998770, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Jan", "Zone": "MUMBAI D2R", "Salesman": "TUKARAM", "A_Qty": 134, "A_Val": 171187, "W_Qty": 220, "W_Val": 364287, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Jan", "Zone": "MUMBAI D2R", "Salesman": "KALPESH", "A_Qty": 2, "A_Val": 2109, "W_Qty": 0, "W_Val": 0, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Jan", "Zone": "PUNE D2R", "Salesman": "FIROZ", "A_Qty": 112, "A_Val": 103472, "W_Qty": 567, "W_Val": 934789, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Jan", "Zone": "PUNE D2R", "Salesman": "GIRISH", "A_Qty": 192, "A_Val": 360738, "W_Qty": 149, "W_Val": 333707, "Acc_Qty": 0, "Acc_Val": 0},

    # FEBRUARY 2026 (Verified Totals: 42,970 Qty | ₹5,80,71,214 Val)
    {"Month": "Feb", "Zone": "WEST-1", "Salesman": "FIROZ", "A_Qty": 3, "A_Val": 12997, "W_Qty": 63, "W_Val": 176951, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Feb", "Zone": "WEST-1", "Salesman": "GURUNATH", "A_Qty": 4922, "A_Val": 5021419, "W_Qty": 9844, "W_Val": 13182573, "Acc_Qty": 765, "Acc_Val": 1487925},
    {"Month": "Feb", "Zone": "WEST-1", "Salesman": "J-CORP", "A_Qty": 275, "A_Val": 392490, "W_Qty": 42, "W_Val": 49974, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Feb", "Zone": "WEST-1", "Salesman": "J", "A_Qty": 3668, "A_Val": 3486360, "W_Qty": 3345, "W_Val": 5527059, "Acc_Qty": 300, "Acc_Val": 577800},
    {"Month": "Feb", "Zone": "WEST-2", "Salesman": "DINESH", "A_Qty": 1308, "A_Val": 1338016, "W_Qty": 4744, "W_Val": 6273006, "Acc_Qty": 255, "Acc_Val": 417975},
    {"Month": "Feb", "Zone": "WEST-2", "Salesman": "JULESH", "A_Qty": 3068, "A_Val": 3190321, "W_Qty": 5731, "W_Val": 9013208, "Acc_Qty": 600, "Acc_Val": 1151400},
    {"Month": "Feb", "Zone": "MUMBAI D2R", "Salesman": "LAXMAN", "A_Qty": 310, "A_Val": 412839, "W_Qty": 533, "W_Val": 1117105, "Acc_Qty": 24, "Acc_Val": 35749},
    {"Month": "Feb", "Zone": "MUMBAI D2R", "Salesman": "AMIT", "A_Qty": 183, "A_Val": 210327, "W_Qty": 304, "W_Val": 471861, "Acc_Qty": 11, "Acc_Val": 22613},
    {"Month": "Feb", "Zone": "MUMBAI D2R", "Salesman": "NILESH", "A_Qty": 168, "A_Val": 198607, "W_Qty": 281, "W_Val": 465939, "Acc_Qty": 13, "Acc_Val": 20707},
    {"Month": "Feb", "Zone": "MUMBAI D2R", "Salesman": "RAKESH", "A_Qty": 170, "A_Val": 217197, "W_Qty": 498, "W_Val": 879009, "Acc_Qty": 24, "Acc_Val": 45216},
    {"Month": "Feb", "Zone": "MUMBAI D2R", "Salesman": "SANDEEP", "A_Qty": 173, "A_Val": 201265, "W_Qty": 398, "W_Val": 883620, "Acc_Qty": 4, "Acc_Val": 8132},
    {"Month": "Feb", "Zone": "MUMBAI D2R", "Salesman": "TUKARAM", "A_Qty": 270, "A_Val": 347908, "W_Qty": 178, "W_Val": 290851, "Acc_Qty": 3, "Acc_Val": 6420},
    {"Month": "Feb", "Zone": "MUMBAI D2R", "Salesman": "J-MUM", "A_Qty": 13, "A_Val": 56680, "W_Qty": 0, "W_Val": 0, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Feb", "Zone": "MUMBAI D2R", "Salesman": "KALPESH", "A_Qty": 3, "A_Val": 3224, "W_Qty": 6, "W_Val": 20309, "Acc_Qty": 1, "Acc_Val": 1282},
    {"Month": "Feb", "Zone": "PUNE D2R", "Salesman": "FIROZ-P", "A_Qty": 85, "A_Val": 84970, "W_Qty": 172, "W_Val": 341024, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Feb", "Zone": "PUNE D2R", "Salesman": "GIRISH", "A_Qty": 85, "A_Val": 94869, "W_Qty": 121, "W_Val": 321691, "Acc_Qty": 6, "Acc_Val": 12326}
]

df = pd.DataFrame(data)

# 3. SIDEBAR CONTROLS
st.sidebar.title("🛠️ Analysis Tools")
month_select = st.sidebar.multiselect("Select Months:", df['Month'].unique(), default=["Jan", "Feb"])
cat_select = st.sidebar.multiselect("Select Categories:", ["Audio", "Watch", "Accessories"], default=["Audio", "Watch", "Accessories"])

# 4. FILTERING LOGIC
filtered_df = df[df['Month'].isin(month_select)]

v_sum, q_sum = 0, 0
if "Audio" in cat_select:
    v_sum += filtered_df['A_Val'].sum(); q_sum += filtered_df['A_Qty'].sum()
if "Watch" in cat_select:
    v_sum += filtered_df['W_Val'].sum(); q_sum += filtered_df['W_Qty'].sum()
if "Accessories" in cat_select:
    v_sum += filtered_df['Acc_Val'].sum(); q_sum += filtered_df['Acc_Qty'].sum()

# 5. HEADER KPI
st.header(f"📊 Dashboard: {', '.join(month_select)}")
c1, c2 = st.columns(2)
c1.metric("Selected Revenue", format_indian(v_sum))
c2.metric("Total Qty (Thousands)", f"{q_sum / 1000:.2f} K")

# 6. CHARTING
fig = px.bar(filtered_df, x="Salesman", y=[(c[0] + "_Val") for c in cat_select], 
             color="Month", barmode="group", title="Category Performance by Salesman")
fig.update_layout(yaxis_title="Billing (₹)")
st.plotly_chart(fig, use_container_width=True)

# 7. DATA SHEET
st.subheader("📋 Master Sales Sheet")
st.dataframe(filtered_df, use_container_width=True, hide_index=True)
