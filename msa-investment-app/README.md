# MSA Investment Ranking Web Application

A professional, interactive web dashboard for analyzing US Metropolitan Statistical Areas (MSAs) investment potential based on Census data and market analysis.

## 🎯 Features

- **Interactive Dashboard** - View investment rankings and key metrics at a glance
- **Search & Filter** - Find specific MSAs by name or code
- **🤖 AI Assistant** ⭐ NEW - Local AI powered by Ollama + web search
  - Ask questions about MSA data and get instant answers
  - Search the web for recent news (hotel industry, real estate trends, etc.)
  - Compare markets using natural language
  - Completely local & private - no external AI API calls
- **4 Interactive Views:**
  1. **Overview** - Rankings table + score distribution chart
  2. **Index Scoring** - ⭐ NEW: Interactive weight adjustment system (recalculate scores in real-time)
  3. **Detailed Analysis** - Deep dive into specific MSA metrics
  4. **6-Dimensional Analysis** - Radar charts comparing top 5 markets across 6 investment dimensions
  5. **Raw Data** - ⭐ NEW: Complete dataset with all 13 factors and metrics

- **13 Comprehensive Factors Analyzed:**
  - **Demographic:** Population, Growth, Employment Rate, Income, Income Growth
  - **Real Estate:** Rent, Home Values, Rent-to-Income Ratio, Vacancy Rate, Implied Value
  - **Investment:** Cap Rate Spread, Tax Differential, Energy Efficiency Score

- **6 Investment Dimensions:**
  - 📈 Economic Index (growth metrics)
  - 🛡️ Stability Index (affordability & stability)
  - 📦 Supply Index (market tightness)
  - 💰 Pricing Index (rent growth)
  - 📊 Valuation Index (property value potential)
  - 🏦 Capital Index (cap rates & taxes)

## 📂 Project Structure

```
msa-investment-app/
├── app.py                    # Flask backend server
├── requirements.txt          # Python dependencies
├── templates/
│   └── index.html           # Interactive dashboard HTML
├── static/
│   ├── style.css            # Professional styling
│   └── script.js            # JavaScript interactivity
└── data/
    └── sample_data.json     # Sample MSA data (replace with your data)
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- (Optional but recommended) Ollama for AI features: https://ollama.ai

### 1. Install Dependencies
```bash
cd msa-investment-app
pip install -r requirements.txt
```

### 2. Start Ollama (Optional - for full AI features)
In a **separate terminal**:
```bash
# Download a model first (one-time)
ollama pull mistral

# Start Ollama server
ollama serve
```

### 3. Run the Application
```bash
python app.py
```

The app will start on `http://localhost:5001`

### 4. Use the AI Assistant
Click the **💬 AI Assistant** button in the top-right corner to:
- Ask about MSA data: "What's the score for Austin?"
- Search news: "Tell me about Austin hotel industry news"
- Compare markets: "How does Denver compare to Seattle?"

**For detailed AI Assistant setup, see [AI_SETUP.md](AI_SETUP.md)**

## 📊 Using Your Data

The application currently uses sample data from `data/sample_data.json`. To use your actual Census data:

### Option A: Prepare Data from Your Notebook

1. Export your analysis results from the Jupyter notebook as CSV or Excel
2. Convert to JSON format matching the structure in `sample_data.json`
3. Replace the sample data file with your data

### Option B: Auto-Generate from Notebook

Create a Python script to export notebook results:

```python
import json
import pandas as pd

# Load your analysis results (modify path as needed)
df = pd.read_excel("hotelshift_factors_standardized.xlsx")

# Convert to JSON format
msa_list = df.to_dict(orient='records')

data = {
    "stats": {
        "year": 2024,
        "total_msa_count": len(msa_list)
    },
    "msas": msa_list
}

# Save to app
with open('msa-investment-app/data/sample_data.json', 'w') as f:
    json.dump(data, f, indent=2)
```

## 🎨 Customization

### Change Colors
Edit `static/style.css` - look for color values like `#667eea` and `#764ba2`

### Modify Weights
Update the weighting logic in `app.py` at the API endpoints

### Add New Visualizations
Edit `static/script.js` and add new Chart.js configurations

## 📊 View Descriptions

