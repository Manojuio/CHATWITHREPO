from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List, Dict, Any

from config.settings import CHUNK_SIZE, CHUNK_OVERLAP

def split_generic_file(content: str, metadata: Dict[str, Any]) -> List[Document]:
    """
    Splits any text file using RecursiveCharacterTextSplitter.
    Returns a list of LangChain Document objects.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_text(content)
    return [Document(page_content=chunk, metadata=metadata) for chunk in chunks]