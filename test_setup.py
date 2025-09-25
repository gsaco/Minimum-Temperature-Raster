#!/usr/bin/env python3
"""
Test script to verify the project setup and basic functionality.
This script can run without external dependencies to validate the basic structure.
"""

import os
import sys
from pathlib import Path

def test_project_structure():
    """Test that all required directories and files exist."""
    print("🔍 Testing project structure...")
    
    base_path = Path(__file__).parent
    required_dirs = ['app', 'data', 'notebooks']
    required_files = ['tmin_raster.tif', 'requirements.txt', 'README.md']
    
    # Check directories
    for dir_name in required_dirs:
        dir_path = base_path / dir_name
        if dir_path.exists():
            print(f"  ✅ Directory '{dir_name}' exists")
        else:
            print(f"  ❌ Directory '{dir_name}' missing")
            return False
    
    # Check files
    for file_name in required_files:
        file_path = base_path / file_name
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"  ✅ File '{file_name}' exists ({size} bytes)")
        else:
            print(f"  ❌ File '{file_name}' missing")
            return False
    
    return True

def test_raster_file():
    """Test basic raster file properties."""
    print("\n🗺️ Testing raster file...")
    
    raster_path = Path(__file__).parent / 'tmin_raster.tif'
    
    if not raster_path.exists():
        print("  ❌ Raster file not found")
        return False
    
    size = raster_path.stat().st_size
    print(f"  ✅ Raster file size: {size:,} bytes ({size/1024/1024:.2f} MB)")
    
    # Basic file validation (GeoTIFF should start with specific bytes)
    with open(raster_path, 'rb') as f:
        header = f.read(4)
        if header[:2] in [b'II', b'MM']:  # TIFF format indicators
            print("  ✅ File appears to be a valid TIFF format")
            return True
        else:
            print("  ⚠️ File may not be a valid TIFF format")
            return False

def test_app_files():
    """Test that application files exist and are readable."""
    print("\n📱 Testing application files...")
    
    base_path = Path(__file__).parent
    app_files = {
        'app/streamlit_app.py': 'Streamlit application',
        'data/download_boundaries.py': 'Boundary download script',
        'notebooks/peru_tmin_analysis.ipynb': 'Analysis notebook'
    }
    
    for file_path, description in app_files.items():
        full_path = base_path / file_path
        if full_path.exists():
            size = full_path.stat().st_size
            print(f"  ✅ {description}: {size:,} bytes")
        else:
            print(f"  ❌ {description}: not found")
            return False
    
    return True

def test_requirements():
    """Test requirements file content."""
    print("\n📦 Testing requirements...")
    
    req_path = Path(__file__).parent / 'requirements.txt'
    
    try:
        with open(req_path, 'r') as f:
            requirements = f.read().strip().split('\n')
        
        required_packages = [
            'numpy', 'pandas', 'matplotlib', 'streamlit', 
            'geopandas', 'rasterio', 'rasterstats'
        ]
        
        for package in required_packages:
            if any(package in req for req in requirements):
                print(f"  ✅ {package} found in requirements")
            else:
                print(f"  ⚠️ {package} not found in requirements")
        
        return True
    
    except Exception as e:
        print(f"  ❌ Error reading requirements: {e}")
        return False

def main():
    """Run all tests."""
    print("🧊 Peru Minimum Temperature Raster Analysis - Setup Test")
    print("=" * 60)
    
    tests = [
        test_project_structure,
        test_raster_file,
        test_app_files,
        test_requirements
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"  ❌ Test failed with error: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Project setup is complete.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run analysis notebook: jupyter notebook notebooks/peru_tmin_analysis.ipynb")
        print("3. Launch Streamlit app: streamlit run app/streamlit_app.py")
        return 0
    else:
        print("❌ Some tests failed. Please check the project setup.")
        return 1

if __name__ == "__main__":
    sys.exit(main())