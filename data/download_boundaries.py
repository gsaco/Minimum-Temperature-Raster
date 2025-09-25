#!/usr/bin/env python3
"""
Download Peru administrative boundaries from natural earth or other sources.
This script downloads district-level boundaries for Peru for zonal statistics analysis.
"""

import os
import requests
import zipfile
import geopandas as gpd
from pathlib import Path

def download_file(url, local_filename):
    """Download a file from URL to local path."""
    print(f"Downloading {url}...")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"Downloaded to {local_filename}")
    return local_filename

def extract_zip(zip_path, extract_to):
    """Extract ZIP file to directory."""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Extracted {zip_path} to {extract_to}")

def download_peru_boundaries():
    """Download Peru administrative boundaries."""
    data_dir = Path(__file__).parent
    data_dir.mkdir(exist_ok=True)
    
    # Download from Natural Earth - Admin 1 (Departments/Regions) - Fixed URL
    ne_admin1_url = "https://www.naturalearthdata.com/http/www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_1_states_provinces.zip"
    # Alternative URLs in case the primary fails
    alt_urls = [
        "https://naciscdn.org/naturalearth/10m/cultural/ne_10m_admin_1_states_provinces.zip",
        "https://github.com/nvkelso/natural-earth-vector/raw/master/10m_cultural/ne_10m_admin_1_states_provinces.zip"
    ]
    
    admin1_zip = data_dir / "ne_admin1.zip"
    
    if not admin1_zip.exists():
        # Try multiple URLs until one works
        success = False
        for url in [ne_admin1_url] + alt_urls:
            try:
                download_file(url, admin1_zip)
                success = True
                break
            except Exception as e:
                print(f"Failed to download from {url}: {e}")
                continue
        
        if not success:
            print("Could not download from any source. Trying GADM as fallback...")
        else:
            extract_zip(admin1_zip, data_dir / "ne_admin1")
    
    # Load and filter for Peru
    admin1_path = data_dir / "ne_admin1" / "ne_10m_admin_1_states_provinces.shp"
    if admin1_path.exists():
        gdf = gpd.read_file(admin1_path)
        peru_admin1 = gdf[gdf['admin'] == 'Peru'].copy()
        
        # Clean column names - remove diacritics and uppercase
        peru_admin1['NAME_CLEAN'] = peru_admin1['name'].str.upper().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('ascii')
        
        # Save Peru departments
        peru_admin1.to_file(data_dir / "peru_departments.geojson", driver="GeoJSON")
        print("Saved Peru departments to peru_departments.geojson")
    
    # Try to get district-level data from GADM (if available)
    gadm_url = "https://geodata.ucdavis.edu/gadm/gadm4.1/gpkg/gadm41_PER.gpkg"
    gadm_file = data_dir / "gadm41_PER.gpkg"
    
    try:
        if not gadm_file.exists():
            download_file(gadm_url, gadm_file)
        
        # Load districts (level 2)
        districts = gpd.read_file(gadm_file, layer='ADM_ADM_2')
        
        # Clean names
        districts['NAME_CLEAN'] = districts['NAME_2'].str.upper().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('ascii')
        districts['DEPT_CLEAN'] = districts['NAME_1'].str.upper().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('ascii')
        
        # Save districts
        districts.to_file(data_dir / "peru_districts.geojson", driver="GeoJSON")
        print("Saved Peru districts to peru_districts.geojson")
        
    except Exception as e:
        print(f"Could not download district data: {e}")
        print("Will use department-level data instead")

if __name__ == "__main__":
    download_peru_boundaries()