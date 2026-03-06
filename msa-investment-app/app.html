#!/usr/bin/env python3
"""
MSA Investment Ranking Web Application
Automated interactive dashboard for US Census data analysis and MSA investment potential ranking
"""

from flask import Flask, render_template, jsonify, request
import json
import os
from pathlib import Path
try:
    from ai_helper import get_assistant
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

app = Flask(__name__)

# Initialize AI assistant if available
ai_assistant = None
if AI_AVAILABLE:
    try:
        ai_assistant = get_assistant()
    except Exception as e:
        print(f"Warning: Could not initialize AI assistant: {e}")
        AI_AVAILABLE = False

# Load sample data
DATA_PATH = Path(__file__).parent / 'data' / 'sample_data.json'

def load_msa_data():
    """Load MSA data from JSON file"""
    if DATA_PATH.exists():
        with open(DATA_PATH, 'r') as f:
            return json.load(f)
    return {"msas": [], "stats": {}}

@app.route('/')
def index():
    """Serve the main dashboard"""
    return render_template('index.html')

@app.route('/api/msa-rankings')
def get_rankings():
    """Get MSA rankings sorted by investment score"""
    data = load_msa_data()
    msas = sorted(data.get('msas', []), key=lambda x: x.get('Investment_Score', 0), reverse=True)
    return jsonify({
        'msas': msas,
        'total': len(msas),
        'stats': data.get('stats', {})
    })

@app.route('/api/msa/<int:msa_code>')
def get_msa_detail(msa_code):
    """Get detailed data for a specific MSA"""
    data = load_msa_data()
    msa = next((m for m in data.get('msas', []) if m['msa_code'] == msa_code), None)
    if msa:
        return jsonify(msa)
    return jsonify({'error': 'MSA not found'}), 404

@app.route('/api/top-10')
def get_top_10():
    """Get top 10 MSAs"""
    data = load_msa_data()
    msas = sorted(data.get('msas', []), key=lambda x: x.get('Investment_Score', 0), reverse=True)[:10]
    return jsonify({'msas': msas})

@app.route('/api/search')
def search_msa():
    """Search for MSA by name or code"""
    query = request.args.get('q', '').lower()
    data = load_msa_data()
    results = [m for m in data.get('msas', []) 
               if query in m['msa_name'].lower() or str(m['msa_code']) == query]
    return jsonify({'results': results[:5]})

@app.route('/api/stats')
def get_stats():
    """Get overall statistics"""
    data = load_msa_data()
    msas = data.get('msas', [])
    
    if not msas:
        return jsonify({'error': 'No data available'}), 404
    
    scores = [m.get('Investment_Score', 0) for m in msas]
    
    stats = {
        'total_msas': len(msas),
        'avg_score': round(sum(scores) / len(scores), 2),
        'max_score': round(max(scores), 2),
        'min_score': round(min(scores), 2),
        'latest_year': data.get('stats', {}).get('year', 2024)
    }
    return jsonify(stats)

@app.route('/api/indices-comparison')
def indices_comparison():
    """Get comparison data for 6 dimensions"""
    data = load_msa_data()
    top_5 = sorted(data.get('msas', []), key=lambda x: x.get('Investment_Score', 0), reverse=True)[:5]
    
    categories = [
        'Economic_Index', 'Stability_Index', 'Supply_Index',
        'Pricing_Index', 'Valuation_Index', 'Capital_Index'
    ]
    
    return jsonify({
        'msas': [{'name': m['msa_name'], 'code': m['msa_code']} for m in top_5],
        'data': [
            {
                'msa_name': m['msa_name'],
                'indices': {cat: m.get(cat, 0) for cat in categories}
            } for m in top_5
        ],
        'categories': categories
    })

@app.route('/api/factors')
def get_factors():
    """Get description of all factors collected"""
    factors = {
        'demographic': {
            'Total_Population': 'MSA resident count',
            'Pop_Growth': 'Year-over-year population change (%)',
            'Employment_Rate': '% of labor force employed',
            'Median_Household_Income': 'Average annual income ($)',
            'Income_Growth': 'Year-over-year income change (%)'
        },
        'real_estate': {
            'Median_Gross_Rent': 'Average monthly rent ($)',
            'Median_House_Value': 'Average property value ($)',
            'Rent_to_Income_Ratio': 'Monthly rent / monthly income (%)',
            'Vacancy_Rate': 'Empty units as % of total',
            'Implied_Value': 'Annual rent × cap rate'
        },
        'investment': {
            'Cap Spread': 'Hotel Cap Rate - Multifamily Cap Rate (%)',
            'Diff_Effective_Rate': 'Hotel tax rate - Multifamily tax rate (%)',
            'Average HERS Index Score': 'Energy efficiency (lower = more efficient)'
        },
        'indices': {
            'Economic_Index': 'Growth metrics composite',
            'Stability_Index': 'Affordability & stability composite',
            'Supply_Index': 'Market tightness composite',
            'Pricing_Index': 'Rent growth composite',
            'Valuation_Index': 'Property value potential composite',
            'Capital_Index': 'Cap rates & taxes composite'
        }
    }
    return jsonify(factors)

@app.route('/api/factor-descriptions')
def get_factor_descriptions():
    """Get detailed descriptions of calculation methodology"""
    descriptions = {
        'Investment_Score': 'Composite score based on weighted combination of 6 indices',
        'Economic_Index': 'Average of: Employment Growth, Population Growth, Income Growth, Employment Rate',
        'Stability_Index': 'Average of: Rent-to-Income Ratio (negated), Vacancy Rate (negated)',
        'Supply_Index': 'Market Tightness = 1 - (Vacant Units / Total Units)',
        'Pricing_Index': 'Rent Growth = Year-over-year change in median rent',
        'Valuation_Index': 'Average of: Implied Value, Value Potential (1/Rent-to-Income)',
        'Capital_Index': 'Average of: Cap Rate Spread, Tax Rate Differential'
    }
    return jsonify(descriptions)

@app.route('/api/ai-chat', methods=['POST'])
def ai_chat():
    """Handle AI chat with web search"""
    if not AI_AVAILABLE or ai_assistant is None:
        return jsonify({'error': 'AI not available', 'response': 'AI assistant is not initialized'}), 503
    
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Process through AI assistant
        result = ai_assistant.process_query(message)
        
        return jsonify({
            'response': result.get('response', ''),
            'source': result.get('source', 'unknown'),
            'search_results': result.get('search_results', []),
            'msa_results': result.get('msa_results', [])
        })
    
    except Exception as e:
        return jsonify({'error': str(e), 'response': 'Sorry, there was an error'}), 500

@app.route('/api/ai-status')
def ai_status():
    """Check AI assistant status"""
    if not AI_AVAILABLE or ai_assistant is None:
        return jsonify({'available': False, 'message': 'AI assistant not initialized'})
    
    return jsonify({
        'available': True,
        'ollama_available': ai_assistant.ollama_available,
        'message': 'AI assistant ready'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    if AI_AVAILABLE:
        print(f"\n✨ MSA Investment Analyzer with AI Assistant")
        print(f"🤖 AI features: {'✅ Enabled' if ai_assistant else '⚠️ Disabled'}")
    else:
        print(f"\n✨ MSA Investment Analyzer")
    print(f"🌐 Open browser: http://localhost:{port}")
    print(f"🔧 Press Ctrl+C to stop\n")
    app.run(debug=False, use_reloader=False, port=port)
