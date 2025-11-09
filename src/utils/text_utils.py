"""
Text processing utilities
"""

import re
from typing import List


def truncate_text(text: str, max_length: int = 800) -> str:
    """
    Truncate text to a maximum length, breaking at word boundaries.
    
    Args:
        text: Text to truncate
        max_length: Maximum length in characters
        
    Returns:
        Truncated text with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    
    truncated = text[:max_length].rsplit(" ", 1)[0]
    return truncated + " ..."


def clean_query_for_wiki(query: str) -> str:
    """
    Clean and enhance query for Wikipedia search.
    Handles AI/tech terms, removes stopwords, and adds context.
    
    Args:
        query: Original search query
        
    Returns:
        Enhanced query string
    """
    # Initial cleaning
    query = query.lower()
    query = re.sub(r'[^\w\s]', '', query)  # remove punctuation
    
    # Define AI/tech term mappings
    ai_terms = {
        'ia': 'artificial intelligence',
        'ai': 'artificial intelligence',
        'ml': 'machine learning',
        'dl': 'deep learning',
        'nlp': 'natural language processing'
    }
    
    # Define domain-specific context terms
    domain_contexts = {
        'ecology': ['environmental', 'ecosystem', 'biological'],
        'climate': ['environmental', 'weather', 'atmospheric'],
        'health': ['medical', 'healthcare', 'clinical'],
        'economy': ['economic', 'financial', 'market']
    }
    
    # Careful stopword selection (keep important modifiers)
    stopwords = {
        'what', 'about', 'how', 'the', 'a', 'an', 'and',
        'to', 'of', 'for', 'with', 'by'
    }
    
    # Split into words
    words = query.split()
    enhanced_words = []
    
    # First pass: replace AI terms and keep non-stopwords
    for word in words:
        if word in ai_terms:
            enhanced_words.append(ai_terms[word])
        elif word not in stopwords:
            enhanced_words.append(word)
    
    # Add domain context if detected
    query_str = ' '.join(enhanced_words)
    for domain, context_terms in domain_contexts.items():
        if domain in query_str.lower():
            enhanced_words.extend(context_terms)
    
    # Join and deduplicate terms
    return ' '.join(dict.fromkeys(enhanced_words))
