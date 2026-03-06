#!/usr/bin/env python3
"""
Convert complete hotelshift_factors_standardized.xlsx to JSON for web app
This includes ALL MSAs from the Census API scraping
"""

import pandas as pd
import json
from pathlib import Path

# Read the complete standardized factors Excel file
excel_file = Path.home() / "Downloads" / "hotelshift_factors_standardized.xlsx"

print(f"📖 Reading {excel_file}...")
df = pd.read_excel(excel_file)

print(f"✅ Loaded {len(df)} records from {df['msa_code'].nunique()} unique MSAs")

# Filter for latest year only (for web app display)
latest_year = df['year'].max()
df_latest = df[df['year'] == latest_year].copy()

print(f"📅 Using latest year: {latest_year}")
print(f"📊 MSAs in latest year: {len(df_latest)}")

# Sort by Investment_Score (descending)
df_latest = df_latest.sort_values('Investment_Score', ascending=False)

# Convert to list of dictionaries
msas = df_latest.to_dict(orient='records')

# Ensure numeric fields are proper types
for msa in msas:
    for key, value in msa.items():
        if pd.notna(value):
            if isinstance(value, (int, float, bool)):
                # Try to convert to int if it's a whole number
                if isinstance(value, float) and value == int(value):
                    msa[key] = int(value)
                else:
                    msa[key] = float(value) if isinstance(value, float) else value
            elif hasattr(pd, 'Timestamp') and isinstance(value, pd.Timestamp):
                msa[key] = int(value.timestamp())

# Create JSON structure
data = {
    "stats": {
        "year": latest_year,
        "total_msa_count": len(msas)
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
print(f"   File size: {output_file.stat().st_size / 1024:.1f} KB")

# Display top 5 for verification
print(f"\n🏆 Top 5 MSAs by Investment Score:")
for i, msa in enumerate(msas[:5], 1):
    print(f"   {i}. {msa['msa_name']}: {msa.get('Investment_Score', 'N/A'):.2f}")
