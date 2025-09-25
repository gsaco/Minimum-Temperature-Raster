#!/usr/bin/env python3
"""
🧊 Peru Minimum Temperature (Tmin) Raster Analysis
Interactive Streamlit App for Climate Risk Analysis and Public Policy

This app provides:
- Interactive visualization of Peru's minimum temperature data
- Zonal statistics by administrative units
- Climate risk analysis (frost/cold surges)
- Evidence-based public policy recommendations
"""

import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import base64
from io import BytesIO
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="🧊 Peru Minimum Temperature Analysis",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(90deg, #f0f8ff 0%, #e6f3ff 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .risk-high {
        background: linear-gradient(90deg, #ffe6e6 0%, #ffcccc 100%);
        border-left: 5px solid #ff4444;
    }
    .risk-medium {
        background: linear-gradient(90deg, #fff8e6 0%, #ffebcc 100%);
        border-left: 5px solid #ff8800;
    }
    .policy-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load the processed analysis data."""
    base_path = Path(__file__).parent.parent
    data_path = base_path / 'data'
    
    try:
        # Try to load GeoJSON data
        geojson_path = data_path / 'peru_tmin_analysis.geojson'
        if geojson_path.exists():
            gdf = gpd.read_file(geojson_path)
            return gdf, True
        else:
            st.error("Analysis data not found. Please run the notebook first.")
            return None, False
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, False

def create_download_link(df, filename, link_text):
    """Create a download link for dataframe."""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">{link_text}</a>'

def plot_distribution(data, column, title):
    """Create distribution plot."""
    fig = px.histogram(
        data, 
        x=column, 
        nbins=30,
        title=title,
        labels={column: 'Temperature (°C)', 'count': 'Frequency'},
        color_discrete_sequence=['#1f77b4']
    )
    fig.add_vline(
        x=data[column].mean(), 
        line_dash="dash", 
        line_color="red",
        annotation_text=f"Mean: {data[column].mean():.2f}°C"
    )
    return fig

def plot_ranking(data, column, title, n_areas=15, ascending=True):
    """Create ranking plot."""
    if ascending:
        top_data = data.nsmallest(n_areas, column)
        color = '#ff6b6b'
    else:
        top_data = data.nlargest(n_areas, column)
        color = '#4ecdc4'
    
    fig = px.bar(
        top_data, 
        x=column, 
        y='NAME_CLEAN',
        orientation='h',
        title=title,
        labels={column: 'Temperature (°C)', 'NAME_CLEAN': 'Administrative Unit'},
        color_discrete_sequence=[color]
    )
    fig.update_layout(height=600)
    return fig

def main():
    # Main header
    st.markdown('<h1 class="main-header">🧊 Peru Minimum Temperature Analysis</h1>', unsafe_allow_html=True)
    st.markdown("### Climate Risk Analysis and Evidence-Based Public Policy Recommendations")
    
    # Load data
    data, success = load_data()
    if not success or data is None:
        st.stop()
    
    # Sidebar filters
    st.sidebar.header("🔧 Filters and Controls")
    
    # Temperature threshold filter
    temp_threshold = st.sidebar.slider(
        "Temperature Threshold (°C)", 
        min_value=float(data['mean'].min()), 
        max_value=float(data['mean'].max()),
        value=0.0,
        help="Filter areas below this temperature threshold"
    )
    
    # Risk level filter
    risk_levels = data['risk_level'].unique() if 'risk_level' in data.columns else ['All']
    selected_risks = st.sidebar.multiselect(
        "Risk Levels",
        options=risk_levels,
        default=risk_levels,
        help="Select risk levels to display"
    )
    
    # Filter data
    filtered_data = data[data['mean'] <= temp_threshold] if temp_threshold < data['mean'].max() else data
    if 'risk_level' in data.columns and selected_risks:
        filtered_data = filtered_data[filtered_data['risk_level'].isin(selected_risks)]
    
    # Main content area
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Areas", len(filtered_data))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Mean Temperature", f"{filtered_data['mean'].mean():.2f}°C")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        frost_risk_count = filtered_data['frost_risk'].sum() if 'frost_risk' in filtered_data.columns else 0
        st.markdown('<div class="metric-card risk-high">', unsafe_allow_html=True)
        st.metric("Frost Risk Areas", frost_risk_count)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        extreme_cold_count = filtered_data['extreme_cold'].sum() if 'extreme_cold' in filtered_data.columns else 0
        st.markdown('<div class="metric-card risk-high">', unsafe_allow_html=True)
        st.metric("Extreme Cold Areas", extreme_cold_count)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Statistics & Visualizations", "🗺️ Maps", "📋 Data Tables", "🏛️ Public Policy"])
    
    with tab1:
        st.header("📊 Statistical Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Temperature Distribution")
            dist_fig = plot_distribution(filtered_data, 'mean', 'Distribution of Mean Minimum Temperatures')
            st.plotly_chart(dist_fig, use_container_width=True)
        
        with col2:
            st.subheader("Temperature Statistics")
            stats_data = filtered_data[['mean', 'min', 'max']].describe().round(2)
            st.dataframe(stats_data)
        
        # Ranking plots
        st.subheader("🥶 Coldest Areas (Highest Risk)")
        cold_fig = plot_ranking(filtered_data, 'mean', 'Top 15 Coldest Areas', ascending=True)
        st.plotly_chart(cold_fig, use_container_width=True)
        
        st.subheader("🔥 Warmest Areas (Lowest Risk)")
        warm_fig = plot_ranking(filtered_data, 'mean', 'Top 15 Warmest Areas', ascending=False)
        st.plotly_chart(warm_fig, use_container_width=True)
    
    with tab2:
        st.header("🗺️ Spatial Analysis")
        
        # Check if map image exists
        base_path = Path(__file__).parent.parent
        map_path = base_path / 'data' / 'peru_tmin_map.png'
        
        if map_path.exists():
            st.subheader("Peru Minimum Temperature Map")
            st.image(str(map_path), caption="Mean Minimum Temperature by Administrative Unit")
        
        # Interactive map with plotly (if coordinates available)
        if 'geometry' in filtered_data.columns:
            try:
                # Get centroids for plotting
                centroids = filtered_data.geometry.centroid
                filtered_data['lon'] = centroids.x
                filtered_data['lat'] = centroids.y
                
                st.subheader("Interactive Temperature Map")
                fig = px.scatter_mapbox(
                    filtered_data,
                    lat='lat',
                    lon='lon',
                    color='mean',
                    size='range',
                    hover_name='NAME_CLEAN',
                    hover_data=['mean', 'min', 'max', 'risk_level'],
                    color_continuous_scale='RdYlBu_r',
                    mapbox_style='open-street-map',
                    title='Peru Minimum Temperature - Interactive Map'
                )
                fig.update_layout(height=600)
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not create interactive map: {e}")
    
    with tab3:
        st.header("📋 Data Tables and Downloads")
        
        st.subheader("Filtered Data Summary")
        
        # Display key columns
        display_columns = ['NAME_CLEAN', 'mean', 'min', 'max', 'std', 'risk_level']
        available_columns = [col for col in display_columns if col in filtered_data.columns]
        
        st.dataframe(
            filtered_data[available_columns].sort_values('mean').reset_index(drop=True),
            use_container_width=True
        )
        
        # Download section
        st.subheader("📥 Download Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Download Filtered Data (CSV)"):
                csv_data = filtered_data.drop(columns=['geometry']) if 'geometry' in filtered_data.columns else filtered_data
                csv = csv_data.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="peru_tmin_filtered.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("📈 Download Full Dataset (CSV)"):
                csv_data = data.drop(columns=['geometry']) if 'geometry' in data.columns else data
                csv = csv_data.to_csv(index=False)
                st.download_button(
                    label="Download Full CSV",
                    data=csv,
                    file_name="peru_tmin_complete.csv",
                    mime="text/csv"
                )
    
    with tab4:
        st.header("🏛️ Public Policy Recommendations")
        
        st.markdown("""
        Based on the minimum temperature analysis, here are evidence-based public policy recommendations 
        to mitigate the impact of frost and cold surges (*friaje*) in Peru:
        """)
        
        # Policy 1
        st.markdown('<div class="policy-card">', unsafe_allow_html=True)
        st.subheader("🏠 Policy 1: Thermal Housing Improvement Program (ISUR)")
        st.markdown("""
        **Objective:** Reduce respiratory illnesses (ILI/ARI) and hypothermia cases in high-risk areas
        
        **Target Population:** 
        - Households in areas with mean minimum temperature ≤ 0°C
        - Estimated 500,000 households in high-Andean regions (Puno, Cusco, Ayacucho, Huancavelica)
        
        **Intervention:**
        - Thermal insulation packages for homes
        - Improved cooking stoves (cocinas mejoradas)
        - Emergency heating equipment distribution
        
        **Estimated Cost:** S/ 2,500 per household × 500,000 = **S/ 1.25 billion**
        
        **KPIs:**
        - Reduce ARI cases by 30% in target areas (MINSA data)
        - Decrease hypothermia deaths by 50%
        - Improve indoor temperature by 5-8°C
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Policy 2
        st.markdown('<div class="policy-card">', unsafe_allow_html=True)
        st.subheader("🌾 Policy 2: Agricultural Anti-Frost Protection")
        st.markdown("""
        **Objective:** Reduce agricultural losses from frost events
        
        **Target Population:**
        - 200,000 small farmers in areas with frost risk (min < 0°C)
        - Focus on potato, quinoa, and livestock regions
        
        **Intervention:**
        - Anti-frost technology kits (water sprinklers, wind machines)
        - Crop calendar optimization based on temperature forecasts
        - Livestock shelter construction
        - Crop insurance expansion
        
        **Estimated Cost:** S/ 3,000 per farm × 200,000 = **S/ 600 million**
        
        **KPIs:**
        - Reduce crop losses by 40% during frost events
        - Decrease alpaca/llama mortality by 25%
        - Increase agricultural productivity by 15%
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Policy 3
        st.markdown('<div class="policy-card">', unsafe_allow_html=True)
        st.subheader("🎒 Policy 3: Educational Continuity Program")
        st.markdown("""
        **Objective:** Maintain school attendance during extreme cold periods
        
        **Target Population:**
        - 300,000 students in schools located in extreme cold areas (p10 < -5°C)
        - 5,000 schools in high-Andean regions
        
        **Intervention:**
        - School heating systems installation
        - Winter clothing distribution program
        - Mobile health units during cold surges
        - Flexible academic calendar adaptation
        
        **Estimated Cost:** S/ 50,000 per school × 5,000 = **S/ 250 million**
        
        **KPIs:**
        - Increase school attendance by 20% during cold months
        - Reduce cold-related absences by 60%
        - Improve academic performance in affected areas by 10%
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Summary
        st.subheader("📊 Policy Impact Summary")
        
        policy_summary = pd.DataFrame({
            'Policy': ['Thermal Housing (ISUR)', 'Agricultural Protection', 'Educational Continuity'],
            'Target Population': ['500,000 households', '200,000 farmers', '300,000 students'],
            'Investment (S/)': ['1.25 billion', '600 million', '250 million'],
            'Primary KPI': ['30% reduction ARI', '40% less crop losses', '20% better attendance']
        })
        
        st.dataframe(policy_summary, use_container_width=True)
        
        st.markdown("""
        **Total Investment:** S/ 2.1 billion over 5 years
        
        **Implementation Priority:**
        1. **High Priority:** Areas with mean temperature < -2°C
        2. **Medium Priority:** Areas with mean temperature 0-2°C  
        3. **Monitor:** Areas with significant temperature variability
        
        **Financing Sources:**
        - World Bank climate adaptation funds
        - Government budget allocation
        - International cooperation (UN Green Climate Fund)
        - Private sector partnerships
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    **Data Sources:** Peru Minimum Temperature Raster Analysis | **Analysis Level:** Administrative Districts/Departments
    
    **Methodology:** Zonal statistics using rasterstats library | **Risk Classification:** Based on temperature thresholds and percentiles
    """)

if __name__ == "__main__":
    main()