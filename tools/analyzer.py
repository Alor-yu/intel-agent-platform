from typing import List
from app.schemas.task_schema import WebSearchResult


def extract_key_updates(web_results: List[WebSearchResult]) -> List[str]:
    updates = []
    for item in web_results:
        updates.append(f"{item.title}：{item.content}")
    return updates


def build_analysis_summary(web_results: List[WebSearchResult], kb_result: str) -> str:
    if not web_results and not kb_result:
        return "未获取到足够信息，暂时无法形成有效分析结论。"

    company_mentions = []
    combined_text = " ".join([f"{item.title} {item.content}" for item in web_results]) + " " + kb_result

    for name in ["Perplexity", "Kimi", "秘塔", "豆包", "DeepSeek", "Claude", "ChatGPT"]:
        if name.lower() in combined_text.lower():
            company_mentions.append(name)

    company_mentions = list(dict.fromkeys(company_mentions))

    if len(company_mentions) >= 2:
        return (
            f"当前资料显示，{company_mentions[0]} 与 {company_mentions[1]} 所在赛道竞争持续加剧，"
            "产品演进重点集中在搜索体验、信息整合、长文本处理与任务执行能力。"
        )

    if len(company_mentions) == 1:
        return (
            f"当前资料显示，{company_mentions[0]} 正在围绕核心能力持续优化，"
            "重点方向包括产品体验提升、信息组织效率和模型能力增强。"
        )

    return "当前资料显示，AI 产品正在持续围绕搜索、Agent、工作流和知识整合能力进行迭代。"


def analyze_data(web_results: List[WebSearchResult], kb_result: str) -> dict:
    key_updates = extract_key_updates(web_results)
    summary = build_analysis_summary(web_results, kb_result)

    return {
        "summary": summary,
        "key_updates": key_updates
    }