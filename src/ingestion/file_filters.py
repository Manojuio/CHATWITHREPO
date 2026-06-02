from pathlib import Path
from config.settings import ALLOWED_EXTENSIONS, EXCLUDED_DIRS, MAX_FILE_SIZE_MB

def should_include(file_path: str, file_size: int) -> bool:
    """
    Decide whether to fetch a file based on its path, extension, and size.
    """
    path = Path(file_path)
    
    # Check excluded directories
    if any(part in EXCLUDED_DIRS for part in path.parts):
        return False
    
    # Check extension
    if path.suffix.lower() not in ALLOWED_EXTENSIONS:
        return False
    
    # Check size (in bytes)
    max_bytes = MAX_FILE_SIZE_MB * 1024 * 1024
    if file_size > max_bytes:
        return False
    
    return True