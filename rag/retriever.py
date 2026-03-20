from pathlib import Path
from typing import List


KB_FILE_PATH = Path("data/raw/company_notes.txt")


def load_local_knowledge() -> List[str]:
    if not KB_FILE_PATH.exists():
        return []

    text = KB_FILE_PATH.read_text(encoding="utf-8")
    chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]
    return chunks


def simple_keyword_retrieve(query: str, top_k: int = 3) -> List[str]:
    knowledge_chunks = load_local_knowledge()
    if not knowledge_chunks:
        return []

    query_terms = [term.strip().lower() for term in query.split() if term.strip()]
    scored = []

    for chunk in knowledge_chunks:
        score = sum(1 for term in query_terms if term in chunk.lower())
        scored.append((score, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)

    results = [item[1] for item in scored if item[0] > 0]
    if not results:
        return knowledge_chunks[:top_k]

    return results[:top_k]


def retrieve_knowledge(query: str, use_real: bool = False) -> List[str]:
    return simple_keyword_retrieve(query)