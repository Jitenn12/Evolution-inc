import streamlit as st
import pandas as pd
import plotly.express as px
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Evolution Inc Sales Intelligence", layout="wide")

st.title("Evolution Inc AI Sales Intelligence Dashboard")

# ---------------- COMPLETE SALES DATA ----------------

data = [

# JANUARY WEST-1
["January","WEST-1 INDIA","FIROZ",13,33783,38,100534,0,0],
["January","WEST-1 INDIA","GURUNATH",7228,7011402,10398,14456438,6,6990],
["January","WEST-1 INDIA","J-CORP",20,15680,1,4750,0,0],
["January","WEST-1 INDIA","J",5111,4730444,6389,10225496,0,0],

# JANUARY WEST-2
["January","WEST-2 INDIA","DINESH",3052,4479353,2690,4345648,90,175050],
["January","WEST-2 INDIA","JULESH",2326,2846038,3654,6491939,17,19805],

# JANUARY MUMBAI
["January","MUMBAI D2R","AMIT",143,214900,269,489864,0,0],
["January","MUMBAI D2R","LAXMAN",439,641890,498,1267414,1,2067],
["January","MUMBAI D2R","NILESH",147,166844,247,408888,0,0],
["January","MUMBAI D2R","RAKESH",229,356996,499,948731,0,0],
["January","MUMBAI D2R","SANDEEP",417,530527,414,998770,0,0],
["January","MUMBAI D2R","TUKARAM",134,171187,220,364287,0,0],
["January","MUMBAI D2R","KALPESH",2,2109,0,0,0,0],

# JANUARY PUNE
["January","PUNE D2R","FIROZ",112,103472,567,934789,0,0],
["January","PUNE D2R","GIRISH",192,360738,149,333707,0,0],
["January","PUNE D2R","KALPESH",0,0,0,0,0,0],

# FEB WEST-1
["February","WEST-1 INDIA","FIROZ",3,12997,63,176951,0,0],
["February","WEST-1 INDIA","GURUNATH",4922,5021419,9844,13182573,765,1487925],
["February","WEST-1 INDIA","J-CORP",275,392490,42,49974,0,0],
["February","WEST-1 INDIA","J",3668,3486360,3345,5527059,300,577800],

# FEB WEST-2
["February","WEST-2 INDIA","DINESH",1308,1338016,4744,6273006,255,417975],
["February","WEST-2 INDIA","JULESH",3068,3190321,5731,9013208,600,1151400],

# FEB MUMBAI
["February","MUMBAI D2R","AMIT",183,210327,304,471861,11,22613],
["February","MUMBAI D2R","LAXMAN",310,412839,533,1117105,24,35749],
["February","MUMBAI D2R","NILESH",168,198607,281,465939,13,20707],
["February","MUMBAI D2R","RAKESH",170,217197,498,879009,24,45216],
["February","MUMBAI D2R","SANDEEP",173,201265,398,883620,4,8132],
["February","MUMBAI D2R","TUKARAM",270,347908,178,290851,3,6420],
["February","MUMBAI D2R","J",13,56680,0,0,0,0],
["February","MUMBAI D2R","KALPESH",3,3224,6,20309,1,1282],

# FEB PUNE
["February","PUNE D2R","FIROZ",85,84970,172,341024,0,0],
["February","PUNE D2R","GIRISH",85,94869,121,321691,6,12326],
["February","PUNE D2R","KALPESH",0,0,0,0,0,0]

]

columns = [
"Month","Zone","Salesman",
"Audio Qty","Audio Revenue",
"Watch Qty","Watch Revenue",
"Accessories Qty","Accessories Revenue"
]

df = pd.DataFrame(data,columns=columns)

# ---------------- CALCULATIONS ----------------

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

# ---------------- CATEGORY CHART ----------------

cat = pd.DataFrame({
"Category":["Audio","Watch","Accessories"],
"Revenue":[
df["Audio Revenue"].sum(),
df["Watch Revenue"].sum(),
df["Accessories Revenue"].sum()
]
})

fig = px.pie(cat,names="Category",values="Revenue")
st.plotly_chart(fig,use_container_width=True)

# ---------------- SALESMAN LEADERBOARD ----------------

salesman = df.groupby("Salesman")["Total Revenue"].sum().reset_index()

salesman = salesman.sort_values("Total Revenue",ascending=False)

fig2 = px.bar(salesman,x="Salesman",y="Total Revenue",color="Total Revenue")

st.plotly_chart(fig2,use_container_width=True)

# ---------------- ZONE PERFORMANCE ----------------

zone = df.groupby("Zone")["Total Revenue"].sum().reset_index()

fig3 = px.bar(zone,x="Zone",y="Total Revenue",color="Total Revenue")

st.plotly_chart(fig3,use_container_width=True)

# ---------------- MONTH TREND ----------------

month = df.groupby("Month")["Total Revenue"].sum().reset_index()

fig4 = px.line(month,x="Month",y="Total Revenue",markers=True)

st.plotly_chart(fig4,use_container_width=True)

# ---------------- AI INSIGHTS ----------------

summary = df.groupby("Salesman").agg({
"Total Revenue":"sum",
"Total Qty":"sum"
}).reset_index()

prompt = f"""
Analyze this sales data:

{summary.to_string()}

Provide:
1. Top salesman
2. Weak zone
3. Opportunity
4. Risk
5. Strategy
"""

response = client.chat.completions.create(
model="gpt-4o-mini",
messages=[{"role":"user","content":prompt}]
)

st.subheader("AI Insights")

st.write(response.choices[0].message.content)

# ---------------- DATA TABLE ----------------

st.subheader("Full Data")

st.dataframe(df)
