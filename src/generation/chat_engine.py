from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain_classic.chains import RetrievalQA

from src.indexing.vector_store import get_embeddings

class CodeChatEngine:
    def __init__(self, vectorstore: FAISS):
        self.vectorstore = vectorstore
        self.llm = Ollama(model="qwen2.5-coder:3b")
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3})
        )
    
    def ask(self, question: str) -> str:
        """Ask a question and get an answer."""
        response = self.qa_chain.invoke({"query": question})
        return response["result"]