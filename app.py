from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib
import time

app = Flask(__name__)
CORS(app)

# In-memory storage (replace with vector DB in production)
documents = {}
embeddings_cache = {}

def generate_embedding(text):
    """Generate a simple hash-based embedding (replace with real embedding model)"""
    # In production, use OpenAI API or sentence transformers
    hash_obj = hashlib.md5(text.encode())
    hash_hex = hash_obj.hexdigest()
    # Convert to numeric vector (simplified)
    return [int(hash_hex[i:i+2], 16) / 255.0 for i in range(0, min(32, len(hash_hex)), 2)]

def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors"""
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = sum(a * a for a in vec1) ** 0.5
    magnitude2 = sum(b * b for b in vec2) ** 0.5
    if magnitude1 == 0 or magnitude2 == 0:
        return 0
    return dot_product / (magnitude1 * magnitude2)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "service": "ai-embeddings-search",
        "documents_indexed": len(documents)
    })

@app.route('/api/documents', methods=['POST'])
def index_document():
    """Index a document for search"""
    data = request.json
    
    if not data or 'content' not in data:
        return jsonify({"error": "Content is required"}), 400
    
    doc_id = hashlib.md5(f"{data.get('title', '')}{time.time()}".encode()).hexdigest()[:12]
    content = data['content']
    
    # Generate embedding
    embedding = generate_embedding(content)
    
    # Store document
    documents[doc_id] = {
        "id": doc_id,
        "title": data.get('title', 'Untitled'),
        "content": content,
        "embedding": embedding,
        "metadata": data.get('metadata', {}),
        "created_at": time.time()
    }
    
    return jsonify({
        "document_id": doc_id,
        "status": "indexed",
        "chunks": 1
    }), 201

@app.route('/api/search', methods=['POST'])
def search():
    """Semantic search for documents"""
    data = request.json
    
    if not data or 'query' not in data:
        return jsonify({"error": "Query is required"}), 400
    
    query = data['query']
    top_k = data.get('top_k', 10)
    
    # Generate query embedding
    query_embedding = generate_embedding(query)
    
    # Calculate similarities
    results = []
    for doc_id, doc in documents.items():
        similarity = cosine_similarity(query_embedding, doc['embedding'])
        results.append({
            "document_id": doc_id,
            "title": doc['title'],
            "content": doc['content'][:200] + "..." if len(doc['content']) > 200 else doc['content'],
            "similarity_score": round(similarity, 4),
            "metadata": doc['metadata']
        })
    
    # Sort by similarity and return top K
    results.sort(key=lambda x: x['similarity_score'], reverse=True)
    results = results[:top_k]
    
    return jsonify({
        "query": query,
        "results": results,
        "total_results": len(results)
    })

@app.route('/api/documents/<doc_id>', methods=['GET'])
def get_document(doc_id):
    """Get a document by ID"""
    if doc_id not in documents:
        return jsonify({"error": "Document not found"}), 404
    
    doc = documents[doc_id].copy()
    doc.pop('embedding', None)  # Don't return embedding in response
    
    return jsonify(doc)

@app.route('/api/documents/<doc_id>', methods=['DELETE'])
def delete_document(doc_id):
    """Delete a document"""
    if doc_id not in documents:
        return jsonify({"error": "Document not found"}), 404
    
    del documents[doc_id]
    return jsonify({"message": "Document deleted"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
