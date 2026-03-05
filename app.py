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
    "Upload Excel / CSV / Image",
    type=["xlsx","csv","jpg","jpeg","png"]
)

df = None

if uploaded_file:

    ext = uploaded_file.name.split(".")[-1]

    # ---------- EXCEL ----------
    if ext in ["xlsx","csv"]:

        if ext == "xlsx":
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)

        df.columns = df.columns.str.strip()

        # -------- SMART COLUMN DETECTION --------

        for col in df.columns:

            c = col.lower()

            if "audio" in c and ("value" in c or "revenue" in c or "sales" in c):
                df.rename(columns={col:"Audio Revenue"}, inplace=True)

            if "watch" in c and ("value" in c or "revenue" in c or "sales" in c):
                df.rename(columns={col:"Watch Revenue"}, inplace=True)

            if "access" in c and ("value" in c or "revenue" in c or "sales" in c):
                df.rename(columns={col:"Accessories Revenue"}, inplace=True)

            if "audio" in c and ("qty" in c or "unit" in c):
                df.rename(columns={col:"Audio Qty"}, inplace=True)

            if "watch" in c and ("qty" in c or "unit" in c):
                df.rename(columns={col:"Watch Qty"}, inplace=True)

            if "access" in c and ("qty" in c or "unit" in c):
                df.rename(columns={col:"Accessories Qty"}, inplace=True)

    # ---------- IMAGE ----------
    else:

        st.image(uploaded_file)

        image_bytes = uploaded_file.getvalue()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[{
                "role":"user",
                "content":[
                    {"type":"input_text",
                     "text":"Extract this sales table and return CSV"},
                    {
                        "type":"input_image",
                        "image_url":f"data:image/jpeg;base64,{base64_image}"
                    }
                ]
            }]
        )

        extracted = response.output_text

        st.write(extracted)

        try:
            df = pd.read_csv(StringIO(extracted))
        except:
            st.error("Could not convert image")

# ---------------- DATA CHECK ----------------

if df is None:
    st.info("Upload a sales file to begin")
    st.stop()

required = [
"Audio Revenue",
"Watch Revenue",
"Accessories Revenue",
"Audio Qty",
"Watch Qty",
"Accessories Qty"
]

missing = [c for c in required if c not in df.columns]

if missing:
    st.error(f"Missing columns: {missing}")
    st.write("Detected columns:", df.columns)
    st.stop()

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

# ---------------- DASHBOARD ----------------

st.title("Evolution Inc AI Sales Intelligence")

col1,col2,col3 = st.columns(3)

total_sales = df["Total Revenue"].sum()
total_units = df["Total Qty"].sum()
asp = int(total_sales/total_units)

col1.metric("Total Revenue",f"₹{total_sales:,}")
col2.metric("Units Sold",total_units)
col3.metric("Average Selling Price",f"₹{asp}")

# ---------------- CATEGORY CHART ----------------

st.subheader("Category Revenue")

cat_df = pd.DataFrame({
"Category":["Audio","Watch","Accessories"],
"Revenue":[
df["Audio Revenue"].sum(),
df["Watch Revenue"].sum(),
df["Accessories Revenue"].sum()
]})

fig = px.bar(cat_df,x="Category",y="Revenue",color="Category")

st.plotly_chart(fig,use_container_width=True)

# ---------------- FORECAST ----------------

st.subheader("Next Month Forecast")

forecast = int(total_sales * 1.05)

st.title(f"₹{forecast:,}")

# ---------------- DATA ----------------

st.subheader("Sales Data")

st.dataframe(df)
