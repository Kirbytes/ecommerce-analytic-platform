import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="ASAP - Alimama Shop Analytics Platform", layout="wide")

# MySQL database connection
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",  # Update with your MySQL host
        user="root",  # Update with your MySQL username
        password="Editec@2022!",  # Update with your MySQL password
        database="alibaba_analysis"  # Database name
    )

# Query data from the database
@st.cache_data
def query_data(query):
    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    result = pd.DataFrame(cursor.fetchall())
    cursor.close()
    connection.close()
    return result

# Queries for data
dim_time_query = "SELECT * FROM dim_time;"
dim_product_query = "SELECT * FROM dim_product;"
dim_user_query = "SELECT * FROM dim_user;"
dim_shop_query = "SELECT * FROM dim_shop;"
fact_sales_query = "SELECT * FROM fact_sales;"

# Load data from the database
dim_time = query_data(dim_time_query)
dim_product = query_data(dim_product_query)
dim_user = query_data(dim_user_query)
dim_shop = query_data(dim_shop_query)
fact_sales = query_data(fact_sales_query)

# Add a logo and title
st.title("ASAP - Alibaba Shop Analytics Platform")
st.markdown("**Empowering sellers with actionable insights and analytics.**")

# Sidebar navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio(
    "Go to:", ["Dashboard", "Item Sales Trends", "User Targeting", "Risk Detection"]
)

# Dashboard Section
if menu == "Dashboard":
    st.subheader("📊 Dashboard")
    col1, col2, col3 = st.columns(3)

    with col1:
        total_views = fact_sales['total_views'].sum()
        st.metric("Total Views", f"{total_views:,}")

    with col2:
        avg_conversion_rate = fact_sales['conversion_rate'].mean()
        st.metric("Avg Conversion Rate", f"{avg_conversion_rate:.2%}")

    with col3:
        total_sales = fact_sales['total_purchases'].sum()
        st.metric("Total Sales", f"{total_sales:,}")

    st.markdown("---")

    # Dropdown for visualizations within Dashboard
    st.subheader("📊 Choose a Visualization")
    options = ["Sales by Category", "Sales by Gender", "Sales by Time"]
    choice = st.selectbox("Select a trend to view:", options)

    if choice == "Sales by Category":
        st.subheader("Sales Trends by Category")
        sales_trends = dim_product.groupby('category_list')['sales_level'].sum()
        fig, ax = plt.subplots(figsize=(3, 2))  # Adjusted figure size
        sales_trends.plot(kind='barh', ax=ax, color="#FF9F9B")
        ax.set_title("Sales by Category", fontsize=10)
        ax.set_xlabel("Category", fontsize=8)
        ax.set_ylabel("Sales Level", fontsize=8)
        st.pyplot(fig)

    elif choice == "Sales by Gender":
        st.subheader("Sales by Gender")
        gender_mapping = {-1: "Unspecified", 0: "Female", 1: "Male", 2: "Family"}
        gender_sales = fact_sales.merge(dim_user, on="user_id").groupby('gender_id')['total_views'].sum()
        gender_sales.index = gender_sales.index.map(gender_mapping)
        fig, ax = plt.subplots(figsize=(3, 2))
        gender_sales.plot(kind='barh', ax=ax, color="purple")
        ax.set_title("Sales by Gender", fontsize=10)
        ax.set_xlabel("Gender", fontsize=8)
        ax.set_ylabel("Total Sales", fontsize=8)
        st.pyplot(fig)

    elif choice == "Sales by Time":
        st.subheader("Sales Trends by Time")
        time_sales = fact_sales.merge(dim_time, on="time_key")
        daily_sales = time_sales.groupby('date_only')['total_views'].sum()
        fig, ax = plt.subplots(figsize=(6, 6))
        daily_sales.plot(kind='line', ax=ax, color="blue", marker='o')
    # Format the dates
    ax.set_title("Daily Sales Trends", fontsize=10)
    ax.set_xlabel("Date", fontsize=8)
    ax.set_ylabel("Total Purchases", fontsize=8)
    ax.tick_params(axis='y', labelsize=8)

    # Adjust date formatting and tick frequency
    ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))  # Include year
    #ax.xaxis.set_major_locator(plt.matplotlib.dates.DayLocator(interval=2))  # Show every 2nd day
    plt.xticks(rotation=45)  # Rotate labels for better readability

    plt.tight_layout()
    st.pyplot(fig)

# Item Sales Trends Section
elif menu == "Item Sales Trends":
    st.subheader("📦 Item Sales Trends")
    st.write("Explore sales trends and best-selling products.")

    # Display the table with container width adjustment
    st.subheader("Top Selling Items")
    top_items = dim_product.sort_values('sales_level', ascending=False).head(10)
    st.dataframe(top_items, use_container_width=True)  # Adjusts the table to fill the page


# User Targeting Section
elif menu == "User Targeting":
    st.subheader("🎯 User Targeting")
    st.write("Analyze user demographics and behavior for targeted campaigns.")

    # Dropdown for selecting demographic type
    demographic_choice = st.selectbox(
        "Select a demographic to analyze:",
        options=["Gender", "Age Group", "Occupation"]
    )

    # Prepare data based on the selected demographic
    if demographic_choice == "Gender":
        st.subheader("User Distribution by Gender")
        gender_counts = dim_user.groupby('gender_id')['user_id'].count()
        gender_mapping = {-1: "Unspecified", 0: "Female", 1: "Male", 2: "Family"}
        gender_counts.index = gender_counts.index.map(gender_mapping)  # Map gender IDs to labels

        # Plot the data
        fig, ax = plt.subplots(figsize=(6, 2))
        gender_counts.plot(kind='barh', ax=ax, color=["#4C72B0", "#FF9F9B", "#55A868", "#C44E52"])
        ax.set_title("User Count by Gender", fontsize=10)
        ax.set_xlabel("User Count", fontsize=8)
        ax.tick_params(axis='y', labelsize=8)
        ax.tick_params(axis='x', labelsize=8)
        plt.tight_layout()
        st.pyplot(fig)

    elif demographic_choice == "Age Group":
        st.subheader("User Distribution by Age Group")
        age_counts = dim_user.groupby('age_level')['user_id'].count()

        # Plot the data
        fig, ax = plt.subplots(figsize=(6, 2))
        age_counts.plot(kind='barh', ax=ax, color="#4C72B0")
        ax.set_title("User Count by Age Group", fontsize=10)
        ax.set_xlabel("User Count", fontsize=8)
        ax.tick_params(axis='y', labelsize=8)
        ax.tick_params(axis='x', labelsize=8)
        plt.tight_layout()
        st.pyplot(fig)

    elif demographic_choice == "Occupation":
        st.subheader("User Distribution by Occupation")
        occupation_counts = dim_user.groupby('occupation_id')['user_id'].count()

        # Plot the data
        fig, ax = plt.subplots(figsize=(6, 2))
        occupation_counts.plot(kind='barh', ax=ax, color="#55A868")
        ax.set_title("User Count by Occupation", fontsize=10)
        ax.set_xlabel("User Count", fontsize=8)
        ax.tick_params(axis='y', labelsize=8)
        ax.tick_params(axis='x', labelsize=8)
        plt.tight_layout()
        st.pyplot(fig)

# Risk Detection Section
elif menu == "Risk Detection":
    st.subheader("⚠️ Risk Detection")
    flagged_items = fact_sales[fact_sales['conversion_rate'] < 0.01]
    st.warning("Low-performing items detected! Review flagged items below.")
    st.dataframe(flagged_items.head(10))
    st.markdown("**Action Required:** Adjust marketing strategies for flagged items.")
