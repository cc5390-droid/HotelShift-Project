#!/usr/bin/env python3
"""
Fetch Total Population from US Census API for all MSAs in our data
"""

import json
import requests
from pathlib import Path

# US Census API Key (from notebook)
API_KEY = '722729cfa99e33f0f76a6c4385beb4a6394f1728'

# Load existing MSA data
with open('msa-investment-app/data/sample_data.json', 'r') as f:
    data = json.load(f)

print("=" * 80)
print("FETCHING TOTAL POPULATION DATA FROM US CENSUS API")
print("=" * 80)

# Get list of MSA codes
msa_codes = [str(msa['msa_code']) for msa in data['msas']]
msa_dict = {msa['msa_code']: msa for msa in data['msas']}

print(f"\nFetching data for {len(msa_codes)} MSAs...")
print("This may take a moment...\n")

# Fetch population data from Census API
# Using ACS 1-Year estimate for most recent year (2024)
base_url = "https://api.census.gov/data/2024/acs/acs1"

params = {
    "get": "NAME,B01003_001E",  # B01003_001E is Total Population
    "for": "metropolitan statistical area/micropolitan statistical area:*",
    "key": API_KEY
}

try:
    response = requests.get(base_url, params=params, timeout=30)
    response.raise_for_status()
    
    data_from_api = response.json()
    print(f"✅ API Response received: {len(data_from_api)} rows")
    
    # Parse the response
    # First row is the header: ['NAME', 'B01003_001E', 'metropolitan statistical area/micropolitan statistical area']
    header = data_from_api[0]
    population_index = header.index('B01003_001E')
    msa_index = header.index('metropolitan statistical area/micropolitan statistical area')
    name_index = 0
    
    population_data = {}
    
    for row in data_from_api[1:]:  # Skip header
        try:
            msa_code = int(row[msa_index])
            population = int(float(row[population_index]))
            msa_name = row[name_index]
            population_data[msa_code] = {
                'population': population,
                'name': msa_name
            }
        except (ValueError, IndexError):
            pass
    
    print(f"✅ Parsed {len(population_data)} MSAs from API\n")
    
    # Update the data with population information
    updated_count = 0
    missing_count = 0
    
    for msa in data['msas']:
        msa_code = msa['msa_code']
        if msa_code in population_data:
            msa['Total_Population'] = population_data[msa_code]['population']
            updated_count += 1
        else:
            msa['Total_Population'] = 0
            missing_count += 1
    
    print(f"Updated {updated_count} MSAs with population data")
    if missing_count > 0:
        print(f"⚠️  {missing_count} MSAs not found in API response")
    
    # Save updated data
    with open('msa-investment-app/data/sample_data.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\n✅ Data saved to sample_data.json\n")
    
    # Show sample
    print("=" * 80)
    print("SAMPLE DATA WITH POPULATION")
    print("=" * 80)
    for i, msa in enumerate(sorted(data['msas'], key=lambda x: x.get('Total_Population', 0), reverse=True)[:5]):
        pop = msa.get('Total_Population', 0)
        print(f"\n{i+1}. {msa['msa_name']}")
        print(f"   MSA Code: {msa['msa_code']}")
        print(f"   Total Population: {pop:,}")
        print(f"   Investment Score: {msa['Investment_Score']:.2f}")
    
except requests.exceptions.RequestException as e:
    print(f"❌ API Error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
