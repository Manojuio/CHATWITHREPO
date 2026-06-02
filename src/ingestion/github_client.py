import base64
import requests
from typing import List, Dict, Any
from pathlib import Path

from config.settings import GITHUB_TOKEN,GITHUB_API_BASE
from src.ingestion.file_filters import should_include

# Headers for GitHub API authentication
HEADERS = {
    "Accept": "application/vnd.github.v3+json"
}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"token {GITHUB_TOKEN}"

def parse_github_url(repo_url: str) -> tuple:
    """
    Extracts owner and repo name from a GitHub URL.
    Supports formats:
    - https://github.com/owner/repo
    - https://github.com/owner/repo.git
    - github.com/owner/repo
    """
    # Remove protocol if present
    url = repo_url.replace("https://", "").replace("http://", "")
    if url.startswith("github.com/"):
        url = url[len("github.com/"):]
    parts = url.rstrip("/").split("/")
    owner = parts[0]
    repo = parts[1].replace(".git", "")
    return owner, repo

def fetch_file_content(file_api_url: str) -> str:
    """
    Fetches and decodes base64 content from a GitHub file API URL.
    Returns empty string on failure.
    """
    response = requests.get(file_api_url, headers=HEADERS)
    if response.status_code != 200:
        return ""
    data = response.json()
    if data.get("encoding") == "base64":
        decoded_bytes = base64.b64decode(data["content"])
        return decoded_bytes.decode("utf-8", errors="ignore")
    return ""

def fetch_repo_contents_recursive(owner: str, repo: str, path: str = "") -> List[Dict[str, Any]]:
    """
    Recursively walks a GitHub repository directory and returns a list of
    document dictionaries (content + metadata) for all files that pass filtering.
    """
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/contents/{path}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        # Possibly a private repo or rate limit issue
        print(f"Error fetching {url}: {response.status_code}")
        return []
    
    items = response.json()
    # If it's a single file (not a directory list), wrap it
    if not isinstance(items, list):
        items = [items]
    
    documents = []
    
    for item in items:
        if item["type"] == "dir":
            # Recurse into subdirectory
            docs = fetch_repo_contents_recursive(owner, repo, item["path"])
            documents.extend(docs)
        elif item["type"] == "file":
            file_path = item["path"]
            file_size = item.get("size", 0)
            
            if should_include(file_path, file_size):
                print(f"Fetching: {file_path}")
                content = fetch_file_content(item["url"])
                if content:
                    documents.append({
                        "content": content,
                        "metadata": {
                            "source": file_path,
                            "extension": Path(file_path).suffix.lower(),
                            "size": file_size,
                            "repo": f"{owner}/{repo}"
                        }
                    })
    return documents

def fetch_repository(repo_url: str, branch: str = "main") -> List[Dict[str, Any]]:
    """
    Main entry point: given a GitHub repo URL, returns a list of document dicts
    (same format as your old loader.py).
    Optionally specify branch (default 'main').
    """
    owner, repo = parse_github_url(repo_url)
    # Note: For branch other than default, you would need to adjust the API calls
    # (e.g., /repos/{owner}/{repo}/contents/{path}?ref={branch})
    # We'll use the default branch for simplicity; can be extended.
    print(f"Fetching repository: {owner}/{repo}")
    return fetch_repo_contents_recursive(owner, repo)