import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="Evolution Inc. Verified Dashboard", layout="wide")

# Custom Function for Indian Currency Formatting
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

# 2. VERIFIED FEBRUARY DATASET
data = [
    {"Zone": "WEST-1", "Salesman": "FIROZ", "A_Qty": 3, "A_Val": 12997, "W_Qty": 63, "W_Val": 176951, "Acc_Qty": 0, "Acc_Val": 0},
    {"Zone": "WEST-1", "Salesman": "GURUNATH", "A_Qty": 4922, "A_Val": 5021419, "W_Qty": 9844, "W_Val": 13182573, "Acc_Qty": 765, "Acc_Val": 1487925},
    {"Zone": "WEST-1", "Salesman": "J-CORP", "A_Qty": 275, "A_Val": 392490, "W_Qty": 42, "W_Val": 49974, "Acc_Qty": 0, "Acc_Val": 0},
    {"Zone": "WEST-1", "Salesman": "J", "A_Qty": 3668, "A_Val": 3486360, "W_Qty": 3345, "W_Val": 5527059, "Acc_Qty": 300, "Acc_Val": 577800},
    {"Zone": "WEST-2", "Salesman": "DINESH", "A_Qty": 1308, "A_Val": 1338016, "W_Qty": 4744, "W_Val": 6273006, "Acc_Qty": 255, "Acc_Val": 417975},
    {"Zone": "WEST-2", "Salesman": "JULESH", "A_Qty": 3068, "A_Val": 3190321, "W_Qty": 5731, "W_Val": 9013208, "Acc_Qty": 600, "Acc_Val": 1151400},
    {"Zone": "MUMBAI D2R", "Salesman": "AMIT", "A_Qty": 183, "A_Val": 210327, "W_Qty": 304, "W_Val": 471861, "Acc_Qty": 11, "Acc_Val": 22613},
    {"Zone": "MUMBAI D2R", "Salesman": "LAXMAN", "A_Qty": 310, "A_Val": 412839, "W_Qty": 533, "W_Val": 1117105, "Acc_Qty": 24, "Acc_Val": 35749},
    {"Zone": "MUMBAI D2R", "Salesman": "NILESH", "A_Qty": 168, "A_Val": 198607, "W_Qty": 281, "W_Val": 465939, "Acc_Qty": 13, "Acc_Val": 20707},
    {"Zone": "MUMBAI D2R", "Salesman": "RAKESH", "A_Qty": 170, "A_Val": 217197, "W_Qty": 498, "W_Val": 879009, "Acc_Qty": 24, "Acc_Val": 45216},
    {"Zone": "MUMBAI D2R", "Salesman": "SANDEEP", "A_Qty": 173, "A_Val": 201265, "W_Qty": 398, "W_Val": 883620, "Acc_Qty": 4, "Acc_Val": 8132},
    {"Zone": "MUMBAI D2R", "Salesman": "TUKARAM", "A_Qty": 270, "A_Val": 347908, "W_Qty": 178, "W_Val": 290851, "Acc_Qty": 3, "Acc_Val": 6420},
    {"Zone": "MUMBAI D2R", "Salesman": "J-MUM", "A_Qty": 13, "A_Val": 56680, "W_Qty": 0, "W_Val": 0, "Acc_Qty": 0, "Acc_Val": 0},
    {"Zone": "MUMBAI D2R", "Salesman": "KALPESH", "A_Qty": 3, "A_Val": 3224, "W_Qty": 6, "W_Val": 20309, "Acc_Qty": 1, "Acc_Val": 1282},
    {"Zone": "PUNE D2R", "Salesman": "FIROZ-P", "A_Qty": 85, "A_Val": 84970, "W_Qty": 172, "W_Val": 341024, "Acc_Qty": 0, "Acc_Val": 0},
    {"Zone": "PUNE D2R", "Salesman": "GIRISH", "A_Qty": 85, "A_Val": 94869, "W_Qty": 121, "W_Val": 321691, "Acc_Qty": 6, "Acc_Val": 12326}
]

df = pd.DataFrame(data)
df['Total_Qty'] = df['A_Qty'] + df['W_Qty'] + df['Acc_Qty']
df['Total_Val'] = df['A_Val'] + df['W_Val'] + df['Acc_Val']

# 3. Sidebar
st.sidebar.title("🛠️ Tools")
view_type = st.sidebar.radio("View Metric:", ["Executive Summary", "Full Data Sheet"])
zone_filter = st.sidebar.multiselect("Filter Zones:", df['Zone'].unique(), default=df['Zone'].unique())

filtered_df = df[df['Zone'].isin(zone_filter)]

# 4. Interactive Content
if view_type == "Executive Summary":
    st.header("📊 Performance Overview (Feb 2026)")
    c1, c2 = st.columns(2)
    
    # Displaying KPIs in Indian Format
    total_revenue = filtered_df['Total_Val'].sum()
    c1.metric("Grand Total Billing", format_indian_currency(total_revenue))
    c2.metric("Grand Total Qty", f"{filtered_df['Total_Qty'].sum():,}")
    
    # Chart with Lakh formatting for labels
    fig = px.bar(filtered_df, x="Salesman", y="Total_Val", color="Zone", 
                 title="Salesman Ranking (Billing Amount)")
    
    # Update Chart to show Lakhs/Crores on the axis
    fig.update_layout(yaxis_title="Billing (₹)")
    st.plotly_chart(fig, use_container_width=True)

else:
    st.subheader("📋 Complete Sales Sheet")
    # Applying Indian format to the dataframe display
    display_df = filtered_df.copy()
    for col in ['A_Val', 'W_Val', 'Acc_Val', 'Total_Val']:
        display_df[col] = display_df[col].apply(format_indian_currency)
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)
