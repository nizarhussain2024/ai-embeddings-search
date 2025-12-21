"""
NLP utilities for text processing and analysis.
"""
import re
from typing import List, Dict, Optional

def extract_keywords(text: str, min_length: int = 3) -> List[str]:
    """Extract keywords from text using simple tokenization."""
    words = re.findall(r'\b\w+\b', text.lower())
    return [w for w in words if len(w) >= min_length]

def calculate_text_similarity(text1: str, text2: str) -> float:
    """Calculate simple word overlap similarity between two texts."""
    words1 = set(extract_keywords(text1))
    words2 = set(extract_keywords(text2))
    
    if not words1 or not words2:
        return 0.0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union) if union else 0.0

def normalize_text(text: str) -> str:
    """Normalize text by removing extra whitespace and lowercasing."""
    return ' '.join(text.lower().split())
