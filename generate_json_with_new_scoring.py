#!/usr/bin/env python3
"""
Generate JSON with NEW 6-Dimensional Index Scoring System
This uses the proper StandardScaler + weighted index approach
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import json
from pathlib import Path

# Read the complete hotelshift_factors.xlsx
excel_file = Path.home() / "Downloads" / "hotelshift_factors.xlsx"

print(f"📖 Reading {excel_file}...")
df = pd.read_excel(excel_file)

print(f"✅ Loaded {len(df)} records from {df['msa_code'].nunique()} unique MSAs")

# Filter for latest year only
latest_year = df["year"].max()
df = df[df["year"] == latest_year].copy()

print(f"📅 Using latest year: {latest_year}")
print(f"📊 MSAs in latest year: {len(df)}")

# ==========================================
# 1. Directional Correction (All "Higher is Better")
# ==========================================

df["Vacancy_Rate_adj"] = -df["Vacancy_Rate"]
df["Rent_to_Income_adj"] = -df["Rent_to_Income_Ratio"]

# ==========================================
# 2. Define Six Dimensional Variables
# ==========================================

economic_vars = [
    "Employment_Growth",
    "Pop_Growth",
    "Income_Growth",
    "Employment_Rate"
]

stability_vars = [
    "Rent_to_Income_adj",
    "Vacancy_Rate_adj"
]

supply_vars = [
    "Market_Tightness"
]

pricing_vars = [
    "Rent_Growth"
]

valuation_vars = [
    "Implied_Value",
    "Value_Potential"
]

capital_vars = [
    "Cap Spread",
    "Diff_Effective_Rate"
]

# ==========================================
# 3. Standardization (z-scores)
# ==========================================

scaler = StandardScaler()

all_vars = (
    economic_vars +
    stability_vars +
    supply_vars +
    pricing_vars +
    valuation_vars +
    capital_vars
)

df_scaled = df.copy()
df_scaled[all_vars] = scaler.fit_transform(df_scaled[all_vars])

# ==========================================
# 4. Create Sub-Indices
# ==========================================

df_scaled["Economic_Index"] = df_scaled[economic_vars].mean(axis=1)
df_scaled["Stability_Index"] = df_scaled[stability_vars].mean(axis=1)
df_scaled["Supply_Index"] = df_scaled[supply_vars].mean(axis=1)
df_scaled["Pricing_Index"] = df_scaled[pricing_vars].mean(axis=1)
df_scaled["Valuation_Index"] = df_scaled[valuation_vars].mean(axis=1)
df_scaled["Capital_Index"] = df_scaled[capital_vars].mean(axis=1)

# ==========================================
# 5. Weighted Total Score
# ==========================================

df_scaled["Investment_Score"] = (
    0.25 * df_scaled["Economic_Index"] +
    0.15 * df_scaled["Stability_Index"] +
    0.15 * df_scaled["Supply_Index"] +
    0.15 * df_scaled["Pricing_Index"] +
    0.20 * df_scaled["Valuation_Index"] +
    0.10 * df_scaled["Capital_Index"]
)

# ==========================================
# 6. Normalize to 0-100 scale for display
# ==========================================

min_score = df_scaled["Investment_Score"].min()
max_score = df_scaled["Investment_Score"].max()

df_scaled["Investment_Score"] = (
    (df_scaled["Investment_Score"] - min_score) / (max_score - min_score) * 100
)

# Sort by Investment Score
df_sorted = df_scaled.sort_values("Investment_Score", ascending=False)

# ==========================================
# 7. Prepare for JSON
# ==========================================

# Select columns to include
columns_to_include = [
    'msa_code', 'msa_name', 'year',
    'Employment_Rate', 'Pop_Growth', 'Income_Growth', 'Employment_Growth',
    'Rent_Growth', 'Rent_to_Income_Ratio', 'Implied_Value', 
    'Vacancy_Rate', 'Market_Tightness', 'Value_Potential',
    'Diff_Effective_Rate', 'Cap Spread', 'Average HERS Index Score',
    'Economic_Index', 'Stability_Index', 'Supply_Index', 
    'Pricing_Index', 'Valuation_Index', 'Capital_Index',
    'Investment_Score'
]

df_json = df_sorted[columns_to_include].copy()

# Convert to list of dictionaries
msas = df_json.to_dict(orient='records')

# Ensure numeric fields are proper types
for msa in msas:
    for key, value in msa.items():
        if pd.notna(value):
            if isinstance(value, (int, float, bool)):
                # Try to convert to int if it's a whole number
                if isinstance(value, float) and value == int(value):
                    msa[key] = int(value)
                else:
                    msa[key] = float(round(value, 4)) if isinstance(value, float) else value

# Create JSON structure
data = {
    "stats": {
        "year": latest_year,
        "total_msa_count": len(msas),
        "scoring_system": "6-Dimensional Index (Economic, Stability, Supply, Pricing, Valuation, Capital)"
    },
    "msas": msas
}

# Save to sample_data.json
output_file = Path("/Users/ac/Desktop/Capstone Project/Capstone-Coding/msa-investment-app/data/sample_data.json")
output_file.parent.mkdir(parents=True, exist_ok=True)

with open(output_file, 'w') as f:
    json.dump(data, f, indent=2)

print(f"\n✅ Successfully created {output_file}")
print(f"   Total MSAs: {len(msas)}")
print(f"   Year: {latest_year}")
print(f"   Scoring System: 6-Dimensional Index")
print(f"   File size: {output_file.stat().st_size / 1024:.1f} KB")

# Display top 10 for verification
print(f"\n🏆 Top 10 MSAs by NEW 6D Index Score (0-100 scale):")
for i, msa in enumerate(msas[:10], 1):
    score = msa.get('Investment_Score', 0)
    if isinstance(score, (int, float)):
        print(f"   {i}. {msa['msa_name']}: {score:.2f}")
    else:
        print(f"   {i}. {msa['msa_name']}: {score}")

print(f"\n📊 Score Distribution:")
scores = [m.get('Investment_Score', 0) for m in msas if isinstance(m.get('Investment_Score'), (int, float))]
if scores:
    print(f"   Min: {min(scores):.2f}, Max: {max(scores):.2f}, Mean: {np.mean(scores):.2f}")
