import streamlit as st
import pandas as pd
import plotly.express as px
from openai import OpenAI

# -------------------- OPENAI --------------------

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(layout="wide")

st.title("Evolution Inc AI Sales Intelligence")

# -------------------- DATA --------------------

data = [

["January","WEST-1 INDIA","FIROZ",13,33783,38,100534,0,0],
["January","WEST-1 INDIA","GURUNATH",7228,7011402,10398,14456438,6,6990],
["January","WEST-1 INDIA","J-CORP",20,15680,1,4750,0,0],
["January","WEST-1 INDIA","J",5111,4730444,6389,10225496,0,0],

["January","WEST-2 INDIA","DINESH",3052,4479353,2690,4345648,90,175050],
["January","WEST-2 INDIA","JULESH",2326,2846038,3654,6491939,17,19805],

["January","MUMBAI D2R","AMIT",143,214900,269,489864,0,0],
["January","MUMBAI D2R","LAXMAN",439,641900,498,1267414,1,2067],
["January","MUMBAI D2R","NILESH",147,166844,247,408888,0,0],
["January","MUMBAI D2R","RAKESH",229,356996,499,948731,0,0],
["January","MUMBAI D2R","SANDEEP",417,530527,414,998770,0,0],
["January","MUMBAI D2R","TUKARAM",134,171187,220,364287,0,0],

["January","PUNE D2R","FIROZ",112,103472,567,934789,0,0],
["January","PUNE D2R","GIRISH",192,360738,149,333707,0,0],

["February","WEST-1 INDIA","FIROZ",3,12997,63,176951,0,0],
["February","WEST-1 INDIA","GURUNATH",4922,5021419,9844,13182573,765,1487925],
["February","WEST-1 INDIA","J-CORP",275,392490,42,49974,0,0],
["February","WEST-1 INDIA","J",3668,3486360,3345,5527059,300,577800],

["February","WEST-2 INDIA","DINESH",1308,1338016,4744,6273006,255,417975],
["February","WEST-2 INDIA","JULESH",3068,3190321,5731,9013208,600,1151400],

["February","MUMBAI D2R","AMIT",183,210327,304,471861,11,22613],
["February","MUMBAI D2R","LAXMAN",310,412839,533,1117105,24,35749],
["February","MUMBAI D2R","NILESH",168,198607,281,465939,13,20707],
["February","MUMBAI D2R","RAKESH",170,217197,498,879009,24,45216],
["February","MUMBAI D2R","SANDEEP",173,201265,398,883620,4,8132],
["February","MUMBAI D2R","TUKARAM",270,347908,178,290851,3,6420],

["February","PUNE D2R","FIROZ",85,84970,172,341024,0,0],
["February","PUNE D2R","GIRISH",85,94869,121,321691,6,12326],

]

df = pd.DataFrame(data, columns=[
"Month","Zone","Salesman",
"Audio Qty","Audio Revenue",
"Watch Qty","Watch Revenue",
"Accessories Qty","Accessories Revenue"
])

df["Total Revenue"] = df["Audio Revenue"] + df["Watch Revenue"] + df["Accessories Revenue"]
df["Total Qty"] = df["Audio Qty"] + df["Watch Qty"] + df["Accessories Qty"]

# -------------------- FILTERS --------------------

st.sidebar.header("Filters")

month = st.sidebar.multiselect("Month",df["Month"].unique(),df["Month"].unique())
zone = st.sidebar.multiselect("Zone / State",df["Zone"].unique(),df["Zone"].unique())
salesman = st.sidebar.multiselect("Salesman",df["Salesman"].unique(),df["Salesman"].unique())

filtered = df[
(df["Month"].isin(month)) &
(df["Zone"].isin(zone)) &
(df["Salesman"].isin(salesman))
]

# -------------------- KPIs --------------------

col1,col2,col3 = st.columns(3)

