#!/usr/bin/env python3
"""
Fix the sample data by preserving the correct 0-1 normalized indices
instead of raw z-scores
"""

import json
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

print("=" * 80)
print("FIXING SCORING SYSTEM")
print("=" * 80)

# Load current data
with open('data/sample_data.json', 'r') as f:
    data = json.load(f)

# Extract all index values to normalize them to 0-1 scale
economic_values = np.array([msa.get('Economic_Index', 0) for msa in data['msas']]).reshape(-1, 1)
stability_values = np.array([msa.get('Stability_Index', 0) for msa in data['msas']]).reshape(-1, 1)
supply_values = np.array([msa.get('Supply_Index', 0) for msa in data['msas']]).reshape(-1, 1)
pricing_values = np.array([msa.get('Pricing_Index', 0) for msa in data['msas']]).reshape(-1, 1)
valuation_values = np.array([msa.get('Valuation_Index', 0) for msa in data['msas']]).reshape(-1, 1)
capital_values = np.array([msa.get('Capital_Index', 0) for msa in data['msas']]).reshape(-1, 1)

# Normalize each to 0-1 range
scaler = MinMaxScaler(feature_range=(0, 1))

economic_norm = scaler.fit_transform(economic_values).flatten()
stability_norm = scaler.fit_transform(stability_values).flatten()
supply_norm = scaler.fit_transform(supply_values).flatten()
pricing_norm = scaler.fit_transform(pricing_values).flatten()
valuation_norm = scaler.fit_transform(valuation_values).flatten()
capital_norm = scaler.fit_transform(capital_values).flatten()

# Replace the index values with normalized versions
for i, msa in enumerate(data['msas']):
    msa['Economic_Index'] = round(economic_norm[i], 4)
    msa['Stability_Index'] = round(stability_norm[i], 4)
    msa['Supply_Index'] = round(supply_norm[i], 4)
    msa['Pricing_Index'] = round(pricing_norm[i], 4)
    msa['Valuation_Index'] = round(valuation_norm[i], 4)
    msa['Capital_Index'] = round(capital_norm[i], 4)
    
    # Recalculate Investment_Score using normalized indices
    # Since indices are now 0-1, the score will also be 0-1, then multiply by 100
    new_score = (
        msa['Economic_Index'] * 0.25 +
        msa['Stability_Index'] * 0.15 +
        msa['Supply_Index'] * 0.15 +
        msa['Pricing_Index'] * 0.15 +
        msa['Valuation_Index'] * 0.20 +
        msa['Capital_Index'] * 0.10
    ) * 100
    
    msa['Investment_Score'] = round(new_score, 2)

# Save the fixed data
with open('data/sample_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("✅ Index values normalized to 0-1 range")
print("✅ Investment_Scores recalculated")
print("\nVerification - First 5 MSAs:")

for i in range(min(5, len(data['msas']))):
    msa = data['msas'][i]
    score = (
        msa['Economic_Index'] * 0.25 +
        msa['Stability_Index'] * 0.15 +
        msa['Supply_Index'] * 0.15 +
        msa['Pricing_Index'] * 0.15 +
        msa['Valuation_Index'] * 0.20 +
        msa['Capital_Index'] * 0.10
    ) * 100
    
    print(f"\n{msa['msa_name']}:")
    print(f"  Economic (0-1):  {msa['Economic_Index']:.4f}")
    print(f"  Stability (0-1): {msa['Stability_Index']:.4f}")
    print(f"  Supply (0-1):    {msa['Supply_Index']:.4f}")
    print(f"  Pricing (0-1):   {msa['Pricing_Index']:.4f}")
    print(f"  Valuation (0-1): {msa['Valuation_Index']:.4f}")
    print(f"  Capital (0-1):   {msa['Capital_Index']:.4f}")
    print(f"  Investment Score calculated: {score:.2f}")
    print(f"  Investment Score stored:     {msa['Investment_Score']:.2f}")

print("\n✅ All data has been fixed and saved!")
print("=" * 80)
