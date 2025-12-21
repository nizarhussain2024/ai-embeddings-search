from typing import List, Dict
from datetime import datetime
import json

class SearchHistory:
    def __init__(self):
        self.history: List[Dict] = []
        self.max_history = 100
    
    def add_search(self, query: str, results_count: int, filters: Dict = None):
        """Record a search query"""
        entry = {
            "query": query,
            "results_count": results_count,
            "filters": filters or {},
            "timestamp": datetime.now().isoformat()
        }
        self.history.append(entry)
        
        # Keep only last N searches
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
    
    def get_recent_searches(self, limit: int = 10) -> List[Dict]:
        """Get recent search queries"""
        return self.history[-limit:]
    
    def get_popular_queries(self, limit: int = 10) -> List[Dict]:
        """Get most popular search queries"""
        query_counts = {}
        for entry in self.history:
            query = entry["query"]
            query_counts[query] = query_counts.get(query, 0) + 1
        
        popular = sorted(query_counts.items(), key=lambda x: x[1], reverse=True)
        return [{"query": q, "count": c} for q, c in popular[:limit]]
    
    def get_history_stats(self) -> Dict:
        """Get search history statistics"""
        return {
            "total_searches": len(self.history),
            "unique_queries": len(set(e["query"] for e in self.history)),
            "average_results": sum(e["results_count"] for e in self.history) / len(self.history) if self.history else 0
        }



