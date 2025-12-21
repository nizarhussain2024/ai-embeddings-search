from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib
import time
from typing import List, Dict

app = Flask(__name__)
CORS(app)

documents = {}
embeddings_cache = {}

def generate_embedding(text: str) -> List[float]:
    """Generate a simple hash-based embedding"""
    hash_obj = hashlib.md5(text.encode())
    hash_hex = hash_obj.hexdigest()
    return [int(hash_hex[i:i+2], 16) / 255.0 for i in range(0, min(32, len(hash_hex)), 2)]

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculate cosine similarity between two vectors"""
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = sum(a * a for a in vec1) ** 0.5
    magnitude2 = sum(b * b for b in vec2) ** 0.5
    if magnitude1 == 0 or magnitude2 == 0:
        return 0
    return dot_product / (magnitude1 * magnitude2)

@app.route('/api/documents/batch', methods=['POST'])
def batch_index():
    """Index multiple documents at once"""
    data = request.json
    if not data or 'documents' not in data:
        return jsonify({"error": "documents array is required"}), 400
    
    results = []
    for doc_data in data['documents']:
        doc_id = hashlib.md5(f"{doc_data.get('title', '')}{time.time()}".encode()).hexdigest()[:12]
        content = doc_data.get('content', '')
        embedding = generate_embedding(content)
        
        documents[doc_id] = {
            "id": doc_id,
            "title": doc_data.get('title', 'Untitled'),
            "content": content,
            "embedding": embedding,
            "metadata": doc_data.get('metadata', {}),
            "created_at": time.time()
        }
        results.append(doc_id)
    
    return jsonify({
        "indexed": len(results),
        "document_ids": results
    }), 201

@app.route('/api/search/filter', methods=['POST'])
def search_with_filter():
    """Search with metadata filters"""
    data = request.json
    if not data or 'query' not in data:
        return jsonify({"error": "Query is required"}), 400
    
    query = data['query']
    filters = data.get('filters', {})
    top_k = data.get('top_k', 10)
    
    query_embedding = generate_embedding(query)
    results = []
    
    for doc_id, doc in documents.items():
        # Apply metadata filters
        if filters:
            match = True
            for key, value in filters.items():
                if doc.get('metadata', {}).get(key) != value:
                    match = False
                    break
            if not match:
                continue
        
        similarity = cosine_similarity(query_embedding, doc['embedding'])
        results.append({
            "document_id": doc_id,
            "title": doc['title'],
            "content": doc['content'][:200] + "..." if len(doc['content']) > 200 else doc['content'],
            "similarity_score": round(similarity, 4),
            "metadata": doc['metadata']
        })
    
    results.sort(key=lambda x: x['similarity_score'], reverse=True)
    results = results[:top_k]
    
    return jsonify({
        "query": query,
        "filters": filters,
        "results": results,
        "total_results": len(results)
    })




