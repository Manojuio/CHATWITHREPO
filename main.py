import os
import time
from pathlib import Path
from dotenv import load_dotenv

from app.loader import load_documents
from app.splitter import split_documents
from app.vector_store import create_or_load_vectorstore
from app.repo_handler import clone_repo

from langchain_groq import ChatGroq

def main():
    load_dotenv()

    if not os.getenv("GROQ_API_KEY"):
        print("GROQ_API_KEY not found.")
        return

    user_input = input("Enter local path OR GitHub URL: ").strip()

    # Handle URL vs local path
    if user_input.startswith("http"):
        repo_path = clone_repo(user_input)
    else:
        repo_path = Path(user_input)

    if not Path(repo_path).exists():
        print("Invalid path.")
        return

    repo_name = Path(repo_path).name

    print("Indexing repository...")
    raw_docs = load_documents(repo_path)
    split_docs = split_documents(raw_docs)
    vectorstore = create_or_load_vectorstore(split_docs, repo_name)

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 4}
    )

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0
    )

    print("Ready. Ask questions.\n")

    while True:
        query = input(">> ").strip()
        if query.lower() == "exit":
            break

        start_total = time.time()

        # Retrieval timing
        start_retrieval = time.time()
        docs = retriever.invoke(query)
        end_retrieval = time.time()

        context = "\n\n".join(
            f"Source: {d.metadata.get('source')}\n{d.page_content}"
            for d in docs
        )

        prompt = f"""
You are a code assistant.
Answer using ONLY the context below.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{query}
"""

        # LLM timing
        start_llm = time.time()
        response = llm.invoke(prompt)
        end_llm = time.time()

        end_total = time.time()

        print("\nAnswer:\n")
        print(response.content)

        print("\n--- Latency ---")
        print(f"Retrieval: {(end_retrieval - start_retrieval):.3f}s")
        print(f"LLM: {(end_llm - start_llm):.3f}s")
        print(f"Total: {(end_total - start_total):.3f}s\n")


if __name__ == "__main__":
    main()