import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Evolution Inc Dashboard", layout="wide")

st.title("Evolution Inc Sales Intelligence Dashboard")

uploaded_file = st.file_uploader("Upload Sales Excel File", type=["xlsx"])

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    # Convert Date
    df["Date"] = pd.to_datetime(df["Date"])

    # Total quantity
    df["TotalQty"] = df["Watches"] + df["Audio"] + df["Accessories"]

    # Unit price
    df["UnitPrice"] = df["Amount"] / df["TotalQty"]

    # Revenue allocation
    df["WatchRevenue"] = df["Watches"] * df["UnitPrice"]
    df["AudioRevenue"] = df["Audio"] * df["UnitPrice"]
    df["AccessoriesRevenue"] = df["Accessories"] * df["UnitPrice"]

    # Top metrics
    total_sales = df["Amount"].sum()
    total_units = df["TotalQty"].sum()
    overall_asp = total_sales / total_units

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Sales", f"₹{total_sales:,.0f}")
    col2.metric("Total Units", int(total_units))
    col3.metric("Overall ASP", f"₹{overall_asp:,.0f}")

    st.divider()

    # ASP by category
    watch_asp = df["WatchRevenue"].sum() / df["Watches"].sum()
    audio_asp = df["AudioRevenue"].sum() / df["Audio"].sum()
    accessories_asp = df["AccessoriesRevenue"].sum() / df["Accessories"].sum()

    st.subheader("Average Selling Price by Category")

    c1, c2, c3 = st.columns(3)

    c1.metric("Watches ASP", f"₹{watch_asp:,.0f}")
    c2.metric("Audio ASP", f"₹{audio_asp:,.0f}")
    c3.metric("Accessories ASP", f"₹{accessories_asp:,.0f}")

    st.divider()

    # Dealer analytics
    st.subheader("Dealer Analytics")

    dealer_sales = df.groupby("Dealer").agg({
        "Amount": "sum",
        "TotalQty": "sum"
    }).reset_index()

    dealer_sales["ASP"] = dealer_sales["Amount"] / dealer_sales["TotalQty"]

    fig1 = px.bar(
        dealer_sales.sort_values("Amount", ascending=False),
        x="Dealer",
        y="Amount",
        color="Amount",
        title="Dealer Revenue"
    )

    st.plotly_chart(fig1, use_container_width=True)

    st.dataframe(dealer_sales.sort_values("Amount", ascending=False))

    st.divider()

    # Category performance
    st.subheader("Category Performance")

    category_data = {
        "Category": ["Watches", "Audio", "Accessories"],
        "Units": [
            df["Watches"].sum(),
            df["Audio"].sum(),
            df["Accessories"].sum()
        ]
    }

    cat_df = pd.DataFrame(category_data)

    fig2 = px.pie(cat_df, names="Category", values="Units")

    st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # Region analytics
    st.subheader("Region Performance")

    region_sales = df.groupby("Region")["Amount"].sum().reset_index()

    fig3 = px.bar(
        region_sales,
