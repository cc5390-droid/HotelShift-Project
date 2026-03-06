#!/usr/bin/env python3
"""
Fetch Median Rent and Median Income from US Census API for all MSAs
"""

import json
import requests

# US Census API Key
API_KEY = '722729cfa99e33f0f76a6c4385beb4a6394f1728'

# Load existing MSA data
with open('msa-investment-app/data/sample_data.json', 'r') as f:
    data = json.load(f)

print("=" * 80)
print("FETCHING MEDIAN RENT & MEDIAN INCOME FROM US CENSUS API")
print("=" * 80)

# Get list of MSA codes
msa_dict = {msa['msa_code']: msa for msa in data['msas']}

print(f"\nFetching data for {len(msa_dict)} MSAs...")

# Fetch from Census API
# B25064_001E = Median gross rent
# B19013_001E = Median household income
base_url = "https://api.census.gov/data/2024/acs/acs1"

params = {
    "get": "NAME,B25064_001E,B19013_001E",
    "for": "metropolitan statistical area/micropolitan statistical area:*",
    "key": API_KEY
}

try:
    response = requests.get(base_url, params=params, timeout=30)
    response.raise_for_status()
    
    data_from_api = response.json()
    print(f"✅ API Response received: {len(data_from_api)} rows\n")
    
    # Parse the response
    # Header: ['NAME', 'B25064_001E', 'B19013_001E', 'metropolitan statistical area/micropolitan statistical area']
    header = data_from_api[0]
    print(f"Headers: {header}\n")
    
    rent_index = header.index('B25064_001E')
    income_index = header.index('B19013_001E')
    msa_index = header.index('metropolitan statistical area/micropolitan statistical area')
    
    rent_data = {}
    income_data = {}
    
    for row in data_from_api[1:]:  # Skip header
        try:
            msa_code = int(row[msa_index])
            
            # Parse rent (may be null or -666666 for not applicable)
            try:
                rent = int(float(row[rent_index])) if row[rent_index] and row[rent_index] != '-666666' else None
            except (ValueError, IndexError):
                rent = None
            
            # Parse income (may be null or -666666 for not applicable)
            try:
                income = int(float(row[income_index])) if row[income_index] and row[income_index] != '-666666' else None
            except (ValueError, IndexError):
                income = None
            
            if msa_code in msa_dict:
                rent_data[msa_code] = rent
                income_data[msa_code] = income
        except (ValueError, IndexError):
            pass
    
    print(f"✅ Parsed Median Rent for {sum(1 for x in rent_data.values() if x)} MSAs")
    print(f"✅ Parsed Median Income for {sum(1 for x in income_data.values() if x)} MSAs\n")
    
    # Update the data
    updated_rent = 0
    updated_income = 0
    
    for msa in data['msas']:
        msa_code = msa['msa_code']
        
        if msa_code in rent_data and rent_data[msa_code]:
            msa['Median_Rent'] = rent_data[msa_code]
            updated_rent += 1
        else:
            msa['Median_Rent'] = 0
        
        if msa_code in income_data and income_data[msa_code]:
            msa['Median_Income'] = income_data[msa_code]
            updated_income += 1
        else:
            msa['Median_Income'] = 0
    
    print(f"Updated {updated_rent} MSAs with Median Rent")
    print(f"Updated {updated_income} MSAs with Median Income")
    
    # Save updated data
    with open('msa-investment-app/data/sample_data.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\n✅ Data saved to sample_data.json\n")
    
    # Show sample
    print("=" * 80)
    print("SAMPLE DATA WITH MEDIAN RENT & INCOME")
    print("=" * 80)
    
    # Sort by population to show large MSAs
    sorted_by_pop = sorted(data['msas'], key=lambda x: x.get('Total_Population', 0), reverse=True)
    
    for i, msa in enumerate(sorted_by_pop[:5]):
        pop = msa.get('Total_Population', 0)
        rent = msa.get('Median_Rent', 0)
        income = msa.get('Median_Income', 0)
        rent_to_income = (rent * 12 / income * 100) if income > 0 else 0
        
        print(f"\n{i+1}. {msa['msa_name']}")
        print(f"   Population: {pop:,}")
        print(f"   Median Rent: ${rent:,}/month")
        print(f"   Median Income: ${income:,}/year")
        print(f"   Rent-to-Income: {rent_to_income:.1f}%")
    
except requests.exceptions.RequestException as e:
    print(f"❌ API Error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