### Overview
- Score distribution histogram (top 15 MSAs)
- Full ranking table with key metrics (top 20 MSAs)
- Quick access to ranked data

### Index Scoring ⭐ NEW
- **Interactive weight sliders** for each of the 6 indices
- **Real-time score recalculation** as you adjust weights
- See how rankings change with different weighting strategies
- Default weights: Economic (25%) | Stability (15%) | Supply (15%) | Pricing (15%) | Valuation (20%) | Capital (10%)

### Detailed Analysis
- Deep dive into any specific MSA
- View all demographic, real estate, and investment metrics
- Compare against market averages

### 6-Dimensional Analysis
- Radar charts comparing top 5 markets
- Visualize performance across all 6 investment dimensions
- Identify market strengths and weaknesses

### Raw Data ⭐ NEW
- Complete dataset showing all 13 factors for every MSA
- Factor definitions and meanings
- Download data as CSV for analysis
- Sort by different metrics (score, population, growth, income)

## 🔧 API Endpoints

```
GET  /api/msa-rankings      - Get all MSAs sorted by score
GET  /api/top-10            - Get top 10 MSAs
GET  /api/msa/<code>        - Get details for specific MSA
GET  /api/stats             - Get overall statistics
GET  /api/search?q=<query>  - Search for MSA
GET  /api/indices-comparison - Get 6D analysis data
GET  /api/factors           - Get factor definitions
GET  /api/factor-descriptions - Get calculation methodology
```

## 📐 Index Calculation Methodology

### Raw Data Collection
All data sourced from:
- **US Census Bureau ACS1** (Annual Community Survey)
- **Market Analysis** (Cap rates, tax rates via Gemini)
- **RESNET Database** (Energy efficiency scores)

### Factor Standardization
Each factor is standardized (normalized 0-1) within its year/dataset to ensure comparable scores across different units.

### Index Calculation
```
Economic_Index = Avg(Employment_Growth, Population_Growth, Income_Growth, Employment_Rate)
Stability_Index = Avg(1 - Rent_to_Income_Ratio, 1 - Vacancy_Rate) 
Supply_Index = 1 - (House_Vacant / (House_Vacant + House_Occupied))
Pricing_Index = Rent_Growth
Valuation_Index = Avg(Implied_Value, 1/Rent_to_Income_Ratio)
Capital_Index = Avg(Cap_Spread, Tax_Differential)
```

### Investment Score
```
Investment_Score = (Economic_Index × w₁ + 
                    Stability_Index × w₂ + 
                    Supply_Index × w₃ + 
                    Pricing_Index × w₄ + 
                    Valuation_Index × w₅ + 
                    Capital_Index × w₆) × 100

Where w₁ + w₂ + w₃ + w₄ + w₅ + w₆ = 1.0
```

## 💾 Data Format

The JSON data should follow this structure:

```json
{
  "stats": {
    "year": 2024,
    "total_msa_count": 71
  },
  "msas": [
    {
      "msa_code": 12060,
      "msa_name": "Metro Area Name",
      "year": 2024,
      "Total_Population": 6144376,
      "Investment_Score": 78.5,
      "Economic_Index": 0.65,
      "Stability_Index": 0.58,
      ...
    }
  ]
```

## 🎯 Next Steps

1. **Integrate Your Data** - Replace sample data with your Census API results
2. **Update Weights** - Adjust investment score calculation weights in `app.py`
3. **Custom Branding** - Modify header, colors, and text
4. **Deploy** - Host on Heroku, AWS, or your preferred platform

## 🛠️ Troubleshooting

**Port already in use:**
```bash
python app.py --port 5001
```

**Data not showing:**
- Verify `data/sample_data.json` exists
- Check console for error messages
- Ensure JSON format matches the required structure

**Charts not rendering:**
- Clear browser cache (Ctrl+Shift+Delete)
- Check browser console for JavaScript errors
- Verify Chart.js CDN is accessible

## 📝 License

Educational use - Built for capstone project analysis

## ✨ Technologies Used

- **Backend:** Flask (Python)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Charts:** Chart.js
- **HTTP Client:** Axios
- **Data Format:** JSON

---

**Ready to use!** Start the app and explore your MSA investment data interactively. 🚀
