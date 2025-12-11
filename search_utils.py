def rerank_results(results, query, top_k=5):
    """Re-rank search results using a simple scoring mechanism"""
    # In production, use a cross-encoder model for re-ranking
    for result in results:
        # Boost score if query terms appear in title
        title_boost = sum(1 for word in query.lower().split() if word in result['title'].lower())
        result['rerank_score'] = result['similarity_score'] + (title_boost * 0.1)
    
    # Sort by rerank score
    results.sort(key=lambda x: x['rerank_score'], reverse=True)
    return results[:top_k]

def extract_keywords(text, max_keywords=5):
    """Extract keywords from text (simplified version)"""
    # In production, use NLP libraries like spaCy or NLTK
    words = text.lower().split()
    # Remove common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    keywords = [w for w in words if w not in stop_words and len(w) > 3]
    return keywords[:max_keywords]

