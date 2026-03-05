import streamlit as st
import pandas as pd
import plotly.express as px
from openai import OpenAI
import base64
from io import StringIO

st.set_page_config(page_title="Evolution Inc Sales Intelligence", layout="wide")

# ---------------- LOGIN ----------------

users = {
    "admin": "admin123",
    "analyst": "analyst123"
}

st.sidebar.title("Login")

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if username not in users or users[username] != password:
    st.warning("Login to continue")
    st.stop()

st.sidebar.success("Logged in")

# ---------------- OPENAI ----------------

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------- DEFAULT SALES DATA ----------------

data = [

["January","WEST-1 INDIA","Maharashtra","FIROZ",13,33783,38,100534,0,0],
["January","WEST-1 INDIA","Maharashtra","GURUNATH",7228,7011402,10398,14456438,6,6990],
["January","WEST-1 INDIA","Gujarat","J-CORP",20,15680,1,4750,0,0],
["January","WEST-1 INDIA","Gujarat","J",5111,4730444,6389,10225496,0,0],

["January","WEST-2 INDIA","Gujarat","DINESH",3052,4479353,2690,4345648,90,175050],
["January","WEST-2 INDIA","Gujarat","JULESH",2326,2846038,3654,6491939,17,19805],

["January","MUMBAI D2R","Maharashtra","AMIT",143,214900,269,489864,0,0],
["January","MUMBAI D2R","Maharashtra","LAXMAN",439,641900,498,1267414,1,2067],
["January","MUMBAI D2R","Maharashtra","NILESH",147,166844,247,408888,0,0],
["January","MUMBAI D2R","Maharashtra","RAKESH",229,356996,499,948731,0,0],
["January","MUMBAI D2R","Maharashtra","SANDEEP",417,530527,414,998770,0,0],
["January","MUMBAI D2R","Maharashtra","TUKARAM",134,171187,220,364287,0,0],

["January","PUNE D2R","Maharashtra","FIROZ",112,103472,567,934789,0,0],
["January","PUNE D2R","Maharashtra","GIRISH",192,360738,149,333707,0,0],

["February","WEST-1 INDIA","Maharashtra","FIROZ",3,12997,63,176951,0,0],
["February","WEST-1 INDIA","Maharashtra","GURUNATH",4922,5021419,9844,13182573,765,1487925],
["February","WEST-1 INDIA","Gujarat","J-CORP",275,392490,42,49974,0,0],
["February","WEST-1 INDIA","Gujarat","J",3668,3486360,3345,5527059,300,577800],

["February","WEST-2 INDIA","Gujarat","DINESH",1308,1338016,4744,6273006,255,417975],
["February","WEST-2 INDIA","Gujarat","JULESH",3068,3190321,5731,9013208,600,1151400],

["February","MUMBAI D2R","Maharashtra","AMIT",183,210327,304,471861,11,22613],
["February","MUMBAI D2R","Maharashtra","LAXMAN",310,412839,533,1117105,24,35749],
["February","MUMBAI D2R","Maharashtra","NILESH",168,198607,281,465939,13,20707],
["February","MUMBAI D2R","Maharashtra","RAKESH",170,217197,498,879009,24,45216],
["February","MUMBAI D2R","Maharashtra","SANDEEP",173,201265,398,883620,4,8132],
["February","MUMBAI D2R","Maharashtra","TUKARAM",270,347908,178,290851,3,6420],

["February","PUNE D2R","Maharashtra","FIROZ",85,84970,172,341024,0,0],
["February","PUNE D2R","Maharashtra","GIRISH",85,94869,121,321691,6,12326],
]

columns = [
"Month","Zone","State","Salesman",
"Audio Qty","Audio Revenue",
"Watch Qty","Watch Revenue",
"Accessories Qty","Accessories Revenue"
]

df = pd.DataFrame(data, columns=columns)

# ---------------- CALCULATIONS ----------------

df["Total Revenue"] = (
df["Audio Revenue"] +
df["Watch Revenue"] +
df["Accessories Revenue"]
)

df["Total Qty"] = (
df["Audio Qty"] +
df["Watch Qty"] +
df["Accessories Qty"]
)

# ---------------- FILTERS ----------------

st.sidebar.subheader("Filters")

month = st.sidebar.multiselect(
"Month",
df["Month"].unique(),
df["Month"].unique()
)

zone = st.sidebar.multiselect(
"Zone",
df["Zone"].unique(),
df["Zone"].unique()
)

salesman = st.sidebar.multiselect(
"Salesman",
df["Salesman"].unique(),
df["Salesman"].unique()
)

filtered = df[
(df["Month"].isin(month)) &
(df["Zone"].isin(zone)) &
(df["Salesman"].isin(salesman))
]

# ---------------- KPI ----------------

st.title("Evolution Inc AI Sales Intelligence")

col1,col2,col3 = st.columns(3)

total_sales = filtered["Total Revenue"].sum()
total_units = filtered["Total Qty"].sum()

asp = int(total_sales/total_units)

col1.metric("Total Revenue",f"₹{total_sales:,}")
col2.metric("Units Sold",total_units)
col3.metric("Average Selling Price",f"₹{asp}")

# ---------------- CATEGORY CHART ----------------

st.subheader("Category Revenue")

cat_df = pd.DataFrame({
"Category":["Audio","Watch","Accessories"],
"Revenue":[
filtered["Audio Revenue"].sum(),
filtered["Watch Revenue"].sum(),
filtered["Accessories Revenue"].sum()
]})

fig = px.bar(cat_df,x="Category",y="Revenue",color="Category")

st.plotly_chart(fig,use_container_width=True)

# ---------------- ZONE CHART ----------------

st.subheader("Zone Revenue")

zone_df = filtered.groupby("Zone")["Total Revenue"].sum().reset_index()

fig = px.bar(zone_df,x="Zone",y="Total Revenue")

st.plotly_chart(fig,use_container_width=True)

# ---------------- LEADERBOARD ----------------

st.subheader("Salesman Leaderboard")

leader = filtered.groupby("Salesman")["Total Revenue"].sum().reset_index()

leader = leader.sort_values("Total Revenue",ascending=False)

st.dataframe(leader)

# ---------------- FORECAST ----------------

st.subheader("Next Month Forecast")

forecast = int(total_sales * 1.05)

st.title(f"₹{forecast:,}")

# ---------------- AI INSIGHTS ----------------

st.subheader("AI Business Insights")

summary = leader.to_string()

prompt = f"""
Analyze this sales data:

{summary}

Explain
Top performers
Weak zones
Growth opportunities
"""

try:

    response = client.chat.completions.create(

        model="gpt-4o-mini",

        messages=[
        {"role":"system","content":"You are a sales analytics expert"},
        {"role":"user","content":prompt}
        ]
    )

    st.success(response.choices[0].message.content)

except:

    st.warning("AI unavailable")

# ---------------- ASK AI ----------------

st.subheader("Ask AI About Sales")

question = st.text_input("Ask question about sales")

if question:

    prompt = f"""
Sales data:

{filtered.to_string()}

Question:

{question}
"""

    try:

        response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
        {"role":"system","content":"You are a sales analyst"},
        {"role":"user","content":prompt}
        ])

        st.success(response.choices[0].message.content)

    except:

        st.warning("AI unavailable")

# ---------------- DATA TABLE ----------------

st.subheader("Full Sales Data")

st.dataframe(filtered)
