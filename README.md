#📘 GitHub Repository RAG Assistant

AI-powered semantic search and Q&A over any GitHub repository using Retrieval-Augmented Generation (RAG).

🚀 Problem

Developers waste time navigating unfamiliar codebases.

Traditional search:

Keyword-based

Context-blind

Cannot explain logic

This project enables:

Ask natural language questions about any GitHub repository and receive grounded, context-aware answers.

🧠 What This System Does

Given:

A GitHub repository URL
or

A local project folder

The system:

Clones the repository (if URL provided)

Loads relevant source files

Splits code semantically (AST-based for Python)

Generates embeddings

Stores vectors in FAISS

Retrieves relevant chunks using MMR

Sends context to Groq LLM

Returns grounded answer with latency breakdown

🏗 Architecture
GitHub URL / Local Path
        ↓
Repository Cloning
        ↓
File Loader (Filtered Extensions)
        ↓
Semantic Splitter
   ├── AST-based for Python
   └── Recursive splitter for other files
        ↓
SentenceTransformer Embeddings
        ↓
FAISS Vector Store (Persistent)
        ↓
Retriever (MMR Search)
        ↓
Groq LLM (Llama3)
        ↓
Grounded Answer
🛠 Tech Stack

Python

LangChain (v0.2+)

FAISS

SentenceTransformers (all-MiniLM-L6-v2)

Groq (Llama3-8B)

GitPython

uv (package management)

✨ Features

GitHub repository cloning

Local folder indexing

Python AST-based semantic chunking

FAISS persistent vector store

MMR-based retrieval

Grounded prompt (reduces hallucination)

Latency measurement (retrieval + LLM breakdown)

Modular architecture

📊 Example Output
Answer:
The repository implements a study circle platform with authentication,
group management, and resource sharing features.

--- Latency ---
Retrieval: 0.043s
LLM: 0.486s
Total: 0.529s
⚙️ Installation
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

uv venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # Mac/Linux

uv sync
🔑 Environment Setup

Create a .env file:

GROQ_API_KEY=your_groq_api_key_here
▶️ Run
uv run main.py

Then enter:

Local folder path
or

GitHub repository URL

Ask questions in natural language.

Type exit to quit.

🧪 Example Queries

What does this project do?

What stack is used?

How authentication works?

Where is database configured?

What are the main features?

🔮 Future Improvements

Hybrid search (BM25 + FAISS)

Cross-encoder reranking

Token-aware context packing

Streaming responses

Repo update detection & index invalidation

REST API deployment

Evaluation metrics (Recall@k, latency benchmarks)

🎯 Why This Project Matters

This project demonstrates:

System design thinking

Retrieval engineering

Prompt design

Latency instrumentation

Modular backend architecture

Real-world AI integration

📌 Author

Built as an AI-powered semantic codebase exploration tool for backend + GenAI learning.
