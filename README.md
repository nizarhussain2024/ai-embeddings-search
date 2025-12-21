# AI Embeddings Search

A semantic search application powered by AI embeddings and vector similarity.

## Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Client Layer                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Web Interface / API Clients                    │  │
│  │  - Search queries                                     │  │
│  │  - Document upload                                    │  │
│  │  - Results display                                    │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────┬─────────────────────────────────────┘
                        │ HTTP/REST API
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                    Application Layer                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Flask Application                              │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐            │  │
│  │  │  Routes  │─>│ Handlers │─>│ Services │            │  │
│  │  └──────────┘  └──────────┘  └──────────┘            │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐            │  │
│  │  │Embedding │  │  Vector  │  │  Search │            │  │
│  │  │  Model   │  │  Store   │  │  Engine │            │  │
│  │  └──────────┘  └──────────┘  └──────────┘            │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                      AI/ML Layer                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Embedding Models                               │  │
│  │  - OpenAI Embeddings API                              │  │
│  │  - Sentence Transformers                              │  │
│  │  - Custom fine-tuned models                          │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                      Vector Database                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Vector Store (Pinecone, Weaviate, Qdrant)     │  │
│  │  - Document embeddings                                 │  │
│  │  - Metadata storage                                    │  │
│  │  - Similarity search                                    │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Component Architecture

**Core Components:**
- `app.py` - Flask application and routes
- `embeddings/` - Embedding generation service
  - `openai_service.py` - OpenAI API integration
  - `transformer_service.py` - Local model service
- `search/` - Search functionality
  - `vector_search.py` - Vector similarity search
  - `hybrid_search.py` - Combined keyword + semantic search
- `storage/` - Data persistence
  - `vector_store.py` - Vector database interface
  - `metadata_store.py` - Document metadata storage

## Design Decisions

### AI/ML Architecture
- **Embedding Model**: OpenAI text-embedding-ada-002 or Sentence-BERT
- **Vector Database**: Pinecone, Weaviate, or Qdrant for similarity search
- **Search Strategy**: Hybrid search (semantic + keyword)
- **Chunking Strategy**: Text splitting for large documents

### Technology Choices
- **Framework**: Flask for lightweight API
- **Embeddings**: OpenAI API or local transformers
- **Vector DB**: Cloud-based (Pinecone) or self-hosted (Qdrant)
- **Processing**: Async processing for large documents

### Design Patterns
- **Service Layer**: Abstract AI/ML services
- **Repository Pattern**: Vector store abstraction
- **Strategy Pattern**: Multiple embedding models
- **Factory Pattern**: Embedding model factory

## End-to-End Flow

### Flow 1: Index a Document

```
1. Document Upload
   └─> User uploads document via API
       └─> HTTP POST /api/documents
           └─> Request:
           {
             "title": "Machine Learning Guide",
             "content": "Machine learning is...",
             "metadata": { "category": "tech", "author": "John" }
           }

2. Request Processing
   └─> Flask receives request
       └─> Route handler invoked
           └─> Validate input
           └─> Extract document content

3. Text Preprocessing
   └─> Text processing service:
       ├─> Clean text (remove special chars)
       ├─> Normalize whitespace
       └─> Chunk text (if document is large):
           └─> Split into chunks of 500-1000 tokens
           └─> Preserve context between chunks

4. Embedding Generation
   └─> For each text chunk:
       ├─> Call embedding service:
       │   ├─> Option A: OpenAI API
       │   │   └─> POST to OpenAI embeddings endpoint
       │   │       └─> Input: text chunk
       │   │       └─> Model: text-embedding-ada-002
       │   │       └─> Response: 1536-dimensional vector
       │   └─> Option B: Local Model
       │       └─> Load Sentence-BERT model
       │       └─> Generate embedding: 768-dimensional vector
       └─> Store embedding with chunk ID

5. Vector Storage
   └─> Vector database service:
       ├─> Create vector record:
       │   {
       │     "id": "doc-123-chunk-1",
       │     "vector": [0.123, -0.456, ...],
       │     "metadata": {
       │       "document_id": "doc-123",
       │       "chunk_index": 1,
       │       "title": "Machine Learning Guide",
       │       "content": "chunk text...",
       │       "category": "tech"
       │     }
       │   }
       └─> Upsert to vector database:
           ├─> Pinecone: index.upsert(vectors)
           ├─> Weaviate: client.data_object.create()
           └─> Qdrant: client.upsert()

6. Metadata Storage
   └─> Store document metadata:
       ├─> Document ID
       ├─> Title, author, category
       ├─> Chunk count
       └─> Indexing timestamp

7. Response
   └─> HTTP 201 Created
       └─> Response:
       {
         "document_id": "doc-123",
         "chunks_indexed": 5,
         "status": "indexed"
       }
```

### Flow 2: Semantic Search

