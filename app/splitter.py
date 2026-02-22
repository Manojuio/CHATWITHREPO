from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


import ast


CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


def split_documents(raw_documents: list) -> list:
    """
    raw_documents: list of dict
    {
        "content": str,
        "metadata": {...}
    }

    Returns: List[Document]
    """

    documents = []

    for doc in raw_documents:
        content = doc["content"]
        metadata = doc["metadata"]
        extension = metadata.get("extension")

        # Python files → AST splitting
        if extension == ".py":
            documents.extend(_split_python(content, metadata))
        else:
            documents.extend(_split_generic(content, metadata))

    return documents


# ---------- Python AST Splitter ----------

def _split_python(content: str, metadata: dict) -> list:
    documents = []

    try:
        tree = ast.parse(content)
    except Exception:
        # If parsing fails, fallback to generic splitter
        return _split_generic(content, metadata)

    lines = content.splitlines()
    used_line_ranges = []

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            start = node.lineno - 1
            end = node.end_lineno

            chunk_text = "\n".join(lines[start:end])

            documents.append(
                Document(
                    page_content=chunk_text,
                    metadata=metadata
                )
            )

            used_line_ranges.append((start, end))

    # Handle top-level code (imports, globals, etc.)
    top_level_lines = []
    total_lines = len(lines)

    for i in range(total_lines):
        if not any(start <= i < end for start, end in used_line_ranges):
            top_level_lines.append(lines[i])

    top_level_content = "\n".join(top_level_lines).strip()

    if top_level_content:
        documents.append(
            Document(
                page_content=top_level_content,
                metadata=metadata
            )
        )

    return documents


# ---------- Generic Splitter (JS, Java, etc.) ----------

def _split_generic(content: str, metadata: dict) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = splitter.split_text(content)

    return [
        Document(page_content=chunk, metadata=metadata)
        for chunk in chunks
    ]