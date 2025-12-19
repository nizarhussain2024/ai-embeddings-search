class DocumentNotFoundError(Exception):
    pass

class InvalidDocumentError(Exception):
    pass

class SearchError(Exception):
    pass

def handle_error(error):
    """Convert exceptions to HTTP error responses"""
    error_map = {
        DocumentNotFoundError: (404, "Document not found"),
        InvalidDocumentError: (400, "Invalid document"),
        SearchError: (500, "Search error occurred"),
    }
    
    error_type = type(error)
    if error_type in error_map:
        status_code, message = error_map[error_type]
        return {"error": message, "details": str(error)}, status_code
    
    return {"error": "Internal server error"}, 500




