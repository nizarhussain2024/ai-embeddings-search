from typing import Dict, List, Optional
from datetime import datetime
import json

class DocumentVersion:
    def __init__(self, doc_id: str, content: str, version: int = 1):
        self.doc_id = doc_id
        self.content = content
        self.version = version
        self.created_at = datetime.now().isoformat()
        self.metadata = {}

class DocumentVersionManager:
    def __init__(self):
        self.versions: Dict[str, List[DocumentVersion]] = {}
    
    def create_version(self, doc_id: str, content: str) -> DocumentVersion:
        """Create a new version of a document"""
        if doc_id not in self.versions:
            self.versions[doc_id] = []
        
        version_num = len(self.versions[doc_id]) + 1
        version = DocumentVersion(doc_id, content, version_num)
        self.versions[doc_id].append(version)
        return version
    
    def get_versions(self, doc_id: str) -> List[DocumentVersion]:
        """Get all versions of a document"""
        return self.versions.get(doc_id, [])
    
    def get_latest_version(self, doc_id: str) -> Optional[DocumentVersion]:
        """Get the latest version of a document"""
        versions = self.get_versions(doc_id)
        return versions[-1] if versions else None
    
    def get_version(self, doc_id: str, version: int) -> Optional[DocumentVersion]:
        """Get a specific version of a document"""
        versions = self.get_versions(doc_id)
        if 0 < version <= len(versions):
            return versions[version - 1]
        return None