```
1. Search Query
   └─> User submits search query
       └─> HTTP POST /api/search
           └─> Request:
           {
             "query": "How does neural network training work?",
             "top_k": 10,
             "filter": { "category": "tech" }
           }

2. Query Processing
   └─> Flask receives request
       └─> Handler validates query
           └─> Extract search parameters

3. Query Embedding
   └─> Embedding service:
       ├─> Generate embedding for query:
       │   └─> Same model as documents
       │   └─> Input: "How does neural network training work?"
       │   └─> Output: Query vector [0.789, -0.234, ...]
       └─> Normalize vector (optional)

4. Vector Similarity Search
   └─> Vector database query:
       ├─> Calculate cosine similarity:
       │   └─> similarity = cosine(query_vector, doc_vector)
       ├─> Query vector database:
       │   ├─> Pinecone: index.query(vector=query_vec, top_k=10)
       │   ├─> Weaviate: client.query.get()
       │   └─> Qdrant: client.search()
       └─> Apply filters (category, date, etc.)

5. Results Ranking
   └─> Search service:
       ├─> Sort by similarity score (descending)
       ├─> Apply relevance threshold (e.g., > 0.7)
       ├─> Re-rank results (optional):
       │   └─> Cross-encoder re-ranking
       │   └─> BM25 keyword matching
       └─> Select top K results

6. Result Formatting
   └─> Format results:
       ├─> Extract document metadata
       ├─> Include similarity scores
       ├─> Highlight relevant chunks
       └─> Add context snippets

7. Response
   └─> HTTP 200 OK
       └─> Response:
       {
         "query": "How does neural network training work?",
         "results": [
           {
             "document_id": "doc-123",
             "title": "Machine Learning Guide",
             "chunk_id": "doc-123-chunk-2",
             "content": "Neural networks are trained...",
             "similarity_score": 0.89,
             "metadata": { "category": "tech" }
           },
           ...
         ],
         "total_results": 10
       }
```

### Flow 3: Hybrid Search (Semantic + Keyword)

```
1. Search Query
   └─> User submits query
       └─> POST /api/search/hybrid
           └─> { "query": "Python machine learning", "top_k": 10 }

2. Dual Search Execution
   └─> Parallel execution:
       ├─> Semantic Search:
       │   └─> Generate query embedding
       │   └─> Vector similarity search
       │   └─> Get semantic results
       └─> Keyword Search:
           └─> BM25/Elasticsearch search
           └─> Keyword matching
           └─> Get keyword results

3. Result Fusion
   └─> Combine results:
       ├─> Reciprocal Rank Fusion (RRF):
       │   └─> score = 1 / (k + rank)
       │   └─> Combine scores from both searches
       ├─> Weighted combination:
       │   └─> final_score = 0.7 * semantic + 0.3 * keyword
       └─> Deduplicate results

4. Re-ranking
   └─> Cross-encoder re-ranking:
       ├─> Use more powerful model
       ├─> Re-score top candidates
       └─> Re-order by new scores

5. Response
   └─> Return fused, re-ranked results
```

## Data Flow

```
Indexing Flow:
Document → Preprocess → Chunk → Embed → Vector DB
                                    ↓
                              Metadata Store

Search Flow:
Query → Embed → Vector Search → Rank → Format → Results
         ↓
    Query Vector
         ↓
    Similarity Calc
         ↓
    Top K Results
```

## API Endpoints

### Document Management
- `POST /api/documents` - Index a document
- `GET /api/documents/:id` - Get document by ID
- `DELETE /api/documents/:id` - Delete document

### Search
- `POST /api/search` - Semantic search
- `POST /api/search/hybrid` - Hybrid search
- `GET /api/search/suggestions` - Search suggestions

### Health
- `GET /health` - Health check

## Embedding Models

### OpenAI Embeddings
- Model: `text-embedding-ada-002`
- Dimensions: 1536
- Cost: Pay-per-use
- Latency: ~200ms

### Sentence Transformers
- Model: `all-MiniLM-L6-v2`
- Dimensions: 384
- Cost: Free (self-hosted)
- Latency: ~50ms (local)

## Vector Database Options

### Pinecone
- Managed service
- High performance
- Pay-per-use pricing

### Weaviate
- Open source
- Self-hosted or cloud
- GraphQL API

### Qdrant
- Open source
- Self-hosted
- Rust-based (fast)

## Build & Run

### Prerequisites
- Python 3.11+
- OpenAI API key (optional)
- Vector database account (optional)

### Development
```bash
pip install -r requirements.txt
python app.py
# Server runs on :5000
```

### Production
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker
```bash
docker build -t ai-embeddings-search .
docker run -p 5000:5000 ai-embeddings-search
```

## Future Enhancements

- [ ] Multiple embedding model support
- [ ] Fine-tuned domain-specific models
- [ ] Advanced chunking strategies
- [ ] Query expansion and refinement
- [ ] Result caching
- [ ] Batch indexing
- [ ] Document versioning
- [ ] Multi-language support
- [ ] Image embeddings
- [ ] Graph-based knowledge graph

## AI/NLP Capabilities

This project includes AI and NLP utilities for:
- Text processing and tokenization
- Similarity calculation
- Natural language understanding

*Last updated: 2025-12-20*

## Recent Enhancements (2025-12-21)

### Daily Maintenance
- Code quality improvements and optimizations
- Documentation updates for clarity and accuracy
- Enhanced error handling and edge case management
- Performance optimizations where applicable
- Security and best practices updates

*Last updated: 2025-12-21*
