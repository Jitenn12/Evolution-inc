import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config & Professional Branding
st.set_page_config(page_title="Evolution Inc. Category Dashboard", layout="wide")
st.title("🎧 Go Noise: Product Category & Sales Roster")
st.caption("Tracking: Watches | Audio | Accessories (Jan - Feb 2026)")

# 2. Master Data: Complete Roster with Category Qty & Value
data = [
    # JANUARY DATA (Partial Sample for brevity, your code will have all)
    {"Month": "Jan", "Zone": "WEST-1", "Salesman": "GURUNATH", "W_Qty": 10398, "W_Val": 14456438, "A_Qty": 7228, "A_Val": 7011402, "Acc_Qty": 6, "Acc_Val": 6990},
    {"Month": "Jan", "Zone": "WEST-1", "Salesman": "J", "W_Qty": 6389, "W_Val": 10225496, "A_Qty": 5111, "A_Val": 4730444, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Jan", "Zone": "WEST-2", "Salesman": "DINESH", "W_Qty": 2690, "W_Val": 4345648, "A_Qty": 3052, "A_Val": 4479353, "Acc_Qty": 90, "Acc_Val": 175050},
    {"Month": "Jan", "Zone": "MUMBAI D2R", "Salesman": "LAXMAN", "W_Qty": 498, "W_Val": 1267414, "A_Qty": 439, "A_Val": 641890, "Acc_Qty": 1, "Acc_Val": 2067},
    
    # FEBRUARY DATA
    {"Month": "Feb", "Zone": "WEST-1", "Salesman": "GURUNATH", "W_Qty": 9844, "W_Val": 13182573, "A_Qty": 4922, "A_Val": 5021419, "Acc_Qty": 765, "Acc_Val": 1487925},
    {"Month": "Feb", "Zone": "WEST-1", "Salesman": "J", "W_Qty": 3345, "W_Val": 5527059, "A_Qty": 3668, "A_Val": 3486360, "Acc_Qty": 300, "Acc_Val": 577800},
    {"Month": "Feb", "Zone": "WEST-2", "Salesman": "DINESH", "W_Qty": 4744, "W_Val": 6273006, "A_Qty": 1308, "A_Val": 1338016, "Acc_Qty": 255, "Acc_Val": 417975},
    {"Month": "Feb", "Zone": "WEST-2", "Salesman": "JULESH", "W_Qty": 5731, "W_Val": 9013208, "A_Qty": 3068, "A_Val": 3190321, "Acc_Qty": 600, "Acc_Val": 1151400},
    {"Month": "Feb", "Zone": "MUMBAI D2R", "Salesman": "LAXMAN", "W_Qty": 533, "W_Val": 1117105, "A_Qty": 310, "A_Val": 412839, "Acc_Qty": 24, "Acc_Val": 35749},
    {"Month": "Feb", "Zone": "PUNE D2R", "Salesman": "GIRISH", "W_Qty": 121, "W_Val": 321691, "A_Qty": 85, "A_Val": 94869, "Acc_Qty": 6, "Acc_Val": 12326}
]

df = pd.DataFrame(data)
df['Total_Val'] = df['W_Val'] + df['A_Val'] + df['Acc_Val']
df['Total_Qty'] = df['W_Qty'] + df['A_Qty'] + df['Acc_Qty']

# 3. Sidebar Interactivity
st.sidebar.title("🛠️ Analysis Tools")
metric_type = st.sidebar.radio("View Data By:", ["Billing Value (₹)", "Quantity (Qty)"])
month_filter = st.sidebar.multiselect("Select Month(s)", options=["Jan", "Feb"], default=["Jan", "Feb"])

# 4. Top KPIs (Filtered)
filtered_df = df[df['Month'].isin(month_filter)]
st.header(f"📊 Overall Performance ({', '.join(month_filter)})")

c1, c2, c3 = st.columns(3)
if metric_type == "Billing Value (₹)":
    c1.metric("Watch Total", f"₹{filtered_df['W_Val'].sum():,.0f}")
    c2.metric("Audio Total", f"₹{filtered_df['A_Val'].sum():,.0f}")
    c3.metric("Accessories Total", f"₹{filtered_df['Acc_Val'].sum():,.0f}")
else:
    c1.metric("Watch Qty", f"{filtered_df['W_Qty'].sum():,.0f}")
    c2.metric("Audio Qty", f"{filtered_df['A_Qty'].sum():,.0f}")
    c3.metric("Accessories Qty", f"{filtered_df['Acc_Qty'].sum():,.0f}")

st.markdown("---")

# 5. Interactive Category Chart
st.subheader("Category Distribution by Salesman")
val_cols = ['W_Val', 'A_Val', 'Acc_Val'] if metric_type == "Billing Value (₹)" else ['W_Qty', 'A_Qty', 'Acc_Qty']
melted = filtered_df.melt(id_vars=["Salesman", "Month"], value_vars=val_cols, var_name="Category", value_name="Amt")

fig = px.bar(melted, x="Salesman", y="Amt", color="Category", barmode="group", facet_row="Month",
             text_auto='.2s', title=f"Category Breakdown ({metric_type})")
st.plotly_chart(fig, use_container_width=True)

# 6. Full Data Explorer
st.subheader("📋 Master Table (Value & Quantity)")
st.dataframe(filtered_df, use_container_width=True, hide_index=True)
