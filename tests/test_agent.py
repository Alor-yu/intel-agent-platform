from agent.planner import parse_task, plan_task
from agent.executor import run_task


def test_parse_and_plan():
    query = "分析过去7天Perplexity和Kimi的产品动态，输出竞品日报"
    parsed = parse_task(query)
    plan = plan_task(parsed)

    print("task_type:", parsed.task_type)
    print("companies:", parsed.companies)
    print("time_range:", parsed.time_range)
    print("output_format:", parsed.output_format)
    print("need_comparison:", parsed.need_comparison)
    print("execution_plan:", plan)


def test_run_task():
    query = "分析过去7天Perplexity和Kimi的产品动态，输出竞品日报"
    result = run_task(query)

    print("\n=== RUN TASK ===")
    print("parsed_task:", result["parsed_task"])
    print("execution_plan:", result["execution_plan"])
    print("analysis_summary:", result["analysis_result"].get("summary", ""))
    print("report_markdown:\n", result["report_result"].get("report_markdown", ""))
    print("logs:")
    for log in result["logs"]:
        print(log)


if __name__ == "__main__":
    test_parse_and_plan()
    test_run_task()