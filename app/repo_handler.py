from pathlib import Path
from git import Repo
import shutil

BASE_CLONE_DIR = Path("cloned_repos")

def clone_repo(repo_url: str) -> Path:
    """
    Clones a git repository to a local directory.

    """

    BASE_CLONE_DIR.mkdir(exist_ok=True)

    repo_name = repo_url.rstrip("/").split("/")[-1]
    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]
    
    local_path = BASE_CLONE_DIR / repo_name

    if(local_path.exists()):
        print(f"Repository '{repo_name}' already exists locally. Removing it for a fresh clone.")
        return local_path

    print('Cloning repository...')
    Repo.clone_from(repo_url, local_path)

    return local_path