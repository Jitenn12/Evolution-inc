import streamlit as st
import pandas as pd
import plotly.express as px
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# DEBUG CHECK
st.write("API Loaded:", "OPENAI_API_KEY" in st.secrets) 
# ---------------- OPENAI ----------------

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Evolution Inc Sales Dashboard", layout="wide")

st.title("Evolution Inc AI Sales Intelligence")

# ---------------- DATA ----------------

data = [

["January","WEST-1 INDIA","FIROZ",13,33783,38,100534,0,0],
["January","WEST-1 INDIA","GURUNATH",7228,7011402,10398,14456438,6,6990],
["January","WEST-1 INDIA","J-CORP",20,15680,1,4750,0,0],
["January","WEST-1 INDIA","J",5111,4730444,6389,10225496,0,0],

["January","WEST-2 INDIA","DINESH",3052,4479353,2690,4345648,90,175050],
["January","WEST-2 INDIA","JULESH",2326,2846038,3654,6491939,17,19805],

["January","MUMBAI D2R","AMIT",143,214900,269,489864,0,0],
["January","MUMBAI D2R","LAXMAN",439,641890,498,1267414,1,2067],
["January","MUMBAI D2R","NILESH",147,166844,247,408888,0,0],
["January","MUMBAI D2R","RAKESH",229,356996,499,948731,0,0],
["January","MUMBAI D2R","SANDEEP",417,530527,414,998770,0,0],
["January","MUMBAI D2R","TUKARAM",134,171187,220,364287,0,0],
["January","MUMBAI D2R","KALPESH",2,2109,0,0,0,0],

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
["February","PUNE D2R","GIRISH",85,94869,121,321691,6,12326]

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

# ---------------- CATEGORY DATA ----------------

category_df = pd.DataFrame({
"Month": df["Month"].repeat(3).values,
"Zone": df["Zone"].repeat(3).values,
"Salesman": df["Salesman"].repeat(3).values,
"Category": ["Audio","Watch","Accessories"] * len(df),
"Qty": df[["Audio Qty","Watch Qty","Accessories Qty"]].values.flatten(),
"Revenue": df[["Audio Revenue","Watch Revenue","Accessories Revenue"]].values.flatten()
})

# ---------------- FILTERS ----------------

st.sidebar.header("Filters")

month_filter = st.sidebar.multiselect(
"Month",
category_df["Month"].unique(),
default=category_df["Month"].unique()
)

zone_filter = st.sidebar.multiselect(
"Zone / State",
category_df["Zone"].unique(),
default=category_df["Zone"].unique()
)

salesman_filter = st.sidebar.multiselect(
"Salesman",
category_df["Salesman"].unique(),
default=category_df["Salesman"].unique()
)

category_filter = st.sidebar.multiselect(
"Category",
category_df["Category"].unique(),
default=category_df["Category"].unique()
)

filtered = category_df[
(category_df["Month"].isin(month_filter)) &
(category_df["Zone"].isin(zone_filter)) &
(category_df["Salesman"].isin(salesman_filter)) &
(category_df["Category"].isin(category_filter))
]

# ---------------- KPI ----------------

total_sales = filtered["Revenue"].sum()
total_units = filtered["Qty"].sum()
asp = total_sales / total_units if total_units else 0

st.header(f"Total Sales ₹{total_sales:,.0f}")

k1,k2,k3 = st.columns(3)

k1.metric("Total Revenue",f"₹{total_sales:,.0f}")
k2.metric("Units Sold",int(total_units))
k3.metric("Average Selling Price",f"₹{asp:,.0f}")

st.divider()

# ---------------- CATEGORY CHART ----------------

st.subheader("Category Revenue")

fig = px.bar(
filtered,
x="Category",
y="Revenue",
color="Month",
barmode="group"
)

st.plotly_chart(fig,use_container_width=True)

# ---------------- SALESMAN LEADERBOARD ----------------

st.subheader("Salesman Leaderboard")

salesman_chart = filtered.groupby("Salesman")["Revenue"].sum().reset_index()

fig2 = px.bar(
salesman_chart,
x="Salesman",
y="Revenue",
color="Revenue"
)

st.plotly_chart(fig2,use_container_width=True)

# ---------------- ZONE PERFORMANCE ----------------

st.subheader("Zone Performance")

zone_chart = filtered.groupby("Zone")["Revenue"].sum().reset_index()

fig3 = px.bar(
zone_chart,
x="Zone",
y="Revenue",
color="Revenue"
)

st.plotly_chart(fig3,use_container_width=True)

# ---------------- FORECAST ----------------

st.subheader("Forecast")

month_df = df.groupby("Month")["Total Revenue"].sum().reset_index()

jan = month_df.iloc[0]["Total Revenue"]
feb = month_df.iloc[1]["Total Revenue"]

growth = (feb - jan) / jan
forecast = feb * (1 + growth)

st.metric("Predicted March Revenue",f"₹{forecast:,.0f}")

# ---------------- AI INSIGHTS ----------------

st.subheader("AI Business Insights")

summary = filtered.groupby(["Salesman","Zone"])["Revenue"].sum().reset_index()

prompt = f"""
Analyze this sales dataset and provide insights:

{summary.to_string()}

Explain:
1. Top performing salesman
2. Weakest zone
3. Growth opportunity
4. Business risk
5. Strategy recommendation
"""

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    st.success(response.choices[0].message.content)

except:
    st.warning("AI insights unavailable. Check API key.")

# ---------------- ASK AI ----------------

st.divider()
st.subheader("Ask AI About Sales")

question = st.text_input(
"Ask a question about your sales data",
placeholder="Example: Why did February revenue drop?"
)

if question:

    data_context = filtered.groupby(
        ["Month","Zone","Salesman","Category"]
    )[["Revenue","Qty"]].sum().reset_index()

    prompt = f"""
You are a sales analytics expert.

Dataset:
{data_context.to_string()}

Answer this question clearly:

{question}
"""

    try:

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}]
        )

        st.success(response.choices[0].message.content)

    except:

        st.warning("AI unavailable. Check API key.")

# ---------------- DATA TABLE ----------------

st.subheader("Full Data")

st.dataframe(df)