col1.metric("Total Revenue",f"₹{filtered['Total Revenue'].sum():,}")
col2.metric("Units Sold",filtered["Total Qty"].sum())

asp = int(filtered["Total Revenue"].sum()/filtered["Total Qty"].sum())
col3.metric("Average Selling Price",f"₹{asp}")

# -------------------- CATEGORY CHART --------------------

st.subheader("Category Revenue")

cat = pd.DataFrame({
"Category":["Audio","Watch","Accessories"],
"Revenue":[
filtered["Audio Revenue"].sum(),
filtered["Watch Revenue"].sum(),
filtered["Accessories Revenue"].sum()
]})

fig = px.bar(cat,x="Category",y="Revenue",color="Category")
st.plotly_chart(fig,use_container_width=True)

# -------------------- FORECAST --------------------

st.subheader("Forecast")

forecast = int(filtered["Total Revenue"].sum()*1.05)

st.write("Predicted Next Month Revenue")
st.title(f"₹{forecast:,}")

# -------------------- LEADERBOARD --------------------

st.divider()
st.subheader("Salesman Leaderboard")

leaderboard = filtered.groupby("Salesman")["Total Revenue"].sum().reset_index()
leaderboard = leaderboard.sort_values("Total Revenue",ascending=False)

leaderboard["Rank"] = range(1,len(leaderboard)+1)

st.dataframe(leaderboard)

# -------------------- ZONE HEATMAP --------------------

st.divider()
st.subheader("Zone Revenue Heatmap")

heat = filtered.groupby("Zone")["Total Revenue"].sum().reset_index()

fig = px.treemap(
heat,
path=["Zone"],
values="Total Revenue",
color="Total Revenue"
)

st.plotly_chart(fig,use_container_width=True)

# -------------------- ANOMALY DETECTION --------------------

st.divider()
st.subheader("Sales Anomaly Detection")

jan = df[df["Month"]=="January"].groupby("Zone")["Total Revenue"].sum()
feb = df[df["Month"]=="February"].groupby("Zone")["Total Revenue"].sum()

alerts = []

for z in jan.index:

    change = ((feb[z]-jan[z])/jan[z])*100

    if change < -20:
        alerts.append(f"⚠ Sales dropped {round(change,1)}% in {z}")

    if change > 20:
        alerts.append(f"🚀 Sales increased {round(change,1)}% in {z}")

for a in alerts:
    st.warning(a)

# -------------------- AI SALES ALERTS --------------------

st.divider()
st.subheader("AI Sales Alerts")

categories = ["Audio Revenue","Watch Revenue","Accessories Revenue"]

for cat in categories:

    jan_total = df[df["Month"]=="January"][cat].sum()
    feb_total = df[df["Month"]=="February"][cat].sum()

    change = ((feb_total-jan_total)/jan_total)*100

    if change < -15:
        st.warning(f"⚠ {cat.replace(' Revenue','')} dropped {round(change,1)}%")

    if change > 15:
        st.success(f"🚀 {cat.replace(' Revenue','')} grew {round(change,1)}%")

# -------------------- AI BUSINESS INSIGHTS --------------------

st.divider()
st.subheader("AI Business Insights")

summary = filtered.groupby("Salesman")["Total Revenue"].sum().reset_index()

prompt = f"""
Analyze this sales dataset:

{summary.to_string()}

Explain:

Top performer
Weak zone
Opportunity
Strategy
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

except Exception as e:

    st.warning("AI unavailable")
    st.write(e)

# -------------------- ASK AI --------------------

st.divider()
st.subheader("Ask AI About Sales")

question = st.text_input("Ask question about your sales")

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
                {"role":"system","content":"You are a sales analytics expert"},
                {"role":"user","content":prompt}
            ]

        )

        st.success(response.choices[0].message.content)

    except:
        st.warning("AI unavailable")

# -------------------- FULL DATA --------------------

st.divider()
st.subheader("Full Data")

st.dataframe(filtered)
