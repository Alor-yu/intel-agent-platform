from tools.web_search import build_search_query, collect_web_data
from tools.kb_search import build_kb_query, collect_kb_data
from tools.analyzer import analyze_data
from tools.report_generator import generate_report


def test_web_search():
    companies = ["Perplexity", "Kimi"]
    time_range = "7d"

    query = build_search_query(companies, time_range)
    results = collect_web_data(companies, time_range)

    print("=== WEB SEARCH ===")
    print("query:", query)
    print("result_count:", len(results))

    for i, item in enumerate(results, start=1):
        print(f"\nResult {i}")
        print("title:", item.title)
        print("content:", item.content)
        print("url:", item.url)
        print("source:", item.source)


def test_kb_search():
    companies = ["Perplexity", "Kimi"]
    time_range = "7d"

    query = build_kb_query(companies, time_range)
    result = collect_kb_data(companies, time_range)

    print("\n=== KB SEARCH ===")
    print("query:", query)
    print("kb_result:", result)


def test_analyze():
    companies = ["Perplexity", "Kimi"]
    time_range = "7d"

    web_results = collect_web_data(companies, time_range)
    kb_result = collect_kb_data(companies, time_range)
    analysis = analyze_data(web_results, kb_result)

    print("\n=== ANALYSIS ===")
    print("summary:", analysis["summary"])
    print("key_updates:")

    for i, item in enumerate(analysis["key_updates"], start=1):
        print(f"{i}. {item}")


def test_report():
    query = "分析过去7天Perplexity和Kimi的产品动态，输出竞品日报"
    companies = ["Perplexity", "Kimi"]
    time_range = "7d"

    web_results = collect_web_data(companies, time_range)
    kb_result = collect_kb_data(companies, time_range)
    analysis = analyze_data(web_results, kb_result)
    report = generate_report(
        user_query=query,
        companies=companies,
        time_range=time_range,
        analysis_result=analysis
    )

    print("\n=== REPORT ===")
    print("summary:", report["summary"])
    print("comparison_table:\n", report["comparison_table"])
    print("report_markdown:\n", report["report_markdown"])


if __name__ == "__main__":
    test_web_search()
    test_kb_search()
    test_analyze()
    test_report()