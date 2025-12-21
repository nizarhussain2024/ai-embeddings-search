from typing import List, Dict
from document_manager import DocumentManager

class BatchOperations:
    def __init__(self, doc_manager: DocumentManager):
        self.doc_manager = doc_manager
    
    def batch_index(self, documents: List[Dict]) -> Dict:
        """Index multiple documents in batch"""
        results = {
            "success": [],
            "failed": [],
            "total": len(documents)
        }
        
        for doc in documents:
            try:
                doc_id = doc.get('id') or self._generate_id()
                if self.doc_manager.add_document(doc_id, doc):
                    results["success"].append(doc_id)
                else:
                    results["failed"].append({"doc": doc, "error": "Failed to add"})
            except Exception as e:
                results["failed"].append({"doc": doc, "error": str(e)})
        
        return results
    
    def batch_delete(self, doc_ids: List[str]) -> Dict:
        """Delete multiple documents"""
        results = {
            "deleted": [],
            "not_found": [],
            "total": len(doc_ids)
        }
        
        for doc_id in doc_ids:
            if self.doc_manager.delete_document(doc_id):
                results["deleted"].append(doc_id)
            else:
                results["not_found"].append(doc_id)
        
        return results
    
    def batch_update(self, updates: List[Dict]) -> Dict:
        """Update multiple documents"""
        results = {
            "updated": [],
            "failed": [],
            "total": len(updates)
        }
        
        for update in updates:
            doc_id = update.get('id')
            if not doc_id:
                results["failed"].append({"update": update, "error": "Missing id"})
                continue
            
            doc = self.doc_manager.get_document(doc_id)
            if not doc:
                results["failed"].append({"update": update, "error": "Document not found"})
                continue
            
            # Merge updates
            doc.update(update)
            if self.doc_manager.add_document(doc_id, doc):
                results["updated"].append(doc_id)
            else:
                results["failed"].append({"update": update, "error": "Update failed"})
        
        return results
    
    def _generate_id(self) -> str:
        import hashlib
        import time
        return hashlib.md5(f"{time.time()}".encode()).hexdigest()[:12]



