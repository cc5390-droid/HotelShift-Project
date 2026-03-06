import json

# Load the data
with open('data/sample_data.json', 'r') as f:
    data = json.load(f)

# Recalculate Investment_Score using consistent formula
# Formula: (Economic×0.25 + Stability×0.15 + Supply×0.15 + Pricing×0.15 + Valuation×0.20 + Capital×0.10) × 100

print("Recalculating Investment_Scores...\n")

for msa in data['msas']:
    economic = msa.get('Economic_Index', 0)
    stability = msa.get('Stability_Index', 0)
    supply = msa.get('Supply_Index', 0)
    pricing = msa.get('Pricing_Index', 0)
    valuation = msa.get('Valuation_Index', 0)
    capital = msa.get('Capital_Index', 0)
    
    # Calculate consistent score
    new_score = (
        economic * 0.25 +
        stability * 0.15 +
        supply * 0.15 +
        pricing * 0.15 +
        valuation * 0.20 +
        capital * 0.10
    ) * 100
    
    old_score = msa.get('Investment_Score', 0)
    msa['Investment_Score'] = round(new_score, 2)
    
    print(f"{msa['msa_name']}: {old_score} → {msa['Investment_Score']}")

# Save back
with open('data/sample_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("\n✅ All Investment_Scores recalculated consistently!\n")
