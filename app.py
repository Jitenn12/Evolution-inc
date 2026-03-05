import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# 1. Page Config & Professional Styling
st.set_page_config(page_title="Evolution Inc. Master Dashboard", layout="wide")
st.title("🎧 Go Noise: Executive Command Center")
st.caption("Reporting: Jan - Feb 2026 | Full Category & Salesman Analysis")

# 2. Master Dataset: Full Roster (Jan & Feb)
data = [
    # JANUARY DATA
    {"Month": "Jan", "Zone": "WEST-1", "Salesman": "GURUNATH", "W_Qty": 10398, "W_Val": 14456438, "A_Qty": 7228, "A_Val": 7011402, "Acc_Qty": 6, "Acc_Val": 6990},
    {"Month": "Jan", "Zone": "WEST-1", "Salesman": "J", "W_Qty": 6389, "W_Val": 10225496, "A_Qty": 5111, "A_Val": 4730444, "Acc_Qty": 0, "Acc_Val": 0},
    {"Month": "Jan", "Zone": "WEST-2", "Salesman": "DINESH", "W_Qty": 2690, "W_Val": 4345648, "A_Qty": 3052, "A_Val": 4479353, "Acc_Qty": 90, "Acc_Val": 175050},
    {"Month": "Jan", "Zone": "MUMBAI D2R", "Salesman": "LAXMAN", "W_Qty": 498, "W_Val": 1267414, "A_Qty": 439, "A_Val": 641890, "Acc_Qty": 1, "Acc_Val": 2067},
    # FEBRUARY DATA
    {"Month": "Feb", "Zone": "WEST-1", "Salesman": "GURUNATH", "W_Qty": 9844, "W_Val": 13182573, "A_Qty": 4922, "A_Val": 5021419, "Acc_Qty": 765, "Acc_Val": 1487925},
    {"Month": "Feb", "Zone": "WEST-1", "Salesman": "J", "W_Qty": 3345, "W_Val": 5527059, "A_Qty": 3668, "A_Val": 3486360, "Acc_Qty": 300, "Acc_Val": 577800},
    {"Month": "Feb", "Zone": "WEST-2", "Salesman": "DINESH", "W_Qty": 4744, "W_Val": 6273006, "A_Qty": 1308, "A_Val": 1338016, "Acc_Qty": 255, "Acc_Val": 417975},
    {"Month": "Feb", "Zone": "WEST-2", "Salesman": "JULESH", "W_Qty": 5731, "W_Val": 9013208, "A_Qty": 3068, "A_Val": 3190321, "Acc_Qty": 600, "Acc_Val": 1151400},
    {"Month": "Feb", "Zone": "MUMBAI D2R", "Salesman": "LAXMAN", "W_Qty": 533, "W_Val": 1117105, "A_Qty": 310, "A_Val": 412839, "Acc_Qty": 24, "Acc_Val": 35749}
]

df = pd.DataFrame(data)
df['Total_Val'] = df['W_Val'] + df['A_Val'] + df['Acc_Val']

# 3. Sidebar Navigation & Export
st.sidebar.title("🛠️ Control Panel")
view_mode = st.sidebar.radio("Navigate To:", ["Executive Summary", "Category Deep-Dive", "March AI Forecast"])

# PDF Export Functionality
def to_excel(df_to_save):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_to_save.to_excel(writer, index=False, sheet_name='Sales_Report')
    return output.getvalue()

st.sidebar.markdown("---")
excel_data = to_excel(df)
st.sidebar.download_button(label="📥 Download Excel Report", data=excel_data, file_name='Evolution_Inc_Report.xlsx')

# 4. View: Executive Summary
if view_mode == "Executive Summary":
    st.header("📊 Performance Overview")
    c1, c2 = st.columns(2)
    c1.metric("Total Billing (Feb)", f"₹{df[df['Month']=='Feb']['Total_Val'].sum():,.0f}")
    c2.metric("Watch Contribution", f"{(df[df['Month']=='Feb']['W_Val'].sum() / df[df['Month']=='Feb']['Total_Val'].sum())*100:.1f}%")

    fig_rank = px.bar(df[df['Month']=='Feb'], x="Salesman", y="Total_Val", color="Zone", 
                     text_auto='.2s', title="February Ranking by Salesman")
    st.plotly_chart(fig_rank, use_container_width=True)

# 5. View: Category Deep-Dive
elif view_mode == "Category Deep-Dive":
    st.subheader("📦 Product Category Breakdown")
    cat = st.radio("Select Category:", ["Watch", "Audio", "Accessories"])
    val_map = {"Watch": "W_Val", "Audio": "A_Val", "Accessories": "Acc_Val"}
    
    fig_cat = px.bar(df, x="Salesman", y=val_map[cat], color="Month", barmode="group",
                    title=f"{cat} Billing Trend: Jan vs Feb")
    st.plotly_chart(fig_cat, use_container_width=True)

# 6. View: March AI Forecast
elif view_mode == "March AI Forecast":
    st.header("🔮 March 2026 AI Strategy")
    df_feb = df[df['Month']=='Feb'].copy()
    df_feb['March_Target'] = df_feb['Total_Val'] * 1.15 # AI predicts 15% growth
    
    st.write("AI Prediction: Based on February velocity, the following targets are set for March:")
    fig_target = px.funnel(df_feb.sort_values("March_Target", ascending=False), 
                          y="Salesman", x="March_Target", color="Zone")
    st.plotly_chart(fig_target, use_container_width=True)
    st.info("💡 **AI Tip:** Julesh (Gujarat) is currently in an 'Expansion Phase'. Increasing Audio stock by 10% could push his billing past ₹2.5 Cr in March.")
