import streamlit as st
import pandas as pd
import plotly.express as px
import openai

st.set_page_config(page_title="Evolution Inc Sales Intelligence", layout="wide")

st.title("Evolution Inc AI Sales Intelligence Dashboard")

# ---------------- OPENAI ----------------

openai.api_key = st.secrets["OPENAI_API_KEY"]

# ---------------- SALES DATA ----------------

data = [
["January","WEST-1 INDIA","FIROZ",13,33783,38,100534,0,0],
["January","WEST-1 INDIA","GURUNATH",7228,7011402,10398,14456438,6,6990],
["January","WEST-1 INDIA","J",20,15680,6389,10225496,0,0],
["January","WEST-1 INDIA","DINESH",3228,3625520,5281,6913477,18,27506],

["February","WEST-1 INDIA","FIROZ",8,19614,30,73094,0,0],
["February","WEST-1 INDIA","GURUNATH",5445,5427465,9844,13182573,46,81979],
["February","WEST-1 INDIA","J",6,6078,6466,9585150,0,0],
["February","WEST-1 INDIA","DINESH",2413,2556662,4813,5472335,65,102099],
]

columns = [
"Month","Zone","Salesman",
"Audio Qty","Audio Revenue",
"Watch Qty","Watch Revenue",
"Accessories Qty","Accessories Revenue"
]

df = pd.DataFrame(data,columns=columns)

# ---------------- TOTAL CALCULATIONS ----------------

df["Total Qty"] = df["Audio Qty"] + df["Watch Qty"] + df["Accessories Qty"]

df["Total Revenue"] = (
df["Audio Revenue"] +
df["Watch Revenue"] +
df["Accessories Revenue"]
)

df["ASP"] = df["Total Revenue"] / df["Total Qty"]

# ---------------- KPI ----------------

st.subheader("Business KPIs")

c1,c2,c3 = st.columns(3)

total_revenue = df["Total Revenue"].sum()
total_units = df["Total Qty"].sum()
asp = total_revenue / total_units

c1.metric("Total Revenue",f"₹{total_revenue:,.0f}")
c2.metric("Units Sold",int(total_units))
c3.metric("Average Selling Price",f"₹{asp:,.0f}")

st.divider()

# ---------------- CATEGORY ANALYSIS ----------------

st.subheader("Category Revenue")

category_df = pd.DataFrame({
"Category":["Audio","Watch","Accessories"],
"Revenue":[
df["Audio Revenue"].sum(),
df["Watch Revenue"].sum(),
df["Accessories Revenue"].sum()
]
})

fig = px.pie(category_df,names="Category",values="Revenue")

st.plotly_chart(fig,use_container_width=True)

# ---------------- SALESMAN LEADERBOARD ----------------

st.subheader("Salesman Leaderboard")

salesman_df = df.groupby("Salesman").agg({
"Total Revenue":"sum",
"Total Qty":"sum"
}).reset_index()

salesman_df["ASP"] = salesman_df["Total Revenue"] / salesman_df["Total Qty"]

salesman_df = salesman_df.sort_values("Total Revenue",ascending=False)

fig2 = px.bar(
salesman_df,
x="Salesman",
y="Total Revenue",
color="Total Revenue",
title="Salesman Revenue Ranking"
)

st.plotly_chart(fig2,use_container_width=True)

st.dataframe(salesman_df)

# ---------------- ZONE PERFORMANCE ----------------

st.subheader("Zone Performance")

zone_df = df.groupby("Zone")["Total Revenue"].sum().reset_index()

fig3 = px.bar(zone_df,x="Zone",y="Total Revenue",color="Total Revenue")

st.plotly_chart(fig3,use_container_width=True)

# ---------------- MONTHLY TREND ----------------

st.subheader("Monthly Revenue Trend")

month_df = df.groupby("Month")["Total Revenue"].sum().reset_index()

fig4 = px.line(month_df,x="Month",y="Total Revenue",markers=True)

st.plotly_chart(fig4,use_container_width=True)

# ---------------- SALES FORECAST ----------------

st.subheader("Forecast (Next Month)")

jan = month_df.loc[month_df["Month"]=="January","Total Revenue"].values[0]
feb = month_df.loc[month_df["Month"]=="February","Total Revenue"].values[0]

growth = (feb - jan) / jan

forecast = feb * (1 + growth)

st.metric("Predicted March Revenue",f"₹{forecast:,.0f}")

# ---------------- AI INSIGHTS ----------------

st.subheader("AI Business Insights")

summary = df.groupby("Salesman").agg({
"Total Revenue":"sum",
"Total Qty":"sum"
}).reset_index()

prompt = f"""
You are a business sales analyst.

Analyze the following data:

{summary.to_string()}

Provide:

1. Best performing salesman
2. Weak performance
3. Sales risk
4. Growth opportunity
5. Business recommendation
"""

response = openai.ChatCompletion.create(
model="gpt-4o-mini",
messages=[{"role":"user","content":prompt}]
)

insights = response["choices"][0]["message"]["content"]

st.write(insights)

# ---------------- DATA TABLE ----------------

st.subheader("Detailed Data")

st.dataframe(df)is 
