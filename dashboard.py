# dashboard.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Chennai Property Dashboard", layout="wide")

# Load data
df = pd.read_excel("chennai-properties-cleaned.xlsx")
df["price_per_sqft"] = (df["price_lakhs"] * 100000) / df["area_sqft"]

st.title("🏘️ Chennai Property Listings Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
bhk_filter = st.sidebar.multiselect("Select BHK Type", sorted(df["bhk"].dropna().unique()), default=df["bhk"].dropna().unique())
area_min, area_max = st.sidebar.slider("Area Range (sqft)", int(df["area_sqft"].min()), int(df["area_sqft"].max()), (600, 2000))
price_min, price_max = st.sidebar.slider("Price Range (Lakhs)", int(df["price_lakhs"].min()), int(df["price_lakhs"].max()), (50, 150))

# Apply filters
df_filtered = df[
    df["bhk"].isin(bhk_filter) &
    df["area_sqft"].between(area_min, area_max) &
    df["price_lakhs"].between(price_min, price_max)
]

st.subheader(f"Showing {len(df_filtered)} properties after filtering")

# Top Localities
st.markdown("### 📍 Top 10 Localities by Listings")
top_locations = df_filtered["location"].value_counts().head(10)
fig1, ax1 = plt.subplots()
sns.barplot(x=top_locations.values, y=top_locations.index, ax=ax1, palette="viridis")
ax1.set_xlabel("Number of Listings")
st.pyplot(fig1)

# BHK Distribution
st.markdown("### 🛏️ BHK Distribution")
fig2, ax2 = plt.subplots()
df_filtered["bhk"].value_counts().plot.pie(autopct="%1.1f%%", ax=ax2, colors=sns.color_palette("pastel"))
ax2.set_ylabel("")
st.pyplot(fig2)

# Area vs Price
st.markdown("### 📐 Area vs Price")
fig3, ax3 = plt.subplots()
sns.scatterplot(data=df_filtered, x="area_sqft", y="price_lakhs", hue="bhk", ax=ax3)
ax3.set_xlabel("Area (sqft)")
ax3.set_ylabel("Price (Lakhs)")
st.pyplot(fig3)
