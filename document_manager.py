from typing import List, Dict, Optional
import time

class DocumentManager:
    def __init__(self):
        self.documents = {}
        self.categories = set()
    
    def add_document(self, doc_id: str, document: Dict) -> bool:
        """Add or update a document"""
        if doc_id in self.documents:
            document['updated_at'] = time.time()
        else:
            document['created_at'] = time.time()
        
        self.documents[doc_id] = document
        
        # Track categories
        if 'metadata' in document and 'category' in document['metadata']:
            self.categories.add(document['metadata']['category'])
        
        return True
    
    def get_document(self, doc_id: str) -> Optional[Dict]:
        """Get a document by ID"""
        return self.documents.get(doc_id)
    
    def list_documents(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """List documents with pagination"""
        docs = list(self.documents.values())
        return docs[offset:offset+limit]
    
    def delete_document(self, doc_id: str) -> bool:
        """Delete a document"""
        if doc_id in self.documents:
            del self.documents[doc_id]
            return True
        return False
    
    def get_categories(self) -> List[str]:
        """Get all categories"""
        return list(self.categories)
    
    def get_stats(self) -> Dict:
        """Get document statistics"""
        return {
            "total_documents": len(self.documents),
            "categories": len(self.categories),
            "category_list": list(self.categories)
        }




