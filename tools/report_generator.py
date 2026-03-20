from typing import List, Optional
import os
from datetime import datetime


def build_comparison_rows(companies: List[str], key_updates: List[str]) -> List[dict]:
    if len(companies) < 2:
        return []

    rows = []

    for company in companies[:2]:
        matched_update = ""
        for item in key_updates:
            if company.lower() in item.lower():
                matched_update = item
                break

        rows.append({
            "公司": company,
            "关键动态": matched_update or "暂无明确动态"
        })

    return rows


def build_comparison_table_markdown(rows: List[dict]) -> str:
    if not rows:
        return ""

    table = "| 公司 | 关键动态 |\n|------|----------|\n"
    for row in rows:
        table += f"| {row['公司']} | {row['关键动态']} |\n"
    return table


def generate_markdown_report(
    user_query: str,
    companies: List[str],
    time_range: str,
    summary: str,
    key_updates: List[str],
    comparison_table: Optional[str] = None
) -> str:
    company_text = "、".join(companies) if companies else "AI 行业"
    updates_markdown = "\n".join([f"{idx}. {item}" for idx, item in enumerate(key_updates, start=1)])

    report = f"""# 企业情报分析报告

## 一、任务说明
- 用户任务：{user_query}
- 分析对象：{company_text}
- 时间范围：{time_range}

## 二、核心结论
{summary}

## 三、关键动态
{updates_markdown if updates_markdown else '暂无关键动态'}

## 四、竞品对比
{comparison_table if comparison_table else '当前任务未生成竞品对比表'}

## 五、建议动作
1. 持续跟踪重点竞品的产品更新节奏
2. 对搜索、长文本处理、Agent 工作流能力进行专项观察
3. 建议后续补充真实新闻源与知识库文档以提升结论可靠性
"""
    return report


def save_report_to_file(report_markdown: str, reports_dir: str = "data/reports") -> str:
    os.makedirs(reports_dir, exist_ok=True)
    filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    filepath = os.path.join(reports_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report_markdown)

    return filepath


def generate_report(
    user_query: str,
    companies: List[str],
    time_range: str,
    analysis_result: dict
) -> dict:
    summary = analysis_result.get("summary", "")
    key_updates = analysis_result.get("key_updates", [])

    comparison_rows = build_comparison_rows(companies, key_updates)
    comparison_table = build_comparison_table_markdown(comparison_rows)

    report_markdown = generate_markdown_report(
        user_query=user_query,
        companies=companies,
        time_range=time_range,
        summary=summary,
        key_updates=key_updates,
        comparison_table=comparison_table
    )

    saved_path = save_report_to_file(report_markdown)

    return {
        "summary": summary,
        "key_updates": key_updates,
        "comparison_rows": comparison_rows,
        "comparison_table": comparison_table,
        "report_markdown": report_markdown,
        "saved_path": saved_path
    }