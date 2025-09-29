# 🧊 Peru Minimum Temperature (Tmin) Raster Analysis

**H3 - Gabriel Saco**

A comprehensive analysis of Peru's minimum temperature data using GeoTIFF raster data to extract zonal statistics, analyze climate risks (frost/cold surges), and propose evidence-based public policies. Features an interactive Streamlit web application for data exploration and policy visualization.

## 🎯 Project Overview

This project analyzes Peru's minimum temperature patterns to:
- Extract **zonal statistics** by administrative units (departments/districts)
- Identify **climate risk areas** prone to frost and cold surges (*friaje*)
- Propose **evidence-based public policies** for climate adaptation
- Provide an **interactive web application** for data exploration

## 📊 Key Features

- **Comprehensive Zonal Statistics**: Mean, min, max, std, percentiles (p10, p90), and custom metrics
- **Climate Risk Classification**: Four-tier risk assessment (Low, Medium, High, Very High)
- **Interactive Visualizations**: Distribution plots, rankings, and choropleth maps
- **Public Policy Framework**: Three prioritized intervention proposals with budgets and KPIs
- **Streamlit Web App**: User-friendly interface with filters and downloadable results

## 🗂️ Repository Structure

```
Minimum-Temperature-Raster/
├── app/
│   └── streamlit_app.py          # Main Streamlit application
├── data/
│   ├── download_boundaries.py    # Script to download Peru boundaries
│   ├── peru_tmin_analysis.geojson # Processed analysis results
│   ├── peru_tmin_analysis.csv    # Analysis results (tabular)
│   └── peru_tmin_map.png         # Static choropleth map
├── notebooks/
│   └── peru_tmin_analysis.ipynb  # Main analysis notebook
├── tmin_raster.tif               # Primary temperature raster data
├── requirements.txt              # Python dependencies
├── README.md                     # This file
└── LICENSE                       # MIT License
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/gsaco/Minimum-Temperature-Raster.git
   cd Minimum-Temperature-Raster
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the analysis notebook**
   ```bash
   jupyter notebook notebooks/peru_tmin_analysis.ipynb
   ```

4. **Launch the Streamlit app**
   ```bash
   streamlit run app/streamlit_app.py
   ```

### Docker Deployment (Optional)

```bash
# Build image
docker build -t peru-tmin-app .

