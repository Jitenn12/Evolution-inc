
st.markdown("---")

# 5. Visualizing Lead-wise Category Trends
st.subheader("Category Performance Shift by Lead")
view_cat = st.radio("Select Category to Analyze Trend:", ["Watch_Sales", "Audio_Sales", "Accessory_Sales"])

fig_trend = px.bar(df, x="Lead/Entity", y=view_cat, color="Month", barmode="group",
                   title=f"{view_cat} Comparison by Territory",
                   color_discrete_map={'Jan': '#2E4053', 'Feb': '#F4D03F'}, text_auto='.2s')
st.plotly_chart(fig_trend, use_container_width=True)

# 6. AI Strategic Table (Growth Detail)
st.subheader("📋 Detailed Growth Table")
# Creating a growth view per lead
leads = df['Lead/Entity'].unique()
lead_growth_list = []
for lead in leads:
    l_jan = df[(df['Lead/Entity'] == lead) & (df['Month'] == "Jan")].iloc[0]
    l_feb = df[(df['Lead/Entity'] == lead) & (df['Month'] == "Feb")].iloc[0]
    lead_growth_list.append({
        "Lead": lead,
        "Watch Growth %": ((l_feb['Watch_Sales'] - l_jan['Watch_Sales']) / l_jan['Watch_Sales']) * 100,
        "Audio Growth %": ((l_feb['Audio_Sales'] - l_jan['Audio_Sales']) / l_jan['Audio_Sales']) * 100
    })

st.dataframe(pd.DataFrame(lead_growth_list), hide_index=True, use_container_width=True)
