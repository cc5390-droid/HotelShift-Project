#!/usr/bin/env python3
"""
Data Converter: Convert notebook Excel exports to web app JSON format
This script helps you convert your Census analysis results to the format needed by the web app.
"""

import pandas as pd
import json
import sys
from pathlib import Path

def convert_excel_to_json(excel_file, output_file=None):
    """
    Convert Excel file from notebook to JSON format for web app
    """
    
    if not Path(excel_file).exists():
        print(f"❌ Error: File '{excel_file}' not found")
        return False
    
    try:
        # Read the Excel file
        print(f"📖 Reading {excel_file}...")
        df = pd.read_excel(excel_file)
        
        print(f"✅ Loaded {len(df)} records")
        
        # Get year from data if available, otherwise use current year
        year = int(df['year'].max()) if 'year' in df.columns else 2024
        
        # Convert dataframe to list of dictionaries
        msas = df.to_dict(orient='records')
        
        # Ensure all numeric fields are proper numbers
        for msa in msas:
            for key, value in msa.items():
                if pd.notna(value):
                    if isinstance(value, (int, float)):
                        msa[key] = float(value) if '.' in str(value) else int(value)
        
        # Create JSON structure
        data = {
            "stats": {
                "year": year,
                "total_msa_count": len(msas)
            },
            "msas": msas
        }
        
        # Determine output file
        if output_file is None:
            output_file = "data/sample_data.json"
        
        # Create parent directory if needed
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        # Write JSON file
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Successfully converted to {output_file}")
        print(f"   Year: {year}")
        print(f"   MSAs: {len(msas)}")
        print(f"   Columns: {list(df.columns)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Main entry point"""
    
    if len(sys.argv) < 2:
        print("=" * 50)
        print("📊 Excel to JSON Data Converter")
        print("=" * 50)
        print("\nUsage:")
        print("  python convert_data.py <excel_file> [output_file]")
        print("\nExamples:")
        print("  python convert_data.py hotelshift_factors.xlsx")
        print("  python convert_data.py hotelshift_factors.xlsx data/my_data.json")
        print("\nSupported files from notebook:")
        print("  - hotelshift_factors.xlsx")
        print("  - hotelshift_factors_standardized.xlsx")
        print("  - MSA_Investment_ranking_2024.xlsx")
        return
    
    excel_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    convert_excel_to_json(excel_file, output_file)

if __name__ == "__main__":
    main()
