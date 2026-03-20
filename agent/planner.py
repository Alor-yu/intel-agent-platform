from typing import List
from app.schemas.task_schema import ParsedTask


def extract_companies(user_query: str) -> List[str]:
    candidates = [
        "Perplexity", "Kimi", "秘塔", "豆包", "腾讯元宝",
        "ChatGPT", "Claude", "DeepSeek", "通义", "元宝"
    ]
    found = [name for name in candidates if name.lower() in user_query.lower()]
    return list(dict.fromkeys(found))


def extract_time_range(user_query: str) -> str:
    query = user_query.lower()

    if "过去7天" in user_query or "最近7天" in user_query or "7天" in query:
        return "7d"
    if "过去30天" in user_query or "最近30天" in user_query or "30天" in query:
        return "30d"
    if "一周" in user_query or "最近一周" in user_query:
        return "7d"
    if "一个月" in user_query or "最近一个月" in user_query:
        return "30d"

    return "7d"


def detect_output_format(user_query: str) -> str:
    if "日报" in user_query:
        return "daily_report"
    if "周报" in user_query:
        return "weekly_report"
    if "markdown" in user_query.lower():
        return "markdown"
    return "report"


def detect_need_comparison(user_query: str) -> bool:
    keywords = ["对比", "比较", "竞品", "差异"]
    return any(word in user_query for word in keywords)


def parse_task(user_query: str) -> ParsedTask:
    companies = extract_companies(user_query)
    time_range = extract_time_range(user_query)
    output_format = detect_output_format(user_query)
    need_comparison = detect_need_comparison(user_query)

    task_type = "competitive_analysis"
    if "分析" not in user_query and "竞品" not in user_query:
        task_type = "general_research"

    return ParsedTask(
        task_type=task_type,
        companies=companies,
        time_range=time_range,
        output_format=output_format,
        need_comparison=need_comparison
    )


def plan_task(parsed_task: ParsedTask) -> List[str]:
    steps = []

    if parsed_task.task_type == "competitive_analysis":
        steps.append("collect_web_data")
        steps.append("collect_kb_data")
        steps.append("extract_key_updates")

        if parsed_task.need_comparison:
            steps.append("compare_competitors")

        steps.append("generate_report")
        return steps

    steps.append("collect_web_data")
    steps.append("summarize_findings")
    steps.append("generate_report")
    return steps