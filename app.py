import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Google Play Store Analysis",
    page_icon="📱",
    layout="wide"
)

st.title("📱 Google Play Store Data Analysis Dashboard")
st.write("Interactive analysis of Google Play Store applications")

# Load dataset
try:
    df = pd.read_csv("Play Store Data (1).csv")
except:
    uploaded_file = st.file_uploader(
        "Upload Google Play Store CSV Dataset",
        type=["csv"]
    )

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        st.info("Please upload the Google Play Store CSV dataset to view the dashboard.")
        st.stop()

# Clean column names
df.columns = df.columns.str.strip()

# Clean data
if "Rating" in df.columns:
    df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")

if "Reviews" in df.columns:
    df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce")

if "Installs" in df.columns:
    df["Installs"] = (
        df["Installs"]
        .astype(str)
        .str.replace("+", "", regex=False)
        .str.replace(",", "", regex=False)
    )
    df["Installs"] = pd.to_numeric(df["Installs"], errors="coerce")

if "Price" in df.columns:
    df["Price"] = (
        df["Price"]
        .astype(str)
        .str.replace("$", "", regex=False)
    )
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

# Sidebar
st.sidebar.header("🔍 Filters")

if "Category" in df.columns:
    categories = sorted(df["Category"].dropna().unique())
    selected_categories = st.sidebar.multiselect(
        "Select Category",
        categories,
        default=categories
    )
    filtered_df = df[df["Category"].isin(selected_categories)]
else:
    filtered_df = df.copy()

# Metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric("📱 Total Apps", len(filtered_df))

if "Rating" in filtered_df.columns:
    avg_rating = filtered_df["Rating"].mean()
    col2.metric(
        "⭐ Average Rating",
        f"{avg_rating:.2f}" if pd.notna(avg_rating) else "N/A"
    )
else:
    col2.metric("⭐ Average Rating", "N/A")

if "Installs" in filtered_df.columns:
    total_installs = filtered_df["Installs"].sum()
    col3.metric("⬇️ Total Installs", f"{total_installs:,.0f}")
else:
    col3.metric("⬇️ Total Installs", "N/A")

if "Reviews" in filtered_df.columns:
    total_reviews = filtered_df["Reviews"].sum()
    col4.metric("💬 Total Reviews", f"{total_reviews:,.0f}")
else:
    col4.metric("💬 Total Reviews", "N/A")

st.divider()

# Category-wise app count
if "Category" in filtered_df.columns:
    category_count = (
        filtered_df["Category"]
        .value_counts()
        .reset_index()
    )

    category_count.columns = ["Category", "Number of Apps"]

    fig1 = px.bar(
        category_count.head(15),
        x="Category",
        y="Number of Apps",
        title="📊 Top 15 Categories by Number of Apps"
    )

    fig1.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig1, use_container_width=True)

# Free vs Paid
if "Type" in filtered_df.columns:
    type_count = filtered_df["Type"].value_counts().reset_index()
    type_count.columns = ["Type", "Number of Apps"]

    fig2 = px.pie(
        type_count,
        names="Type",
        values="Number of Apps",
        title="💰 Free vs Paid Apps"
    )

    st.plotly_chart(fig2, use_container_width=True)

# Top apps by installs
if "App" in filtered_df.columns and "Installs" in filtered_df.columns:
    top_apps = (
        filtered_df[["App", "Installs"]]
        .dropna()
        .sort_values("Installs", ascending=False)
        .head(10)
    )

    fig3 = px.bar(
        top_apps.sort_values("Installs"),
        x="Installs",
        y="App",
        orientation="h",
        title="📈 Top 10 Apps by Number of Installs"
    )

    st.plotly_chart(fig3, use_container_width=True)

# Rating distribution
if "Rating" in filtered_df.columns:
    rating_data = filtered_df["Rating"].dropna()

    fig4 = px.histogram(
        rating_data,
        x="Rating",
        nbins=20,
        title="⭐ Rating Distribution"
    )

    st.plotly_chart(fig4, use_container_width=True)

# Data preview
st.subheader("📋 Dataset Preview")
st.dataframe(filtered_df.head(20), use_container_width=True)

st.success("✅ Google Play Store analysis completed successfully!")
