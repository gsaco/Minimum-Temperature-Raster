# 🚀 Deployment Guide - Peru Minimum Temperature Analysis

This guide provides multiple deployment options for the Peru Minimum Temperature Analysis application.

## 📋 Prerequisites

- Python 3.10+
- Git
- Docker (optional, for containerized deployment)

## 🎯 Quick Start (Local Development)

### 1. Clone and Setup
```bash
git clone https://github.com/gsaco/Minimum-Temperature-Raster.git
cd Minimum-Temperature-Raster

# Test project structure
python test_setup.py

# Create sample data for demonstration
python create_sample_data.py

# Run basic analysis demo
python simple_demo.py
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Analysis Notebook
```bash
jupyter notebook notebooks/peru_tmin_analysis.ipynb
```

### 4. Launch Streamlit App
```bash
streamlit run app/streamlit_app.py
```
Access at: http://localhost:8501

## 🐳 Docker Deployment

### Option 1: Docker Compose (Recommended)
```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d --build

# Stop
docker-compose down
```

### Option 2: Manual Docker
```bash
# Build image
docker build -t peru-tmin-app .

# Run container
docker run -p 8501:8501 peru-tmin-app

# Run with volume mounting (for development)
docker run -p 8501:8501 -v ./data:/app/data peru-tmin-app
```

## ☁️ Streamlit Community Cloud

### 1. Prepare Repository
Ensure your repository has:
- [x] `app/streamlit_app.py` (main app file)
- [x] `requirements.txt` (dependencies)
- [x] Sample data in `data/` directory
- [x] All necessary files committed to main branch

### 2. Deploy to Streamlit Cloud
1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub account
3. Select repository: `gsaco/Minimum-Temperature-Raster`
4. Main file path: `app/streamlit_app.py`
5. Python version: 3.12
6. Click "Deploy"

### 3. Configuration
Create `app/.streamlit/config.toml` for custom settings:
```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f8ff"

[server]
maxUploadSize = 50
```

## 🌐 Production Deployment Options

### Heroku
```bash
# Install Heroku CLI
# Create Procfile
echo "web: streamlit run app/streamlit_app.py --server.port=$PORT --server.address=0.0.0.0" > Procfile

# Deploy
heroku create peru-tmin-analysis
git push heroku main
```

### AWS EC2
```bash
# Launch EC2 instance (Ubuntu 20.04+)
# SSH into instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Install dependencies
sudo apt update
sudo apt install python3-pip git
pip3 install -r requirements.txt

# Run with nohup
nohup streamlit run app/streamlit_app.py --server.port=8501 --server.address=0.0.0.0 &
```

### Google Cloud Run
```bash
# Build for Cloud Run
gcloud builds submit --tag gcr.io/YOUR_PROJECT/peru-tmin

# Deploy
gcloud run deploy --image gcr.io/YOUR_PROJECT/peru-tmin --platform managed
```

## 📊 Data Management

### Full Analysis Setup
For complete analysis with real boundary data:

```bash
# Run boundary download script
cd data
python download_boundaries.py

# Execute full notebook analysis
jupyter notebook ../notebooks/peru_tmin_analysis.ipynb
```

### Custom Raster Data
Replace `tmin_raster.tif` with your own GeoTIFF:
1. Ensure CRS is EPSG:4326 or compatible
2. Update notebook parameters if needed
3. Re-run analysis: `jupyter notebook notebooks/peru_tmin_analysis.ipynb`

## 🔧 Configuration Options

### Environment Variables
```bash
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_THEME_PRIMARY_COLOR="#1f77b4"
```

### App Configuration
Edit `app/streamlit_app.py` to customize:
- Page title and icon
- Color schemes
- Default filter values
- Policy recommendations

## 🧪 Testing and Validation

### Run Tests
```bash
# Project structure test
python test_setup.py

# Create sample data
python create_sample_data.py

# Run analysis demo
python simple_demo.py

# Test Streamlit app (requires dependencies)
streamlit run app/streamlit_app.py --server.headless true
```

### Health Checks
```bash
# Docker health check
curl http://localhost:8501/_stcore/health

# App availability
curl http://localhost:8501
```

## 🐛 Troubleshooting

### Common Issues

**Package Installation Errors:**
```bash
# Update pip
pip install --upgrade pip

# Install with no-cache
pip install --no-cache-dir -r requirements.txt

# Use conda instead
conda env create -f environment.yml
```

**Streamlit Port Issues:**
```bash
# Use different port
streamlit run app/streamlit_app.py --server.port=8502

# Check port usage
netstat -an | grep 8501
```

**Memory Issues:**
```bash
# Increase Docker memory limit
docker run --memory=2g -p 8501:8501 peru-tmin-app

# Use lighter dependencies
pip install streamlit pandas matplotlib
```

**Data Loading Errors:**
```bash
# Verify data files
python -c "import os; print([f for f in os.listdir('data') if f.endswith('.csv')])"

# Recreate sample data  
python create_sample_data.py
```

## 📈 Performance Optimization

### Streamlit Caching
```python
@st.cache_data
def load_data():
    # Data loading function
    pass

@st.cache_resource  
def create_map():
    # Resource-intensive operations
    pass
```

### Docker Optimization
```dockerfile
# Multi-stage build
FROM python:3.12-slim as builder
# ... build dependencies

FROM python:3.12-slim
# ... copy only necessary files
```

## 🔒 Security Considerations

### Production Deployment
- Use HTTPS (SSL certificates)
- Implement authentication if needed
- Sanitize user inputs
- Regular dependency updates
- Monitor resource usage

### Data Privacy
- Ensure no sensitive data in public repositories
- Use environment variables for credentials
- Implement proper data handling practices

## 📞 Support

For deployment issues:
1. Check logs: `docker logs container-name`
2. Verify requirements: `python test_setup.py`
3. Test locally first: `python simple_demo.py`
4. Review Streamlit docs: [docs.streamlit.io](https://docs.streamlit.io)

## 🎉 Success Metrics

Deployment is successful when:
- [x] App loads without errors
- [x] All 4 tabs display content
- [x] Data tables are downloadable
- [x] Visualizations render correctly
- [x] Policy recommendations display
- [x] Filters work properly

**Public URL Example:** https://peru-tmin-analysis.streamlit.app