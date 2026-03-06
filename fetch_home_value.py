#!/usr/bin/env python3
"""
Fetch Median Home Value from US Census API for all MSAs
"""

import json
import requests

# US Census API Key
API_KEY = '722729cfa99e33f0f76a6c4385beb4a6394f1728'

# Load existing MSA data
with open('msa-investment-app/data/sample_data.json', 'r') as f:
    data = json.load(f)

print("=" * 80)
print("FETCHING MEDIAN HOME VALUE FROM US CENSUS API")
print("=" * 80)

msa_dict = {msa['msa_code']: msa for msa in data['msas']}

print(f"\nFetching data for {len(msa_dict)} MSAs...")

# B25077_001E = Median home value
base_url = "https://api.census.gov/data/2024/acs/acs1"

params = {
    "get": "NAME,B25077_001E",
    "for": "metropolitan statistical area/micropolitan statistical area:*",
    "key": API_KEY
}

try:
    response = requests.get(base_url, params=params, timeout=30)
    response.raise_for_status()
    
    data_from_api = response.json()
    print(f"✅ API Response received: {len(data_from_api)} rows\n")
    
    # Parse the response
    header = data_from_api[0]
    homevalue_index = header.index('B25077_001E')
    msa_index = header.index('metropolitan statistical area/micropolitan statistical area')
    
    homevalue_data = {}
    
    for row in data_from_api[1:]:  # Skip header
        try:
            msa_code = int(row[msa_index])
            
            # Parse home value (may be null or -666666 for not applicable)
            try:
                homevalue = int(float(row[homevalue_index])) if row[homevalue_index] and row[homevalue_index] != '-666666' else None
            except (ValueError, IndexError):
                homevalue = None
            
            if msa_code in msa_dict:
                homevalue_data[msa_code] = homevalue
        except (ValueError, IndexError):
            pass
    
    print(f"✅ Parsed Median Home Value for {sum(1 for x in homevalue_data.values() if x)} MSAs\n")
    
    # Update the data
    updated = 0
    for msa in data['msas']:
        msa_code = msa['msa_code']
        
        if msa_code in homevalue_data and homevalue_data[msa_code]:
            msa['Median_Home_Value'] = homevalue_data[msa_code]
            updated += 1
        else:
            msa['Median_Home_Value'] = 0
    
    print(f"Updated {updated} MSAs with Median Home Value")
    
    # Save updated data
    with open('msa-investment-app/data/sample_data.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\n✅ Data saved to sample_data.json\n")
    
    # Show sample
    print("=" * 80)
    print("COMPLETE DATA SAMPLE")
    print("=" * 80)
    
    # Sort by population
    sorted_by_pop = sorted(data['msas'], key=lambda x: x.get('Total_Population', 0), reverse=True)
    
    for i, msa in enumerate(sorted_by_pop[:3]):
        pop = msa.get('Total_Population', 0)
        rent = msa.get('Median_Rent', 0)
        income = msa.get('Median_Income', 0)
        homevalue = msa.get('Median_Home_Value', 0)
        
        print(f"\n{i+1}. {msa['msa_name']}")
        print(f"   Population: {pop:,}")
        print(f"   Median Rent: ${rent:,}/month")
        print(f"   Median Income: ${income:,}/year")
        print(f"   Median Home Value: ${homevalue:,}")
    
except requests.exceptions.RequestException as e:
    print(f"❌ API Error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
