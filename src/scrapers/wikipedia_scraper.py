"""
Wikipedia article scraper
"""

import time
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Tuple, Optional

from ..utils.text_utils import clean_query_for_wiki


class WikipediaScraper:
    """Scraper for Wikipedia articles"""
    
    def __init__(self, user_agent: str = "WikipediaScraperBot/1.0"):
        """
        Initialize Wikipedia scraper.
        
        Args:
            user_agent: User agent string for requests
        """
        self.headers = {'User-Agent': user_agent}
        self.search_url = "https://en.wikipedia.org/w/api.php"
    
    def search(self, query: str, limit: int = 10) -> List[Tuple[str, str]]:
        """
        Search Wikipedia and return relevant article titles and URLs.
        Includes relevance filtering based on query terms.
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of tuples (title, url) for relevant articles
        """
        # Extract key terms for relevance checking
        key_terms = set(query.lower().split())
        
        # Increase initial limit to allow for filtering
        search_limit = min(limit * 3, 30)  # Get more results to filter from
        
        params = {
            "action": "opensearch",
            "search": query,
            "limit": search_limit,
            "format": "json"
        }
        
        try:
            response = requests.get(
                self.search_url,
                params=params,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            titles = data[1]
            urls = data[3]
            
            # Filter results for relevance
            relevant_results = []
            for title, url in zip(titles, urls):
                title_lower = title.lower()
                
                # Check if title contains any query terms
                if any(term in title_lower for term in key_terms):
                    relevant_results.append((title, url))
                    continue
                
                # For AI/tech queries, ensure results are relevant
                if any(term in query.lower() for term in ['ai', 'ia', 'artificial intelligence']):
                    tech_terms = {'technology', 'science', 'computer', 'digital', 'system', 
                                'automation', 'machine', 'algorithm', 'data'}
                    if any(term in title_lower for term in tech_terms):
                        relevant_results.append((title, url))
                        continue
                
                # Add additional context-based filtering
                if 'ecology' in query.lower() and not any(term in title_lower 
                    for term in ['ecology', 'environment', 'ecosystem', 'biological']):
                    continue
                
                if len(relevant_results) < limit:
                    relevant_results.append((title, url))
            
            return relevant_results[:limit]
        
        except requests.exceptions.RequestException as e:
            print(f"❌ Error searching Wikipedia: {e}")
            return []
    
    def scrape_article(self, url: str) -> Optional[Tuple[str, str]]:
        """
        Scrape content from a Wikipedia article.
        
        Args:
            url: Article URL
            
        Returns:
            Tuple of (title, content) or None if failed
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Get title
            title_elem = soup.find('h1', {'id': 'firstHeading'})
            if not title_elem:
                return None
            title = title_elem.text
            
            # Get main content
            content_div = soup.find('div', {'id': 'mw-content-text'})
            if not content_div:
                return title, ""
            
            # Remove unwanted elements
            for unwanted in content_div.find_all(
                ['table', 'div', 'sup', 'span'],
                {'class': ['infobox', 'navbox', 'reference', 'mw-editsection']}
            ):
                unwanted.decompose()
            
            # Extract paragraphs
            paragraphs = content_div.find_all('p')
            text = '\n\n'.join([
                p.get_text().strip() 
                for p in paragraphs 
                if p.get_text().strip()
            ])
            
            return title, text
        
        except Exception as e:
            print(f"   ❌ Error scraping article: {e}")
            return None
    
    def is_content_relevant(self, content: str, keywords: str, min_relevance: float = 0.2) -> bool:
        """
        Check if article content is relevant to search keywords.
        Uses simple term frequency analysis.
        """
        content_lower = content.lower()
        key_terms = set(keywords.lower().split())
        
        # Count occurrences of key terms
        term_counts = sum(content_lower.count(term) for term in key_terms)
        
        # Calculate rough relevance score (term frequency)
        word_count = len(content_lower.split())
        if word_count == 0:
            return False
            
        relevance = term_counts / word_count
        return relevance >= min_relevance
    
    def scrape_by_keywords(
        self,
        keywords: str,
        max_articles: int = 5
    ) -> Dict[str, any]:
        """
        Search and scrape Wikipedia articles by keywords.
        Includes relevance filtering for both titles and content.
        
        Args:
            keywords: Search keywords
            max_articles: Maximum number of articles to scrape
            
        Returns:
            Dictionary containing:
            - articles: List of article dictionaries with title, content, and url
            - is_fallback: Boolean indicating if these are general fallback results
            - message: String explaining the search result status
        """
        # Clean and enhance query
        cleaned_keywords = clean_query_for_wiki(keywords)
        print(f"🔍 Searching Wikipedia for: '{cleaned_keywords}'")
        
        # Try specific search first
        specific_query = f'"{cleaned_keywords}"'  # Exact phrase match
        results = self.search(specific_query)
        
        if not results:
            print("⚠️  No exact matches found, trying general search...")
            # Try general search as fallback
            results = self.search(cleaned_keywords)
            if not results:
                print("⚠️  No Wikipedia articles found at all")
                return {
                    'articles': [],
                    'is_fallback': False,
                    'message': 'No Wikipedia articles found for this topic'
                }
        
        is_fallback = not specific_query  # True if we're using general search
        scraped_articles = []
        attempted = 0
        max_attempts = max_articles * 2  # Allow some failures while seeking relevant content
        
        for title, url in results:
            if len(scraped_articles) >= max_articles or attempted >= max_attempts:
                break
                
            attempted += 1
            print(f"[{len(scraped_articles) + 1}/{max_articles}] Checking: {title}")
            
            result = self.scrape_article(url)
            if not result:
                print("   ✗ Failed to scrape article")
                continue
                
            article_title, content = result
            
            # Check content relevance - be more lenient with fallback results
            relevance_threshold = 0.1 if is_fallback else 0.2
            if not self.is_content_relevant(content, cleaned_keywords, relevance_threshold):
                print("   ↷ Article content not relevant - skipping")
                continue
            
            scraped_articles.append({
                'title': article_title,
                'content': content,
                'url': url
            })
            print("   ✓ Article scraped and verified relevant")
            
            # Be nice to Wikipedia servers
            time.sleep(1)
        
        if not scraped_articles:
            print("⚠️  No articles passed relevance checks")
            return {
                'articles': [],
                'is_fallback': False,
                'message': 'No relevant articles found after content analysis'
            }
        
        # Prepare result message
        if is_fallback:
            message = (
                "No exact matches found for your query. "
                f"Showing {len(scraped_articles)} general knowledge articles that might be relevant."
            )
        else:
            message = f"Found {len(scraped_articles)} directly relevant articles."
        
        print(f"✅ {message}")
        
        return {
            'articles': scraped_articles,
            'is_fallback': is_fallback,
            'message': message
        }
