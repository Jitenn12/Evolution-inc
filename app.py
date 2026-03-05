import streamlit as st
import pandas as pd
import plotly.express as px
import base64
from openai import OpenAI

st.set_page_config(layout="wide")

# ---------------- LOGIN ----------------

users = {
    "admin": "9326297095",
    "analyst": "evolution123"
}

st.sidebar.title("Login")

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if username not in users or users[username] != password:
    st.warning("Please login")
    st.stop()

# ---------------- OPENAI CLIENT ----------------

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------- DATA UPLOAD ----------------

st.sidebar.subheader("Upload Sales Data")

uploaded_file = st.sidebar.file_uploader(
    "Upload Excel / CSV / Image",
    type=["xlsx","csv","png","jpg","jpeg"]
)

df = None

if uploaded_file is not None:

    file_type = uploaded_file.name.split(".")[-1]

    # ---------- EXCEL ----------
    if file_type in ["xlsx","csv"]:

        if file_type == "csv":
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("Excel data loaded")

    # ---------- IMAGE ----------
    else:

        st.image(uploaded_file, caption="Uploaded Sales Sheet")

        image_bytes = uploaded_file.getvalue()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[{
                "role":"user",
                "content":[
                    {"type":"input_text","text":"Extract the sales table from this image. Return CSV format."},
                    {
                        "type":"input_image",
                        "image_url":f"data:image/jpeg;base64,{base64_image}"
                    }
                ]
            }]
        )

        extracted = response.output_text

        st.subheader("Extracted Data")
        st.write(extracted)

        try:
            from io import StringIO
            df = pd.read_csv(StringIO(extracted))
        except:
            st.warning("Could not convert image to table")

else:

    st.info("Upload sales data")
    st.stop()

# ---------------- DASHBOARD ----------------

st.title("Evolution Inc AI Sales Intelligence")

# Ensure columns exist
required = ["Month","Zone","Salesman","Audio Revenue","Watch Revenue","Accessories Revenue","Audio Qty","Watch Qty","Accessories Qty"]

missing = [c for c in required if c not in df.columns]

if missing:
    st.warning(f"Missing columns: {missing}")
    st.stop()

# Totals

df["Total Revenue"] = df["Audio Revenue"] + df["Watch Revenue"] + df["Accessories Revenue"]
df["Total Qty"] = df["Audio Qty"] + df["Watch Qty"] + df["Accessories Qty"]

# ---------------- FILTERS ----------------

st.sidebar.subheader("Filters")

month = st.sidebar.multiselect("Month",df["Month"].unique(),df["Month"].unique())
zone = st.sidebar.multiselect("Zone",df["Zone"].unique(),df["Zone"].unique())
salesman = st.sidebar.multiselect("Salesman",df["Salesman"].unique(),df["Salesman"].unique())

filtered = df[
(df["Month"].isin(month)) &
(df["Zone"].isin(zone)) &
(df["Salesman"].isin(salesman))
]

# ---------------- KPIs ----------------

col1,col2,col3 = st.columns(3)

col1.metric("Total Revenue",f"₹{filtered['Total Revenue'].sum():,}")
col2.metric("Units Sold",filtered["Total Qty"].sum())

asp = int(filtered["Total Revenue"].sum()/filtered["Total Qty"].sum())
col3.metric("Average Selling Price",f"₹{asp}")

# ---------------- CATEGORY CHART ----------------

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

# ---------------- FORECAST ----------------

st.subheader("Forecast")

forecast = int(filtered["Total Revenue"].sum()*1.05)

st.write("Predicted Next Month Revenue")

st.title(f"₹{forecast:,}")

# ---------------- LEADERBOARD ----------------

st.divider()

st.subheader("Salesman Leaderboard")

leaderboard = filtered.groupby("Salesman")["Total Revenue"].sum().reset_index()

leaderboard = leaderboard.sort_values("Total Revenue",ascending=False)

leaderboard["Rank"] = range(1,len(leaderboard)+1)

st.dataframe(leaderboard)

# ---------------- ZONE HEATMAP ----------------

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

# ---------------- AI INSIGHTS ----------------

st.divider()

st.subheader("AI Business Insights")

summary = filtered.groupby("Salesman")["Total Revenue"].sum().reset_index()

prompt = f"""
Analyze this sales dataset:

{summary.to_string()}

Explain:
Top performers
Weak zones
Opportunities
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

# ---------------- ASK AI ----------------

st.divider()

st.subheader("Ask AI About Sales")

question = st.text_input("Ask about sales")

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

# ---------------- DATA TABLE ----------------

st.divider()

st.subheader("Full Data")

st.dataframe(filtered)
