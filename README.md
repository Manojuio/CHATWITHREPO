# Code RAG Pipeline – No Clone, Local Qwen 3B

A modular RAG (Retrieval-Augmented Generation) system that answers natural language questions about GitHub repositories **without cloning** them. It fetches files directly via GitHub API, chunks them intelligently (AST for Python, recursive split for others), indexes them locally with FAISS, and answers queries using Qwen 3B via Ollama.

## ✨ Features

- **No `git clone`** – fetch only the files you need using GitHub REST API
- **Local & private** – runs entirely on your machine, no cloud costs
- **AST‑aware splitting** – Python code split by functions/classes, not arbitrary characters
- **Lightweight embeddings** – `all-MiniLM-L6-v2` (80 MB) via HuggingFace
- **QLM generation** – Qwen 3B (via Ollama) – fast, private, offline
- **Persistent FAISS index** – indexes are cached per repository for fast reload

## 🧠 How It Works

1. You provide a GitHub repo URL
2. Pipeline walks the repo tree (API) and downloads only allowed file types
3. Python files are parsed with `ast` and split into logical units; other files use recursive text splitting
4. Each chunk is embedded and stored in a FAISS vector index (saved locally)
5. You ask a question → relevant chunks are retrieved → Qwen 3B generates an answer

## 📦 Requirements

- Python 3.9+
- [Ollama](https://ollama.com) running locally with Qwen 3B model
- GitHub personal access token (optional for public repos, required for private)

## 🚀 Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/code-rag-pipeline.git
cd code-rag-pipeline
2. Create virtual environment
bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows
3. Install dependencies
bash
pip install -r requirements.txt
4. Install Ollama and pull Qwen 3B
bash
# Install Ollama from https://ollama.com
ollama pull qwen2.5-coder:3b   # or qwen2.5:3b
5. Set up environment variables
Create a .env file in the project root:

ini
GITHUB_TOKEN=your_github_personal_access_token   # optional for public repos
HUGGINGFACEHUB_API_TOKEN=                        # optional (not needed for default embedding model)
🧪 Usage
Run the CLI:

bash
python main.py
You will be prompted to enter a GitHub repository URL (e.g. https://github.com/octocat/Hello-World).

The pipeline will:

Fetch file list via GitHub API

Download and chunk matching files

Build/load FAISS index (first run builds, later runs load)

Start an interactive Q&A session

Type your questions and press Enter. Type exit or quit to stop.

Example questions (for a Python repo):

"What does the parse_github_url function do?"

"Which file contains the main entry point?"

"Show me the authentication logic."

📁 Project Structure
text
code-rag-pipeline/
├── .env                     # API keys (ignored by git)
├── requirements.txt
├── main.py                  # CLI entry point
├── config/
│   └── settings.py          # All constants (extensions, chunk size, etc.)
├── src/
│   ├── ingestion/
│   │   ├── github_client.py # GitHub API recursive fetcher (no clone)
│   │   └── file_filters.py  # Extension/directory/size filtering
│   ├── parsing/
│   │   ├── ast_chunker.py   # Python AST splitting
│   │   ├── generic_chunker.py # Recursive split for other languages
│   │   └── parser_factory.py # Routes files to appropriate chunker
│   ├── indexing/
│   │   └── vector_store.py  # FAISS + HuggingFace embeddings
│   └── generation/
│       └── chat_engine.py   # Qwen 3B + retrieval chain (LCEL)
└── indexes/                 # Saved FAISS indexes (created at runtime)
⚙️ Configuration
Edit config/settings.py to change:

ALLOWED_EXTENSIONS – which file types to index

EXCLUDED_DIRS – folders to skip (e.g., node_modules)

MAX_FILE_SIZE_MB – maximum file size to download

CHUNK_SIZE / CHUNK_OVERLAP – for generic splitter

EMBEDDING_MODEL_NAME – any Sentence‑Transformers model

🔐 Rate Limits & Tokens
Without GITHUB_TOKEN: 60 API requests/hour (enough for small repos)

With GITHUB_TOKEN: 5000 requests/hour

The token is also required for accessing private repositories.

🧪 Testing
After setup, test with a small public repo:

bash
python main.py
# Enter: https://github.com/octocat/Hello-World
First run will download the embedding model (~80 MB) and build the index. Subsequent runs will be faster.

❓ Troubleshooting
Problem	Solution
ModuleNotFoundError: No module named 'langchain.chains'	Install langchain-core and use LCEL code (provided in chat_engine.py)
429 Rate Limit Exceeded	Set a valid GITHUB_TOKEN in .env
Ollama connection refused	Ensure Ollama is running (ollama serve)
Empty answer / “I don’t know”	Repo may have no matching files; check ALLOWED_EXTENSIONS
📜 License
MIT

🙏 Acknowledgements
LangChain

FAISS

Ollama

Qwen

GitHub REST API
