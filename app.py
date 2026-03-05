import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# 1. Page Config & Indian Number Formatting
st.set_page_config(page_title="Evolution Inc. Executive Dashboard", layout="wide")

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

st.title("🎧 Go Noise: Interactive Sales Intelligence")

# 2. MASTER DATASET (Jan, Feb, Mar 2026 - Every Salesman Included)
data = [
    # FEBRUARY 2026 (Verified Totals from 1000792346.jpg)
    {"Month": "Feb", "Zone": "WEST-1", "Salesman": "GURUNATH", "A_Qty": 4922, "A_Val": 5021419, "W_Qty": 9844, "W_Val": 13182573, "Acc_Qty": 765, "Acc_Val": 1487925},
    {"Month": "Feb", "Zone": "WEST-1", "Salesman": "J", "A_Qty": 3668, "A_Val": 3486360, "W_Qty": 3345, "W_Val": 5527059, "Acc_Qty": 300, "Acc_Val": 577800},
    {"Month": "Feb", "Zone": "WEST-1", "Salesman": "FIROZ", "A_Qty": 3, "A_Val": 12997, "W_Qty": 63, "W_Val": 176951, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Feb", "Zone": "WEST-1", "Salesman": "J-CORP", "A_Qty": 275, "A_Val": 392490, "W_Qty": 42, "W_Val": 49974, "Acc_Qty": 0, "Acc_Val": 0},
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
    {"Month": "Feb", "Zone": "PUNE D2R", "Salesman": "GIRISH", "A_Qty": 85, "A_Val": 94869, "W_Qty": 121, "W_Val": 321691, "Acc_Qty": 6, "Acc_Val": 12326},

    # MARCH 2026 DATA (From 1000798270.jpg)
    {"Month": "Mar", "Zone": "WEST-1", "Salesman": "GURUNATH", "A_Qty": 145, "A_Val": 258923, "W_Qty": 363, "W_Val": 733713, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Mar", "Zone": "PUNE D2R", "Salesman": "FIROZ", "A_Qty": 200, "A_Val": 156000, "W_Qty": 0, "W_Val": 0, "Acc_Qty": 20, "Acc_Val": 44800},
]

df = pd.DataFrame(data)
df['Total_Val'] = df['A_Val'] + df['W_Val'] + df['Acc_Val']
df['Total_Qty'] = df['A_Qty'] + df['W_Qty'] + df['Acc_Qty']

# 3. SIDEBAR FILTERS (Interactive Controls)
st.sidebar.title("🛠️ Analysis Tools")
month_select = st.sidebar.multiselect("Select Months:", df['Month'].unique(), default=["Feb"])
cat_select = st.sidebar.multiselect("Select Categories:", ["Audio", "Watch", "Accessories"], default=["Audio", "Watch", "Accessories"])

# Excel Export Feature
def to_excel(df_to_save):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_to_save.to_excel(writer, index=False, sheet_name='Sales_Report')
    return output.getvalue()

st.sidebar.markdown("---")
excel_data = to_excel(df[df['Month'].isin(month_select)])
st.sidebar.download_button(label="📥 Download Excel Report", data=excel_data, file_name='Go_Noise_Report.xlsx')

# 4. DASHBOARD LOGIC & DISPLAY
filtered_df = df[df['Month'].isin(month_select)]

# Calculate dynamic totals based on category selection
v_sum, q_sum = 0, 0
if "Audio" in cat_select:
    v_sum += filtered_df['A_Val'].sum(); q_sum += filtered_df['A_Qty'].sum()
if "Watch" in cat_select:
    v_sum += filtered_df['W_Val'].sum(); q_sum += filtered_df['W_Qty'].sum()
if "Accessories" in cat_select:
    v_sum += filtered_df['Acc_Val'].sum(); q_sum += filtered_df['Acc_Qty'].sum()

c1, c2 = st.columns(2)
c1.metric("Selected Revenue", format_indian(v_sum))
c2.metric("Total Qty (Thousands)", f"{q_sum / 1000:.2f} K")

# 5. CHARTING (Showing all salesman ranking)
fig = px.bar(filtered_df, x="Salesman", y="Total_Val", color="Zone", text_auto='.2s', title="Salesman Ranking (Billing Amount)")
fig.update_layout(yaxis_title="Billing (₹)")
st.plotly_chart(fig, use_container_width=True)

# 6. MASTER DATA SHEET
st.subheader("📋 Master Sales Sheet")
st.dataframe(filtered_df, use_container_width=True, hide_index=True)
