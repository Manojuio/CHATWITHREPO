import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# GitHub API
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_API_BASE = "https://api.github.com"

# File filtering
ALLOWED_EXTENSIONS = {
    '.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rb',
    '.php', '.html', '.css', '.json', '.xml', '.yml', '.yaml', '.md', '.txt'
}
EXCLUDED_DIRS = {
    '.git', '__pycache__', 'venv', '.venv',
    'node_modules', 'vendor', 'dist', 'build', 'out', 'target'
}
MAX_FILE_SIZE_MB = 1

# Chunking
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

# Embeddings
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Storage
INDEXES_BASE_DIR = Path("indexes")
INDEXES_BASE_DIR.mkdir(exist_ok=True)
