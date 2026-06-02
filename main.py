#!/usr/bin/env python3
"""
CLI for Code RAG Pipeline with No-Clone GitHub fetching.
"""

import sys
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.ingestion.github_client import fetch_repository
from src.parsing.parser_factory import chunk_document
from src.indexing.vector_store import create_or_load_vectorstore
from src.generation.chat_engine import CodeChatEngine

def main():
    print("=== Code RAG Pipeline ===")
    repo_url = input("Enter GitHub repository URL: ").strip()
    if not repo_url:
        print("No URL provided. Exiting.")
        return
    
    # 1. Fetch files via GitHub API (no clone)
    print("\n[1/4] Fetching repository contents via GitHub API...")
    raw_documents = fetch_repository(repo_url)
    if not raw_documents:
        print("No documents found. Check URL or rate limits.")
        return
    print(f"Fetched {len(raw_documents)} files.")
    
    # 2. Chunk documents (AST for Python, generic for others)
    print("\n[2/4] Chunking documents...")
    all_chunks = []
    for raw_doc in raw_documents:
        chunks = chunk_document(raw_doc)
        all_chunks.extend(chunks)
    print(f"Created {len(all_chunks)} chunks.")
    
    # 3. Create/load vector store
    print("\n[3/4] Building/loading FAISS index...")
    # Extract repo name from URL for index folder
    owner_repo = raw_documents[0]["metadata"].get("repo", "unknown")
    repo_name = owner_repo.replace("/", "_")
    vectorstore = create_or_load_vectorstore(all_chunks, repo_name)
    
    # 4. Start chat engine
    print("\n[4/4] Initializing Qwen chat engine...")
    chat = CodeChatEngine(vectorstore)
    
    print("\n✅ Ready! Ask questions about the codebase (type 'exit' to quit).\n")
    while True:
        question = input("❓ You: ")
        if question.lower() in ("exit", "quit"):
            break
        answer = chat.ask(question)
        print(f"🤖 Answer: {answer}\n")

if __name__ == "__main__":
    main()