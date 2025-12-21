import os

class Config:
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    MAX_DOCUMENT_SIZE = int(os.getenv('MAX_DOCUMENT_SIZE', 100000))  # 100KB
    DEFAULT_TOP_K = int(os.getenv('DEFAULT_TOP_K', 10))
    EMBEDDING_DIMENSION = int(os.getenv('EMBEDDING_DIMENSION', 32))
    SIMILARITY_THRESHOLD = float(os.getenv('SIMILARITY_THRESHOLD', 0.0))