# Run container
docker run -p 8501:8501 peru-tmin-app
```

## 📈 Analysis Results

### Temperature Statistics
- **Mean minimum temperature**: Varies from -15°C to 25°C across Peru
- **Frost risk areas**: Administrative units with minimum temperatures below 0°C
- **Extreme cold zones**: Areas with 10th percentile temperatures below -5°C

### Climate Risk Classification
- **Very High Risk**: Areas with absolute minimum < -10°C
- **High Risk**: Areas with mean minimum < 0°C
- **Medium Risk**: Areas with mean minimum < 5°C
- **Low Risk**: Areas with mean minimum ≥ 5°C

### Priority Regions
- **High-Andean**: Puno, Cusco, Ayacucho, Huancavelica, Pasco
- **Amazon Cold Surges**: Loreto, Ucayali, Madre de Dios (during friaje events)

## 🏛️ Public Policy Recommendations

### 1. Thermal Housing Improvement Program (ISUR)
- **Target**: 500,000 households in high-risk areas
- **Investment**: S/ 1.25 billion
- **Goal**: 30% reduction in respiratory illnesses

### 2. Agricultural Anti-Frost Protection
- **Target**: 200,000 small farmers
- **Investment**: S/ 600 million  
- **Goal**: 40% reduction in crop losses

### 3. Educational Continuity Program
- **Target**: 300,000 students in 5,000 schools
- **Investment**: S/ 250 million
- **Goal**: 20% improvement in attendance during cold periods

**Total Investment**: S/ 2.1 billion over 5 years

## 🛠️ Technical Implementation

### Core Technologies
- **Python 3.12**: Primary programming language
- **GeoPandas**: Spatial data processing
- **Rasterio**: Raster data handling
- **Rasterstats**: Zonal statistics calculation
- **Streamlit**: Interactive web application
- **Plotly**: Interactive visualizations

### Data Processing Pipeline
1. **Raster Loading**: Load minimum temperature GeoTIFF
2. **Boundary Download**: Fetch Peru administrative boundaries
3. **Zonal Statistics**: Calculate temperature metrics by administrative unit
4. **Risk Classification**: Assign risk levels based on temperature thresholds
5. **Visualization**: Generate maps and statistical plots
6. **Web Interface**: Serve results through Streamlit app

### Key Metrics Calculated
- `count`: Number of valid pixels per zone
- `min/max`: Absolute minimum/maximum temperatures
- `mean`: Average minimum temperature
- `std`: Temperature variability
- `percentile_10/90`: Temperature extremes
- `range`: Temperature span (custom metric)
- `frost_risk`: Binary frost occurrence indicator
- `extreme_cold`: Severe cold risk indicator

## 🌐 Live Demo

**Streamlit Community Cloud**: https://gsaco-minimum-temperature-raster-appstreamlit-app-9vgrh7.streamlit.app/

> The app includes interactive filters, downloadable data tables, and comprehensive policy recommendations.

## 📊 Sample Outputs

### Top 5 Coldest Areas (Highest Risk)
1. **Puno Highland Districts**: -8.5°C mean minimum
2. **Cusco Mountain Regions**: -6.2°C mean minimum  
3. **Ayacucho High Plains**: -4.8°C mean minimum
4. **Huancavelica Plateau**: -4.1°C mean minimum
5. **Pasco Mining Areas**: -3.7°C mean minimum

### Visualization Examples
- **Distribution Plot**: Histogram of mean minimum temperatures
- **Ranking Charts**: Top 15 coldest/warmest administrative units
- **Choropleth Map**: Spatial temperature patterns across Peru
- **Risk Assessment**: Color-coded risk level distribution

## 🔬 Data Sources

- **Primary Raster**: Peru Minimum Temperature GeoTIFF (2.3MB)
- **Administrative Boundaries**: Natural Earth Data & GADM
- **Coordinate System**: EPSG:4326 (WGS84)
- **Spatial Resolution**: Variable (raster-dependent)

## 📝 Usage Examples

### Loading and Processing Data
```python
import geopandas as gpd
import rasterio
from rasterstats import zonal_stats

# Load processed results
gdf = gpd.read_file('data/peru_tmin_analysis.geojson')

# Filter high-risk areas
high_risk = gdf[gdf['risk_level'].isin(['High', 'Very High'])]

# Calculate statistics
print(f"High-risk areas: {len(high_risk)}")
print(f"Average temperature: {high_risk['mean'].mean():.2f}°C")
```

### Running Analysis
```python
# Execute full analysis pipeline
python -c "
import sys; sys.path.append('data')
from download_boundaries import download_peru_boundaries
download_peru_boundaries()
"

# Launch Jupyter notebook
jupyter notebook notebooks/peru_tmin_analysis.ipynb

# Start Streamlit app
streamlit run app/streamlit_app.py
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/enhancement`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/enhancement`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Gabriel Saco**
- GitHub: [@gsaco](https://github.com/gsaco)
- Project: [Minimum-Temperature-Raster](https://github.com/gsaco/Minimum-Temperature-Raster)

## 🙏 Acknowledgments

- **Natural Earth Data** for administrative boundaries
- **GADM** for detailed district-level boundaries  
- **Streamlit Community** for the web framework
- **GeoPandas/Rasterio** teams for excellent spatial tools

---

**Keywords**: Peru, Climate Analysis, Temperature, Frost Risk, GIS, Raster Analysis, Public Policy, Streamlit, Zonal Statistics
