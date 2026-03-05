import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="Evolution Inc. Multi-Filter Dashboard", layout="wide")

# Indian Currency Formatter
def format_indian_currency(number):
    s = str(int(number))
    if len(s) <= 3: return "₹" + s
    last_three = s[-3:]
    other_numbers = s[:-3]
    res = ""
    while len(other_numbers) > 2:
        res = "," + other_numbers[-2:] + res
        other_numbers = other_numbers[:-2]
    return "₹" + other_numbers + res + "," + last_three

# 2. MASTER DATASET (Jan, Feb, Mar)
data = [
    # JANUARY 2026
    {"Month": "Jan", "Zone": "WEST-1", "Salesman": "GURUNATH", "Audio_Qty": 7228, "Audio_Val": 7011402, "Watch_Qty": 10398, "Watch_Val": 14456438, "Acc_Qty": 6, "Acc_Val": 6990},
    {"Month": "Jan", "Zone": "WEST-2", "Salesman": "DINESH", "Audio_Qty": 3052, "Audio_Val": 4479353, "Watch_Qty": 2690, "Watch_Val": 4345648, "Acc_Qty": 90, "Acc_Val": 175050},
    # FEBRUARY 2026
    {"Month": "Feb", "Zone": "WEST-1", "Salesman": "GURUNATH", "Audio_Qty": 4922, "Audio_Val": 5021419, "Watch_Qty": 9844, "Watch_Val": 13182573, "Acc_Qty": 765, "Acc_Val": 1487925},
    {"Month": "Feb", "Zone": "WEST-2", "Salesman": "JULESH", "Audio_Qty": 3068, "Audio_Val": 3190321, "Watch_Qty": 5731, "Watch_Val": 9013208, "Acc_Qty": 600, "Acc_Val": 1151400},
    # MARCH 2026
    {"Month": "Mar", "Zone": "WEST-1", "Salesman": "GURUNATH", "Audio_Qty": 145, "Audio_Val": 258923, "Watch_Qty": 363, "Watch_Val": 733713, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Mar", "Zone": "PUNE D2R", "Salesman": "FIROZ", "Audio_Qty": 200, "Audio_Val": 156000, "Watch_Qty": 0, "Watch_Val": 0, "Acc_Qty": 20, "Acc_Val": 44800}
    # ... (Include all other salesmen here as per your previous verified list)
]

df = pd.DataFrame(data)

# 3. SIDEBAR FILTERS
st.sidebar.title("🛠️ Dashboard Filters")

# Month Filter
month_selection = st.sidebar.multiselect("Select Months:", df['Month'].unique(), default=["Feb", "Mar"])

# Category Filter
cat_selection = st.sidebar.multiselect("Select Category:", ["Audio", "Watch", "Accessories"], default=["Audio", "Watch"])

# Zone Filter
zone_selection = st.sidebar.multiselect("Select Zones:", df['Zone'].unique(), default=df['Zone'].unique())

# 4. DATA PROCESSING
filtered_df = df[(df['Month'].isin(month_selection)) & (df['Zone'].isin(zone_selection))]

# Calculate dynamic totals based on category selection
total_val = 0
total_qty = 0

if "Audio" in cat_selection:
    total_val += filtered_df['Audio_Val'].sum()
    total_qty += filtered_df['Audio_Qty'].sum()
if "Watch" in cat_selection:
    total_val += filtered_df['Watch_Val'].sum()
    total_qty += filtered_df['Watch_Qty'].sum()
if "Accessories" in cat_selection:
    total_val += filtered_df['Acc_Val'].sum()
    total_qty += filtered_df['Acc_Val'].sum()

# 5. DASHBOARD DISPLAY
st.header(f"📊 Performance Overview: {', '.join(month_selection)}")

c1, c2 = st.columns(2)
# Billing in Lakh/Crore Format
c1.metric("Selected Billing Value", format_indian_currency(total_val))
# Qty in Thousands Format
c2.metric("Selected Qty (in '000s)", f"{total_qty / 1000:.2f} K")

st.markdown("---")

# Chart with dynamic y-axis
fig = px.bar(filtered_df, x="Salesman", y=[c + "_Val" for c in cat_selection if c + "_Val" in filtered_df.columns], 
             color="Month", barmode="group", title="Category Performance by Salesman")

fig.update_layout(yaxis_title="Billing (₹)")
st.plotly_chart(fig, use_container_width=True)

# Data Explorer
st.subheader("📋 Filtered Sales Roster")
st.dataframe(filtered_df, use_container_width=True, hide_index=True)
