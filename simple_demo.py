#!/usr/bin/env python3
"""
Simple demonstration of the Peru Minimum Temperature Analysis.
This script runs without external dependencies and shows the analysis results.
"""

import json
import csv
from pathlib import Path

def load_analysis_data():
    """Load the analysis data from CSV file."""
    data_path = Path(__file__).parent / 'data' / 'peru_tmin_analysis.csv'
    
    if not data_path.exists():
        print("❌ Analysis data not found. Run create_sample_data.py first.")
        return None
    
    data = []
    with open(data_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert numeric columns
            for key in ['count', 'min', 'max', 'mean', 'std', 'percentile_10', 
                       'percentile_90', 'percentile_25', 'percentile_75', 'range',
                       'frost_risk', 'extreme_cold']:
                row[key] = float(row[key])
            data.append(row)
    
    return data

def analyze_climate_risks(data):
    """Analyze climate risks from the data."""
    print("🧊 PERU MINIMUM TEMPERATURE ANALYSIS")
    print("=" * 50)
    
    # Basic statistics
    temps = [row['mean'] for row in data]
    min_temps = [row['min'] for row in data]
    
    print(f"\n📊 TEMPERATURE STATISTICS:")
    print(f"  • Total administrative units: {len(data)}")
    print(f"  • Mean temperature range: {min(temps):.1f}°C to {max(temps):.1f}°C")
    print(f"  • Average minimum temperature: {sum(temps)/len(temps):.1f}°C")
    print(f"  • Coldest absolute minimum: {min(min_temps):.1f}°C")
    print(f"  • Warmest absolute minimum: {max(min_temps):.1f}°C")
    
    # Risk analysis
    risk_counts = {}
    frost_areas = 0
    extreme_cold_areas = 0
    
    for row in data:
        risk = row['risk_level']
        risk_counts[risk] = risk_counts.get(risk, 0) + 1
        if row['frost_risk'] > 0:
            frost_areas += 1
        if row['extreme_cold'] > 0:
            extreme_cold_areas += 1
    
    print(f"\n❄️ CLIMATE RISK ANALYSIS:")
    print(f"  • Areas with frost risk: {frost_areas} ({frost_areas/len(data)*100:.1f}%)")
    print(f"  • Areas with extreme cold: {extreme_cold_areas} ({extreme_cold_areas/len(data)*100:.1f}%)")
    print(f"  • Risk level distribution:")
    for risk in ['Very High', 'High', 'Medium', 'Low']:
        count = risk_counts.get(risk, 0)
        print(f"    - {risk}: {count} units ({count/len(data)*100:.1f}%)")
    
    # Coldest areas (highest risk)
    coldest = sorted(data, key=lambda x: x['mean'])[:5]
    print(f"\n🥶 TOP 5 COLDEST AREAS (HIGHEST RISK):")
    for i, area in enumerate(coldest, 1):
        print(f"  {i}. {area['NAME_CLEAN']}: {area['mean']:.1f}°C "
              f"(min: {area['min']:.1f}°C, risk: {area['risk_level']})")
    
    # Warmest areas (lowest risk)  
    warmest = sorted(data, key=lambda x: x['mean'], reverse=True)[:5]
    print(f"\n🔥 TOP 5 WARMEST AREAS (LOWEST RISK):")
    for i, area in enumerate(warmest, 1):
        print(f"  {i}. {area['NAME_CLEAN']}: {area['mean']:.1f}°C "
              f"(min: {area['min']:.1f}°C, risk: {area['risk_level']})")
    
    return data

def show_policy_recommendations():
    """Display public policy recommendations."""
    print(f"\n🏛️ PUBLIC POLICY RECOMMENDATIONS")
    print("=" * 50)
    
    policies = [
        {
            "name": "Thermal Housing Improvement (ISUR)",
            "target": "500,000 households in high-risk areas",
            "cost": "S/ 1.25 billion",
            "objective": "Reduce respiratory illnesses by 30%",
            "kpi": "30% reduction in ARI cases"
        },
        {
            "name": "Agricultural Anti-Frost Protection", 
            "target": "200,000 farmers in frost-prone areas",
            "cost": "S/ 600 million",
            "objective": "Reduce agricultural losses from frost",
            "kpi": "40% reduction in crop losses"
        },
        {
            "name": "Educational Continuity Program",
            "target": "300,000 students in 5,000 schools",
            "cost": "S/ 250 million", 
            "objective": "Maintain school attendance during cold periods",
            "kpi": "20% improvement in attendance"
        }
    ]
    
    for i, policy in enumerate(policies, 1):
        print(f"\n{i}. {policy['name']}")
        print(f"   Target: {policy['target']}")
        print(f"   Investment: {policy['cost']}")
        print(f"   Objective: {policy['objective']}")
        print(f"   KPI: {policy['kpi']}")
    
    print(f"\n💰 TOTAL INVESTMENT: S/ 2.1 billion over 5 years")
    print(f"📍 PRIORITY REGIONS: Puno, Cusco, Ayacucho, Huancavelica (high-Andean)")
    print(f"🎯 FUNDING: World Bank, Government budget, UN Green Climate Fund")

def main():
    """Run the demonstration."""
    data = load_analysis_data()
    if data is None:
        return 1
    
    analyze_climate_risks(data)
    show_policy_recommendations()
    
    print(f"\n" + "=" * 50)
    print("🎉 ANALYSIS COMPLETE!")
    print("\nFor interactive visualization, run:")
    print("  streamlit run app/streamlit_app.py")
    print("\nFor detailed analysis, see:")
    print("  notebooks/peru_tmin_analysis.ipynb")
    
    return 0

if __name__ == "__main__":
    exit(main())