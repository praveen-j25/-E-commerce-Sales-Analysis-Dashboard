import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from ecommerce_analysis import EcommerceAnalyzer
import os
import base64
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="E-commerce Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 E-commerce Sales Analysis Dashboard")

# Initialize the analyzer
@st.cache_data
def load_data():
    analyzer = EcommerceAnalyzer('data/ecommerce_data.csv')
    analyzer.clean_data()
    return analyzer

analyzer = load_data()

# Download functionality
def get_download_link(df, filename, text):
    """Generates a link to download the dataframe as a CSV file"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href

# Sidebar for downloads
st.sidebar.header("📥 Export Data")
st.sidebar.subheader("Download Analysis Reports")

# Create download buttons for different reports
if st.sidebar.button("📊 Download Full Analysis Report"):
    report = analyzer.generate_report()
    report_df = pd.DataFrame(report)
    st.sidebar.markdown(get_download_link(
        report_df,
        f"ecommerce_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        "⬇️ Download Full Report"
    ), unsafe_allow_html=True)

if st.sidebar.button("📦 Download Product Analysis"):
    product_analysis = analyzer.analyze_top_products()
    st.sidebar.markdown(get_download_link(
        product_analysis,
        f"product_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        "⬇️ Download Product Analysis"
    ), unsafe_allow_html=True)

if st.sidebar.button("🌍 Download Regional Analysis"):
    regional_analysis = analyzer.analyze_regional_performance()
    st.sidebar.markdown(get_download_link(
        regional_analysis,
        f"regional_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        "⬇️ Download Regional Analysis"
    ), unsafe_allow_html=True)

if st.sidebar.button("💳 Download Payment Analysis"):
    payment_analysis = analyzer.analyze_payment_methods()
    st.sidebar.markdown(get_download_link(
        payment_analysis,
        f"payment_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        "⬇️ Download Payment Analysis"
    ), unsafe_allow_html=True)

# Overview Section
st.header("📈 Overview")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Orders", f"{analyzer.df.shape[0]:,}")
with col2:
    st.metric("Total Revenue", f"₹{analyzer.df['total_price'].sum():,.2f}")
with col3:
    st.metric("Average Order Value", f"₹{analyzer.df['total_price'].mean():,.2f}")
with col4:
    st.metric("Total Customers", f"{analyzer.df['customer_id'].nunique():,}")

# Product Analysis
st.header("📦 Product Analysis")
product_analysis = analyzer.analyze_top_products()

# Create two columns for product visualizations
col1, col2 = st.columns(2)

with col1:
    fig = px.bar(
        product_analysis.head(),
        x=product_analysis.head().index,
        y='Total Revenue (₹)',
        title='Top Product Categories by Revenue',
        labels={'x': 'Product Category', 'y': 'Revenue (₹)'}
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.pie(
        product_analysis,
        values='Units Sold',
        names=product_analysis.index,
        title='Product Distribution by Units Sold'
    )
    st.plotly_chart(fig, use_container_width=True)

# Regional Analysis
st.header("🌍 Regional Analysis")
regional_analysis = analyzer.analyze_regional_performance()

# Create two columns for regional visualizations
col1, col2 = st.columns(2)

with col1:
    fig = px.bar(
        regional_analysis.head(),
        x=regional_analysis.head().index,
        y='Total Revenue (₹)',
        title='Top Cities by Revenue',
        labels={'x': 'City', 'y': 'Revenue (₹)'}
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.scatter(
        regional_analysis,
        x='Number of Orders',
        y='Avg Order Value (₹)',
        size='Total Revenue (₹)',
        color=regional_analysis.index,
        title='City Performance Analysis',
        labels={'x': 'Number of Orders', 'y': 'Average Order Value (₹)'}
    )
    st.plotly_chart(fig, use_container_width=True)

# Payment Analysis
st.header("💳 Payment Method Analysis")
payment_analysis = analyzer.analyze_payment_methods()

# Create two columns for payment visualizations
col1, col2 = st.columns(2)

with col1:
    fig = px.bar(
        payment_analysis,
        x=payment_analysis.index,
        y='Number of Orders',
        title='Payment Method Distribution',
        labels={'x': 'Payment Method', 'y': 'Number of Orders'}
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.pie(
        payment_analysis,
        values='Total Revenue (₹)',
        names=payment_analysis.index,
        title='Revenue Distribution by Payment Method'
    )
    st.plotly_chart(fig, use_container_width=True)

# Customer Behavior
st.header("👥 Customer Behavior")
customer_behavior = analyzer.analyze_customer_behavior()

# Create two columns for customer behavior visualizations
col1, col2 = st.columns(2)

with col1:
    st.subheader("Purchase Frequency Statistics")
    st.dataframe(customer_behavior['purchase_frequency'].describe())

with col2:
    st.subheader("Top Cities by Customer Count")
    city_distribution = customer_behavior['city_distribution'].head()
    fig = px.bar(
        x=city_distribution.index,
        y=city_distribution.values,
        title='Top Cities by Customer Count',
        labels={'x': 'City', 'y': 'Number of Customers'}
    )
    st.plotly_chart(fig, use_container_width=True)

# Add a section for raw data download
st.sidebar.header("📊 Raw Data")
if st.sidebar.button("📥 Download Raw Dataset"):
    st.sidebar.markdown(get_download_link(
        analyzer.df,
        f"raw_ecommerce_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        "⬇️ Download Raw Dataset"
    ), unsafe_allow_html=True) 