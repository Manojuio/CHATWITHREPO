from langchain_core.documents import Document
from typing import List, Dict, Any

from src.parsing.ast_chunker import split_python_file
from src.parsing.generic_chunker import split_generic_file

def chunk_document(raw_doc: Dict[str, Any]) -> List[Document]:
    """
    Takes a raw document dict (with 'content' and 'metadata' keys)
    and returns a list of chunked LangChain Documents.
    """
    content = raw_doc["content"]
    metadata = raw_doc["metadata"]
    extension = metadata.get("extension", "")
    
    if extension == ".py":
        return split_python_file(content, metadata)
    else:
        return split_generic_file(content, metadata)