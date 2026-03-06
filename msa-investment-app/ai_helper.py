"""
AI Assistant for MSA Investment Analysis
Combines local LLM (Ollama) with web search and vector-based MSA database queries
"""

import json
import os
from pathlib import Path
import requests
from urllib.parse import quote
import logging
from typing import Dict, List, Tuple, Optional

# Vector search imports
try:
    from sentence_transformers import SentenceTransformer
    VECTOR_SEARCH_AVAILABLE = True
except ImportError:
    VECTOR_SEARCH_AVAILABLE = False
    logging.warning("sentence-transformers not installed. Vector search will be disabled.")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIAssistant:
    """Main AI Assistant class"""
    
    def __init__(self, ollama_url: str = "http://localhost:11434"):
        """
        Initialize AI Assistant
        
        Args:
            ollama_url: URL to Ollama server (ensure it's running)
        """
        self.ollama_url = ollama_url
        self.model = "mistral"  # Default lightweight model
        self.msa_data = self._load_msa_data()
        self.vector_model = None
        self.msa_embeddings = None
        
        # Initialize vector search if available
        if VECTOR_SEARCH_AVAILABLE:
            self._init_vector_search()
        
        # Check Ollama availability
        self.ollama_available = self._check_ollama()
    
    def _load_msa_data(self) -> Dict:
        """Load MSA data from JSON"""
        data_path = Path(__file__).parent / 'data' / 'sample_data.json'
        try:
            with open(data_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Data file not found: {data_path}")
            return {"msas": [], "stats": {}}
    
    def _init_vector_search(self):
        """Initialize sentence transformer for vector search"""
        try:
            self.vector_model = SentenceTransformer('all-MiniLM-L6-v2')
            # Create embeddings for all MSA names and key info
            self._generate_msa_embeddings()
            logger.info("Vector search initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize vector search: {e}")
            self.vector_model = None
    
    def _generate_msa_embeddings(self):
        """Generate embeddings for MSA data"""
        if not self.vector_model:
            return
        
        try:
            msas = self.msa_data.get('msas', [])
            msa_texts = [
                f"{msa.get('msa_name')} MSA code {msa.get('msa_code')} "
                f"with score {msa.get('Investment_Score')} "
                f"population {msa.get('Total_Population', 0)}"
                for msa in msas
            ]
            self.msa_embeddings = self.vector_model.encode(msa_texts)
        except Exception as e:
            logger.warning(f"Failed to generate MSA embeddings: {e}")
    
    def _check_ollama(self) -> bool:
        """Check if Ollama server is running"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            logger.warning("Ollama server not accessible. Some features will be limited.")
            return False
    
    def _classify_query(self, query: str) -> str:
        """
        Classify query to determine if web search is needed
        Returns: 'web_search', 'msa_query', or 'general'
        """
        query_lower = query.lower()
        
        # Keywords that suggest web search needed
        web_search_keywords = [
            'news', 'recent', 'latest', 'current', 'today', 'happening',
            'industry', 'market', 'trend', 'report', 'article', 'research',
            'how', 'explain', 'tell me'
        ]
        
        # Check for web search keywords
        if any(keyword in query_lower for keyword in web_search_keywords):
            if any(city in query_lower for city in ['austin', 'denver', 'seattle', 'san francisco', 'new york']):
                return 'web_search'
        
        # Check for MSA-specific queries
        msa_keywords = ['msa', 'score', 'ranking', 'investment', 'population', 'index']
        if any(keyword in query_lower for keyword in msa_keywords):
            return 'msa_query'
        
        # Check if query mentions any MSA name
        msa_names = [m['msa_name'] for m in self.msa_data.get('msas', [])]
        if any(msa_name.lower() in query_lower for msa_name in msa_names):
            return 'msa_query'
        
        return 'general'
    
    def search_msa_database(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Search MSA database using vector similarity (if available)
        Falls back to name matching if vector search unavailable
        """
        if not self.vector_model or self.msa_embeddings is None:
            # Fallback: simple name matching
            return self._search_msa_simple(query)
        
        try:
            query_embedding = self.vector_model.encode(query)
            
            # Calculate cosine similarity manually (no sklearn needed)
            similarities = self._cosine_similarity(query_embedding, self.msa_embeddings)
            
            # Get top K results
            top_indices = sorted(range(len(similarities)), key=lambda i: similarities[i], reverse=True)[:top_k]
            results = []
            for idx in top_indices:
                if idx < len(self.msa_data['msas']):
                    msa = self.msa_data['msas'][idx]
                    results.append({
                        'name': msa.get('msa_name'),
                        'code': msa.get('msa_code'),
                        'score': msa.get('Investment_Score'),
                        'population': msa.get('Total_Population'),
                        'similarity': float(similarities[idx])
                    })
            return results
        except Exception as e:
            logger.warning(f"Vector search failed: {e}. Using fallback.")
            return self._search_msa_simple(query)
    
    @staticmethod
    def _cosine_similarity(query_vec, doc_vecs):
        """Calculate cosine similarity between query and document vectors"""
        import numpy as np
        
        # Normalize query vector
        query_norm = np.linalg.norm(query_vec)
        if query_norm == 0:
            return [0] * len(doc_vecs)
        
        query_normalized = query_vec / query_norm
        
        # Calculate similarity for each document
        similarities = []
        for doc_vec in doc_vecs:
            doc_norm = np.linalg.norm(doc_vec)
            if doc_norm == 0:
                similarities.append(0)
            else:
                doc_normalized = doc_vec / doc_norm
                sim = np.dot(query_normalized, doc_normalized)
                similarities.append(float(sim))
        
        return similarities
    
    def _search_msa_simple(self, query: str) -> List[Dict]:
        """Simple name-based MSA search"""
        query_lower = query.lower()
        results = []
        
        for msa in self.msa_data.get('msas', []):
            name = msa.get('msa_name', '').lower()
            code = str(msa.get('msa_code', ''))
            
            if query_lower in name or query_lower == code:
                results.append({
                    'name': msa.get('msa_name'),
                    'code': msa.get('msa_code'),
                    'score': msa.get('Investment_Score'),
                    'population': msa.get('Total_Population')
                })
        
        return results[:5]
    
    def process_query(self, user_query: str, include_web_search: bool = True) -> Dict:
        """
        Process user query and return response
        
        Returns:
            {
                'response': str,
                'source': str ('ollama', 'web', 'msa_db'),
                'search_results': list,
                'msa_results': list
            }
        """
        result = {
            'response': '',
            'source': 'unknown',
            'search_results': [],
            'msa_results': []
        }
        
        # Classify the query
        query_type = self._classify_query(user_query)
        
        # Handle MSA queries
        if query_type == 'msa_query':
            msa_results = self.search_msa_database(user_query)
            result['msa_results'] = msa_results
            result['source'] = 'msa_db'
            
            if msa_results:
                response_text = self._generate_response_with_msa(user_query, msa_results)
                result['response'] = response_text
            else:
                result['response'] = f"I couldn't find specific MSA data matching '{user_query}'. Could you be more specific?"
        
        # Handle web search queries
        elif query_type == 'web_search' and include_web_search:
            search_results = search_web(user_query)
            result['search_results'] = search_results
            result['source'] = 'web'
            
            if search_results:
                response_text = self._generate_response_with_web(user_query, search_results)
                result['response'] = response_text
            else:
                result['response'] = f"I couldn't find recent news about '{user_query}'. Try rephrasing your query."
        
        # Handle general queries
        else:
            if self.ollama_available:
                result['response'] = self._query_ollama(user_query)
                result['source'] = 'ollama'
            else:
                result['response'] = self._generate_fallback_response(user_query)
                result['source'] = 'fallback'
        
        return result
    
    def _query_ollama(self, prompt: str, max_tokens: int = 500) -> str:
        """Query local Ollama LLM"""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": max_tokens,
                        "temperature": 0.7
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get('response', 'No response from model')
            else:
                return f"Error from Ollama: {response.status_code}"
        except requests.exceptions.ConnectionError:
            return "Ollama server is not running. Please start it with: ollama serve"
        except Exception as e:
            return f"Error querying Ollama: {str(e)}"
    
    def _generate_response_with_msa(self, query: str, msa_results: List[Dict]) -> str:
        """Generate response using MSA database"""
        if not msa_results:
            return "No matching MSA data found."
        
        response = f"Based on your query about {query}:\n\n"
        
        for i, msa in enumerate(msa_results[:3], 1):
            response += f"{i}. **{msa['name']}** (Code: {msa['code']})\n"
            response += f"   - Investment Score: {msa['score']}\n"
            response += f"   - Population: {msa['population']:,}\n\n"
        
        response += "Would you like more details about any of these MSAs?"
        return response
    
    def _generate_response_with_web(self, query: str, search_results: List[Dict]) -> str:
        """Generate response using web search results"""
        response = f"Here's what I found about {query}:\n\n"
        
        for i, result in enumerate(search_results[:3], 1):
            response += f"{i}. **{result['title']}**\n"
            response += f"   Summary: {result['summary']}\n"
            response += f"   📎 [Read Full Article]({result['url']})\n\n"
        
        return response
    
    def _generate_fallback_response(self, query: str) -> str:
        """Generate response when Ollama is unavailable"""
        return (
            f"I received your question: '{query}'\n\n"
            "To use the AI assistant fully, please:\n"
            "1. Install Ollama from https://ollama.ai\n"
            "2. Run: ollama serve\n"
            "3. Then refresh this page\n\n"
            "For now, you can ask about MSA data or recent news, and I'll search our database or the web."
        )


def search_web(query: str, num_results: int = 3) -> List[Dict]:
    """
    Search the web using multiple strategies
    1. Try DuckDuckGo instant answers
    2. Try to extract from search results
    
    Returns list of dicts with 'title', 'summary', 'url'
    """
    try:
        results = []
        
        # Method 1: Try DuckDuckGo JSON API
        try:
            from urllib.parse import quote
            url = f"https://api.duckduckgo.com/?q={quote(query)}&format=json"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                # Try to get results from AbstractResults
                if data.get('AbstractText'):
                    results.append({
                        'title': data.get('Heading', 'Search Result'),
                        'url': data.get('AbstractURL', '#'),
                        'summary': data.get('AbstractText', '')[:200]
                    })
                
                # Try to get related topics
                for topic in data.get('RelatedTopics', [])[:num_results]:
                    if 'Text' in topic:
                        results.append({
                            'title': topic.get('FirstURL', '').split('/')[-1],
                            'url': topic.get('FirstURL', '#'),
                            'summary': topic.get('Text', '')[:200]
                        })
            
            if results:
                return results[:num_results]
        
        except Exception as e:
            logger.debug(f"DuckDuckGo JSON API failed: {e}")
            pass
        
        # Method 2: Fallback to basic HTML scraping
        try:
            from bs4 import BeautifulSoup
            from urllib.parse import quote
            
            url = f"https://html.duckduckgo.com/?q={quote(query)}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for result divs
                search_results = soup.find_all('div', {'class': 'result'})
                
                for result in search_results[:num_results]:
                    try:
                        # Try multiple selectors for title
                        title_elem = result.find('a', {'class': 'result__a'})
                        if not title_elem:
                            title_elem = result.find('a', {'class': 'result__url'})
                        
                        if not title_elem:
                            continue
                        
                        title = title_elem.get_text().strip()
                        url_elem = title_elem
                        url = url_elem.get('href', '')
                        
                        # Get snippet
                        snippet_elem = result.find('a', {'class': 'result__snippet'})
                        if not snippet_elem:
                            snippet_elem = result.find('div', {'class': 'result__snippet'})
                        
                        summary = snippet_elem.get_text().strip() if snippet_elem else "No summary available"
                        summary = summary.replace('\n', ' ')[:200]
                        
                        if url and title:
                            results.append({
                                'title': title,
                                'url': url,
                                'summary': summary
                            })
                    except Exception as e:
                        logger.debug(f"Error parsing individual result: {e}")
                        continue
                
                if results:
                    return results[:num_results]
        
        except ImportError:
            logger.warning("beautifulsoup4 not installed. Web search partially disabled.")
        except Exception as e:
            logger.debug(f"HTML scraping failed: {e}")
        
        # Method 3: Return a helpful message
        return [{
            'title': f'Search results for "{query}"',
            'url': f'https://duckduckgo.com/?q={quote(query)}',
            'summary': 'Click the link above to search online for more information.'
        }]
    
    except Exception as e:
        logger.warning(f"Web search error: {e}")
        return []


# Initialize global assistant instance
assistant = None

def get_assistant() -> AIAssistant:
    """Get or create global assistant instance"""
    global assistant
    if assistant is None:
        assistant = AIAssistant()
    return assistant
