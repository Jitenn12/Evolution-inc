import streamlit as st
import pandas as pd
import plotly.express as px
from openai import OpenAI
import base64
from io import StringIO

st.set_page_config(layout="wide")

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

# ---------------- FILE UPLOAD ----------------

st.sidebar.subheader("Upload Sales File")

uploaded_file = st.sidebar.file_uploader(
    "Upload Excel / CSV",
    type=["xlsx","csv"]
)

if uploaded_file is None:
    st.info("Upload your Sales Register Excel")
    st.stop()

# ---------------- READ FILE ----------------

if uploaded_file.name.endswith("xlsx"):
    df = pd.read_excel(uploaded_file)
else:
    df = pd.read_csv(uploaded_file)

df.columns = df.columns.str.strip()

# ---------------- REQUIRED COLUMNS ----------------

required = [
"Month",
"Type",
"Quantity",
"Value",
"Salesman",
"State",
"Zone"
]

missing = [c for c in required if c not in df.columns]

if missing:
    st.error(f"Missing columns: {missing}")
    st.stop()

# ---------------- CLEAN DATA ----------------

df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(0)
df["Value"] = pd.to_numeric(df["Value"], errors="coerce").fillna(0)

# ---------------- CATEGORY SPLIT ----------------

audio = df[df["Type"].str.contains("audio", case=False, na=False)]
watch = df[df["Type"].str.contains("watch", case=False, na=False)]
accessories = df[df["Type"].str.contains("access", case=False, na=False)]

# ---------------- TOTALS ----------------

audio_rev = audio["Value"].sum()
watch_rev = watch["Value"].sum()
acc_rev = accessories["Value"].sum()

audio_qty = audio["Quantity"].sum()
watch_qty = watch["Quantity"].sum()
acc_qty = accessories["Quantity"].sum()

total_sales = df["Value"].sum()
total_units = df["Quantity"].sum()

asp = int(total_sales/total_units) if total_units>0 else 0

# ---------------- DASHBOARD ----------------

st.title("Evolution Inc AI Sales Intelligence")

col1,col2,col3 = st.columns(3)

col1.metric("Total Revenue",f"₹{total_sales:,.0f}")
col2.metric("Units Sold",int(total_units))
col3.metric("Average Selling Price",f"₹{asp}")

# ---------------- CATEGORY CHART ----------------

st.subheader("Category Revenue")

cat_df = pd.DataFrame({
"Category":["Audio","Watch","Accessories"],
"Revenue":[audio_rev,watch_rev,acc_rev]
})

fig = px.bar(cat_df,x="Category",y="Revenue",color="Category")

st.plotly_chart(fig,use_container_width=True)

# ---------------- ZONE SALES ----------------

st.subheader("Zone Performance")

zone_df = df.groupby("Zone")["Value"].sum().reset_index()

fig = px.bar(zone_df,x="Zone",y="Value",color="Value")

st.plotly_chart(fig,use_container_width=True)

# ---------------- STATE SALES ----------------

st.subheader("State Sales")

state_df = df.groupby("State")["Value"].sum().reset_index()

fig = px.bar(state_df,x="State",y="Value")

st.plotly_chart(fig,use_container_width=True)

# ---------------- SALESMAN LEADERBOARD ----------------

st.subheader("Salesman Leaderboard")

leader = df.groupby("Salesman")["Value"].sum().reset_index()

leader = leader.sort_values("Value",ascending=False)

st.dataframe(leader)

# ---------------- FORECAST ----------------

st.subheader("Next Month Forecast")

forecast = int(total_sales * 1.05)

st.title(f"₹{forecast:,.0f}")

# ---------------- AI INSIGHTS ----------------

st.subheader("AI Business Insights")

summary = leader.to_string()

prompt = f"""
Analyze this sales performance:

{summary}

Explain
Top performers
Weak performers
Sales opportunities
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

    st.warning("AI insights unavailable")

# ---------------- ASK AI ----------------

st.subheader("Ask AI About Sales")

question = st.text_input("Ask a question about your sales")

if question:

    prompt = f"""
Sales dataset:

{df.to_string()}

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

st.subheader("Full Sales Register")

st.dataframe(df)
