from pathlib import Path

ALLOWED_EXTENSIONS = {
    '.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rb',
    '.php', '.html', '.css', '.json', '.xml', '.yml', '.yaml', '.md', '.txt'
}

EXCLUDED_DIRS = {
    '.git', '__pycache__', 'venv', '.venv',
    'node_modules', 'vendor', 'dist', 'build', 'out', 'target'
}

MAX_FILE_SIZE_MB = 1


def load_documents(repo_path: str) -> list:
    repo = Path(repo_path)
    documents = []

    for file in repo.rglob('*'):

        # Skip excluded directories
        if any(part in EXCLUDED_DIRS for part in file.parts):
            continue

        if not file.is_file():
            continue

        if file.suffix.lower() not in ALLOWED_EXTENSIONS:
            continue

        if file.stat().st_size > MAX_FILE_SIZE_MB * 1024 * 1024:
            continue

        try:
            content = file.read_text(encoding='utf-8')
        except Exception:
            continue

        documents.append({
            "content": content,
            "metadata": {
                "source": str(file),
                "extension": file.suffix.lower(),
                "size": file.stat().st_size
            }
        })

    return documents