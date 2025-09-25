#!/usr/bin/env python3
"""
Create sample analysis data for demonstration purposes.
This script creates mock data that represents the expected output structure
of the full analysis, allowing the Streamlit app to be demonstrated.
"""

import json
import csv
from pathlib import Path
import random

def create_sample_geojson():
    """Create a sample GeoJSON with mock Peru administrative data."""
    
    # Sample Peru departments with approximate locations and mock temperature data
    departments = [
        {"name": "LIMA", "lat": -12.0464, "lon": -77.0428, "temp_bias": 5},
        {"name": "CUSCO", "lat": -13.5319, "lon": -71.9675, "temp_bias": -3},
        {"name": "PUNO", "lat": -15.8402, "lon": -70.0219, "temp_bias": -8},
        {"name": "AREQUIPA", "lat": -16.4090, "lon": -71.5375, "temp_bias": 2},
        {"name": "AYACUCHO", "lat": -13.1586, "lon": -74.2239, "temp_bias": -2},
        {"name": "HUANCAVELICA", "lat": -12.7876, "lon": -74.9760, "temp_bias": -5},
        {"name": "ANCASH", "lat": -9.5270, "lon": -77.5279, "temp_bias": -1},
        {"name": "JUNIN", "lat": -11.1607, "lon": -75.9910, "temp_bias": 0},
        {"name": "LA LIBERTAD", "lat": -8.1090, "lon": -79.0215, "temp_bias": 8},
        {"name": "PIURA", "lat": -5.1945, "lon": -80.6328, "temp_bias": 12},
        {"name": "LAMBAYEQUE", "lat": -6.7011, "lon": -79.9061, "temp_bias": 10},
        {"name": "CAJAMARCA", "lat": -7.1618, "lon": -78.5126, "temp_bias": 4},
        {"name": "LORETO", "lat": -3.7437, "lon": -73.2516, "temp_bias": 15},
        {"name": "UCAYALI", "lat": -8.3791, "lon": -74.5539, "temp_bias": 12},
        {"name": "MADRE DE DIOS", "lat": -12.5934, "lon": -69.1892, "temp_bias": 10},
        {"name": "AMAZONAS", "lat": -6.2305, "lon": -77.8734, "temp_bias": 6},
        {"name": "SAN MARTIN", "lat": -6.4822, "lon": -76.3647, "temp_bias": 8},
        {"name": "HUANUCO", "lat": -9.9306, "lon": -76.2422, "temp_bias": 3},
        {"name": "PASCO", "lat": -10.6928, "lon": -76.2561, "temp_bias": -4},
        {"name": "ICA", "lat": -14.0679, "lon": -75.7286, "temp_bias": 6},
        {"name": "MOQUEGUA", "lat": -17.1934, "lon": -70.9357, "temp_bias": 3},
        {"name": "TACNA", "lat": -18.0146, "lon": -70.2533, "temp_bias": 4},
        {"name": "TUMBES", "lat": -3.5736, "lon": -80.4516, "temp_bias": 14},
        {"name": "APURIMAC", "lat": -13.6340, "lon": -72.8814, "temp_bias": -1},
        {"name": "CALLAO", "lat": -12.0566, "lon": -77.1181, "temp_bias": 7}
    ]
    
    features = []
    
    for i, dept in enumerate(departments):
        # Generate mock temperature statistics
        base_temp = dept["temp_bias"]
        mean_temp = base_temp + random.uniform(-2, 2)
        min_temp = mean_temp - random.uniform(5, 15)
        max_temp = mean_temp + random.uniform(5, 10)
        std_temp = random.uniform(2, 8)
        
        # Create risk classification
        if mean_temp < -2:
            risk_level = "Very High"
        elif mean_temp < 0:
            risk_level = "High"
        elif mean_temp < 5:
            risk_level = "Medium"
        else:
            risk_level = "Low"
        
        # Create a simple square geometry around the coordinates
        lat, lon = dept["lat"], dept["lon"]
        coords = [[
            [lon - 0.5, lat - 0.5],
            [lon + 0.5, lat - 0.5],
            [lon + 0.5, lat + 0.5],
            [lon - 0.5, lat + 0.5],
            [lon - 0.5, lat - 0.5]
        ]]
        
        feature = {
            "type": "Feature",
            "properties": {
                "NAME_CLEAN": dept["name"],
                "count": random.randint(1000, 5000),
                "min": round(min_temp, 2),
                "max": round(max_temp, 2),
                "mean": round(mean_temp, 2),
                "std": round(std_temp, 2),
                "percentile_10": round(min_temp + 1, 2),
                "percentile_90": round(max_temp - 1, 2),
                "percentile_25": round(mean_temp - 2, 2),
                "percentile_75": round(mean_temp + 2, 2),
                "range": round(max_temp - min_temp, 2),
                "frost_risk": 1 if min_temp < 0 else 0,
                "extreme_cold": 1 if (min_temp + 1) < -5 else 0,
                "risk_level": risk_level
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": coords
            }
        }
        features.append(feature)
    
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    
    return geojson

def create_sample_csv(geojson_data):
    """Create CSV data from GeoJSON (without geometry)."""
    csv_data = []
    
    for feature in geojson_data["features"]:
        row = feature["properties"].copy()
        csv_data.append(row)
    
    return csv_data

def main():
    """Create sample data files."""
    data_dir = Path(__file__).parent / 'data'
    data_dir.mkdir(exist_ok=True)
    
    print("🔧 Creating sample analysis data...")
    
    # Create GeoJSON data
    geojson_data = create_sample_geojson()
    
    # Save GeoJSON
    geojson_path = data_dir / 'peru_tmin_analysis.geojson'
    with open(geojson_path, 'w') as f:
        json.dump(geojson_data, f, indent=2)
    print(f"  ✅ Created {geojson_path} ({len(geojson_data['features'])} features)")
    
    # Create and save CSV
    csv_data = create_sample_csv(geojson_data)
    csv_path = data_dir / 'peru_tmin_analysis.csv'
    
    if csv_data:
        fieldnames = csv_data[0].keys()
        with open(csv_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_data)
        print(f"  ✅ Created {csv_path} ({len(csv_data)} rows)")
    
    # Create a simple map placeholder
    map_path = data_dir / 'peru_tmin_map.png'
    map_placeholder = """
    This is a placeholder for the Peru minimum temperature map.
    In the full analysis, this would be generated by the notebook
    using GeoPandas and Matplotlib to create a choropleth map.
    """
    
    with open(map_path.with_suffix('.txt'), 'w') as f:
        f.write(map_placeholder.strip())
    print(f"  ✅ Created map placeholder at {map_path.with_suffix('.txt')}")
    
    print("\n📊 Sample data summary:")
    
    # Calculate some summary statistics
    temps = [f["properties"]["mean"] for f in geojson_data["features"]]
    risk_counts = {}
    for f in geojson_data["features"]:
        risk = f["properties"]["risk_level"]
        risk_counts[risk] = risk_counts.get(risk, 0) + 1
    
    print(f"  • Total administrative units: {len(geojson_data['features'])}")
    print(f"  • Temperature range: {min(temps):.1f}°C to {max(temps):.1f}°C")
    print(f"  • Average temperature: {sum(temps)/len(temps):.1f}°C")
    print("  • Risk distribution:")
    for risk, count in sorted(risk_counts.items()):
        print(f"    - {risk}: {count} units")
    
    print(f"\n🎯 Sample data created successfully!")
    print("You can now run the Streamlit app to see the interface:")
    print("  streamlit run app/streamlit_app.py")

if __name__ == "__main__":
    main()