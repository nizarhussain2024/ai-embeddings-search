from typing import List, Dict
import math

def calculate_relevance_score(similarity: float, boost: float = 1.0) -> float:
    """Calculate relevance score with optional boost factor"""
    return similarity * boost

def rank_documents(results: List[Dict], boost_factors: Dict[str, float] = None) -> List[Dict]:
    """Rank search results by relevance score"""
    if boost_factors is None:
        boost_factors = {}
    
    for result in results:
        doc_id = result.get('doc_id', '')
        boost = boost_factors.get(doc_id, 1.0)
        similarity = result.get('similarity', 0.0)
        result['relevance_score'] = calculate_relevance_score(similarity, boost)
    
    # Sort by relevance score descending
    results.sort(key=lambda x: x.get('relevance_score', 0.0), reverse=True)
    return results

def apply_time_decay(results: List[Dict], decay_factor: float = 0.1) -> List[Dict]:
    """Apply time-based decay to older documents"""
    import time
    current_time = time.time()
    
    for result in results:
        created_at = result.get('created_at', current_time)
        age_days = (current_time - created_at) / 86400
        decay = math.exp(-decay_factor * age_days)
        result['relevance_score'] = result.get('relevance_score', 0.0) * decay
    
    results.sort(key=lambda x: x.get('relevance_score', 0.0), reverse=True)
    return results

