import ast
from langchain_core.documents import Document
from typing import List, Dict, Any

def split_python_file(content: str, metadata: Dict[str, Any]) -> List[Document]:
    """
    Splits a Python file into chunks: one per top-level function/class,
    plus one chunk for top-level code (imports, globals, etc.).
    Returns a list of LangChain Document objects.
    """
    documents = []
    
    try:
        tree = ast.parse(content)
    except SyntaxError:
        # Fallback: treat whole file as one chunk
        return [Document(page_content=content, metadata=metadata)]
    
    lines = content.splitlines()
    used_line_ranges = []  # (start, end) line indices (0-based)
    
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            start = node.lineno - 1
            end = node.end_lineno if node.end_lineno else len(lines)
            chunk_text = "\n".join(lines[start:end])
            documents.append(
                Document(page_content=chunk_text, metadata=metadata)
            )
            used_line_ranges.append((start, end))
    
    # Collect top-level lines not inside any function/class
    top_level_lines = []
    total_lines = len(lines)
    for i in range(total_lines):
        if not any(start <= i < end for start, end in used_line_ranges):
            top_level_lines.append(lines[i])
    
    top_level_content = "\n".join(top_level_lines).strip()
    if top_level_content:
        documents.append(
            Document(page_content=top_level_content, metadata=metadata)
        )
    
    return documents