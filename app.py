import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# 1. Page Config & Indian Currency Function
st.set_page_config(page_title="Evolution Inc. 3-Month Dashboard", layout="wide")

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

st.title("🎧 Go Noise: Jan-Feb-Mar Executive View")

# 2. THE COMPLETE MASTER DATASET (Jan, Feb, Mar 2026)
data = [
    # JANUARY 2026 DATA (From 1000759407.jpg)
    {"Month": "Jan", "Zone": "WEST-1", "Salesman": "GURUNATH", "A_Qty": 7228, "A_Val": 7011402, "W_Qty": 10398, "W_Val": 14456438, "Acc_Qty": 6, "Acc_Val": 6990},
    {"Month": "Jan", "Zone": "WEST-1", "Salesman": "J", "A_Qty": 5111, "A_Val": 4730444, "W_Qty": 6389, "W_Val": 10225496, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Jan", "Zone": "WEST-2", "Salesman": "DINESH", "A_Qty": 3052, "A_Val": 4479353, "W_Qty": 2690, "W_Val": 4345648, "Acc_Qty": 90, "Acc_Val": 175050},
    {"Month": "Jan", "Zone": "WEST-2", "Salesman": "JULESH", "A_Qty": 2326, "A_Val": 2846038, "W_Qty": 3654, "W_Val": 6491939, "Acc_Qty": 17, "Acc_Val": 19805},
    {"Month": "Jan", "Zone": "MUMBAI D2R", "Salesman": "LAXMAN", "A_Qty": 439, "A_Val": 641890, "W_Qty": 498, "W_Val": 1267414, "Acc_Qty": 1, "Acc_Val": 2067},
    {"Month": "Jan", "Zone": "MUMBAI D2R", "Salesman": "AMIT", "A_Qty": 143, "A_Val": 214900, "W_Qty": 269, "W_Val": 489864, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Jan", "Zone": "PUNE D2R", "Salesman": "GIRISH", "A_Qty": 192, "A_Val": 360738, "W_Qty": 149, "W_Val": 333707, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Jan", "Zone": "PUNE D2R", "Salesman": "FIROZ", "A_Qty": 112, "A_Val": 103472, "W_Qty": 567, "W_Val": 934789, "Acc_Qty": 0, "Acc_Val": 0},

    # FEBRUARY 2026 DATA (From 1000792346.jpg)
    {"Month": "Feb", "Zone": "WEST-1", "Salesman": "GURUNATH", "A_Qty": 4922, "A_Val": 5021419, "W_Qty": 9844, "W_Val": 13182573, "Acc_Qty": 765, "Acc_Val": 1487925},
    {"Month": "Feb", "Zone": "WEST-1", "Salesman": "J", "A_Qty": 3668, "A_Val": 3486360, "W_Qty": 3345, "W_Val": 5527059, "Acc_Qty": 300, "Acc_Val": 577800},
    {"Month": "Feb", "Zone": "WEST-2", "Salesman": "JULESH", "A_Qty": 3068, "A_Val": 3190321, "W_Qty": 5731, "W_Val": 9013208, "Acc_Qty": 600, "Acc_Val": 1151400},
    {"Month": "Feb", "Zone": "MUMBAI D2R", "Salesman": "LAXMAN", "A_Qty": 310, "A_Val": 412839, "W_Qty": 533, "W_Val": 1117105, "Acc_Qty": 24, "Acc_Val": 35749},

    # MARCH 2026 DATA (From 1000798270.jpg)
    {"Month": "Mar", "Zone": "WEST-1", "Salesman": "GURUNATH", "A_Qty": 145, "A_Val": 258923, "W_Qty": 363, "W_Val": 733713, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Mar", "Zone": "PUNE D2R", "Salesman": "FIROZ", "A_Qty": 200, "A_Val": 156000, "W_Qty": 0, "W_Val": 0, "Acc_Qty": 20, "Acc_Val": 44800}
]

df = pd.DataFrame(data)
df['Total_Val'] = df['A_Val'] + df['W_Val'] + df['Acc_Val']
df['Total_Qty'] = df['A_Qty'] + df['W_Qty'] + df['Acc_Qty']

# 3. SIDEBAR TOOLS
st.sidebar.title("🛠️ Control Panel")
month_select = st.sidebar.multiselect("Select Months:", df['Month'].unique(), default=["Jan", "Feb", "Mar"])
zone_select = st.sidebar.multiselect("Select Zones:", df['Zone'].unique(), default=df['Zone'].unique())

# Excel Export
def to_excel(df_to_save):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_to_save.to_excel(writer, index=False, sheet_name='Sales_Report')
    return output.getvalue()

st.sidebar.markdown("---")
excel_data = to_excel(df[df['Month'].isin(month_select)])
st.sidebar.download_button(label="📥 Download Excel", data=excel_data, file_name='Evolution_Report.xlsx')

# 4. DASHBOARD HEADER & KPI
filtered_df = df[(df['Month'].isin(month_select)) & (df['Zone'].isin(zone_select))]

c1, c2 = st.columns(2)
c1.metric("Selected Revenue", format_indian(filtered_df['Total_Val'].sum()))
c2.metric("Total Units (Thousands)", f"{filtered_df['Total_Qty'].sum() / 1000:.2f} K")

# 5. CHARTS
fig = px.bar(filtered_df, x="Salesman", y="Total_Val", color="Month", barmode="group",
             title="Monthly Performance Comparison")
fig.update_layout(yaxis_title="Billing (₹)")
st.plotly_chart(fig, use_container_width=True)

# 6. DATA TABLE
st.subheader("📋 Master Sales Sheet")
st.dataframe(filtered_df, use_container_width=True, hide_index=True)
