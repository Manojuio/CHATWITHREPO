from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from typing import List, Optional

from config.settings import EMBEDDING_MODEL_NAME, INDEXES_BASE_DIR

_embeddings = None

def get_embeddings():
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    return _embeddings

def create_or_load_vectorstore(documents: List[Document], repo_name: str) -> FAISS:
    """
    Builds or loads a FAISS index for a given repository.
    If index already exists, loads it. Otherwise, builds and saves.
    """
    index_path = INDEXES_BASE_DIR / repo_name
    
    embeddings = get_embeddings()
    
    if index_path.exists():
        print(f"Loading existing FAISS index from {index_path}")
        return FAISS.load_local(
            str(index_path),
            embeddings,
            allow_dangerous_deserialization=True
        )
    
    print(f"Building new FAISS index for {repo_name}...")
    vectorstore = FAISS.from_documents(documents, embeddings)
    
    index_path.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(index_path))
    print(f"Saved index with {vectorstore.index.ntotal} vectors.")
    
    return vectorstore