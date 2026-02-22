from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def get_embedding_model():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)


def create_or_load_vectorstore(docs, repo_name: str):
    """
    If FAISS index exists → load
    Else → build and save
    """

    index_path = Path("indexes") / repo_name

    embeddings = get_embedding_model()

    if index_path.exists():
        print("Loading existing FAISS index...")
        return FAISS.load_local(
            str(index_path),
            embeddings,
            allow_dangerous_deserialization=True
        )

    print("Building new FAISS index...")

    vectorstore = FAISS.from_documents(docs, embeddings)

    index_path.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(index_path))
    print(vectorstore.index.ntotal, "vectors in the index.")

    return vectorstore