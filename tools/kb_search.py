from typing import List
from utils.config import settings
from rag.retriever import retrieve_knowledge


def build_kb_query(companies: List[str], time_range: str) -> str:
    if not companies:
        return f"AI 行业资料 {time_range}"
    company_part = " ".join(companies)
    return f"{company_part} 知识库资料 {time_range}"


def mock_search_kb(query: str) -> str:
    mock_kb = {
        "perplexity": "Perplexity 的核心优势在于 AI 搜索体验、答案组织方式和检索式交互设计。",
        "kimi": "Kimi 的核心优势在于长文本处理、上下文理解以及复杂信息整合能力。",
        "ai": "AI 搜索赛道的竞争重点正在从单轮问答转向搜索、Agent、工作流与生产力结合。"
    }

    lower_query = query.lower()
    matched = []

    for key, value in mock_kb.items():
        if key in lower_query:
            matched.append(value)

    if not matched:
        matched.append(mock_kb["ai"])

    return "\n".join(matched)


def real_search_kb(query: str) -> str:
    results = retrieve_knowledge(
        query=query,
        use_real=(settings.RAG_BACKEND == "real")
    )
    return "\n".join(results) if results else ""


def search_kb(query: str) -> str:
    mode = settings.KB_SEARCH_MODE

    if mode == "real":
        result = real_search_kb(query)
        if result:
            return result
        return mock_search_kb(query)

    return mock_search_kb(query)


def collect_kb_data(companies: List[str], time_range: str) -> str:
    query = build_kb_query(companies, time_range)
    return search_kb(query)