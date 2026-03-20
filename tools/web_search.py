from typing import List
from app.schemas.task_schema import WebSearchResult
from utils.config import settings


def build_search_query(companies: List[str], time_range: str) -> str:
    if not companies:
        return f"AI 产品动态 {time_range}"
    company_part = " ".join(companies)
    return f"{company_part} 产品动态 {time_range}"


def mock_search_web(query: str) -> List[WebSearchResult]:
    mock_results = [
        WebSearchResult(
            title="Perplexity 推进 AI 搜索产品体验优化",
            content="近期产品更新集中在答案组织、搜索交互和结果可读性提升。",
            url="https://example.com/perplexity-update",
            source="mock"
        ),
        WebSearchResult(
            title="Kimi 强化长文本处理与信息整合能力",
            content="近期动态显示其继续优化长上下文理解与知识整合体验。",
            url="https://example.com/kimi-update",
            source="mock"
        ),
        WebSearchResult(
            title="AI 搜索赛道竞争加剧",
            content="多家产品正在围绕搜索、问答、Agent 和工作流能力持续迭代。",
            url="https://example.com/ai-search-market",
            source="mock"
        ),
    ]

    filtered = []
    lower_query = query.lower()
    for item in mock_results:
        text = f"{item.title} {item.content}".lower()
        if any(word in text for word in lower_query.split()):
            filtered.append(item)

    return filtered if filtered else mock_results


def real_search_web(query: str) -> List[WebSearchResult]:
    """
    真实搜索接口预留。
    当前先返回空列表，后面可接 SerpAPI / Tavily / 自建搜索服务。
    """
    return []


def search_web(query: str) -> List[WebSearchResult]:
    mode = settings.WEB_SEARCH_MODE

    if mode == "real":
        results = real_search_web(query)
        if results:
            return results
        return mock_search_web(query)

    return mock_search_web(query)


def collect_web_data(companies: List[str], time_range: str) -> List[WebSearchResult]:
    query = build_search_query(companies, time_range)
    return search_web(query)