import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Parcl | Buyer Segmentation Intelligence", 
    page_icon="🏙️", 
    layout="wide"
)

st.title("🏙️ Buyer Segmentation & Investment Profiling Dashboard")
st.markdown("**Parcl Co. Limited | AI-Driven Real Estate Market Intelligence**")
st.markdown("---")

# Load processed data
@st.cache_data
def load_data():
    return pd.read_csv('processed_buyer_segments.csv')

df = load_data()

# Sidebar Filters
st.sidebar.header("🔍 Global Filters")

country_opts = df['country'].dropna().unique().tolist() if 'country' in df.columns else []
region_opts = df['region'].dropna().unique().tolist() if 'region' in df.columns else []
client_type_opts = df['client_type'].dropna().unique().tolist() if 'client_type' in df.columns else []

countries = st.sidebar.multiselect("Select Country", options=country_opts, default=country_opts)
regions = st.sidebar.multiselect("Select Region", options=region_opts, default=region_opts)
client_types = st.sidebar.multiselect("Select Client Type", options=client_type_opts, default=client_type_opts)

# Filter Data
filtered_df = df.copy()
if countries:
    filtered_df = filtered_df[filtered_df['country'].isin(countries)]
if regions:
    filtered_df = filtered_df[filtered_df['region'].isin(regions)]
if client_types:
    filtered_df = filtered_df[filtered_df['client_type'].isin(client_types)]

# PRD Dashboard Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Buyer Segmentation Overview", 
    "📈 Investor Behavior Dashboard", 
    "🗺️ Geographic Buyer Analysis", 
    "📑 Segment Insights Panel"
])

# Tab 1: Buyer Segmentation Overview
with tab1:
    st.subheader("Buyer Segment Distribution")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        counts = filtered_df['buyer_segment'].value_counts().reset_index()
        counts.columns = ['Buyer Segment', 'Count']
        st.dataframe(counts, use_container_width=True)
        
    with col2:
        fig_pie = px.pie(
            filtered_df, 
            names='buyer_segment', 
            title='Buyer Segment Proportions', 
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig_pie, use_container_width=True)

# Tab 2: Investor Behavior Dashboard
with tab2:
    st.subheader("Investment Purpose & Financing Patterns")
    col1, col2 = st.columns(2)
    
    with col1:
        if 'acquisition_purpose' in filtered_df.columns:
            fig_purpose = px.histogram(
                filtered_df, 
                x='buyer_segment', 
                color='acquisition_purpose', 
                barmode='group',
                title='Acquisition Purpose by Segment'
            )
            st.plotly_chart(fig_purpose, use_container_width=True)
            
    with col2:
        if 'loan_applied' in filtered_df.columns:
            fig_loan = px.histogram(
                filtered_df, 
                x='buyer_segment', 
                color='loan_applied', 
                barmode='group',
                title='Loan Application Status by Segment'
            )
            st.plotly_chart(fig_loan, use_container_width=True)

# Tab 3: Geographic Buyer Analysis
with tab3:
    st.subheader("Geographic Distribution Across Regions")
    if 'region' in filtered_df.columns:
        fig_geo = px.bar(
            filtered_df, 
            x='region', 
            color='buyer_segment', 
            title='Segment Distribution Across Regions',
            barmode='stack'
        )
        st.plotly_chart(fig_geo, use_container_width=True)

# Tab 4: Segment Insights Panel
with tab4:
    st.subheader("Descriptive Statistics per Cluster")
    metrics = [c for c in ['age', 'satisfaction_score', 'sale_price', 'floor_area_sqft'] if c in filtered_df.columns]
    
    if metrics:
        summary_df = filtered_df.groupby('buyer_segment')[metrics].mean().round(2)
        st.dataframe(summary_df, use_container_width=True)
    
    st.subheader("Raw Filtered Data")
    st.dataframe(filtered_df, use_container_width=True)