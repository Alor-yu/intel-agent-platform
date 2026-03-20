from agent.planner import parse_task, plan_task
from tools.web_search import collect_web_data
from tools.kb_search import collect_kb_data
from tools.analyzer import analyze_data
from tools.report_generator import generate_report
from utils.helpers import get_current_time, generate_task_id
from utils.db import save_task_history


def run_task(user_query: str) -> dict:
    task_id = generate_task_id()
    logs = []

    parsed_task = {}
    execution_plan = []
    web_results = []
    kb_result = ""
    analysis_result = {}
    report_result = {}
    status = "success"
    error_message = None

    logs.append(f"[{get_current_time()}] Start task execution")

    try:
        parsed_obj = parse_task(user_query)
        parsed_task = parsed_obj.model_dump()
        logs.append(f"[{get_current_time()}] Task parsed successfully")

        execution_plan = plan_task(parsed_obj)
        logs.append(f"[{get_current_time()}] Plan generated: {execution_plan}")

        if "collect_web_data" in execution_plan:
            try:
                web_items = collect_web_data(parsed_obj.companies, parsed_obj.time_range)
                web_results = [item.model_dump() for item in web_items]
                logs.append(f"[{get_current_time()}] Web data collected: {len(web_results)} items")
            except Exception as e:
                status = "partial_success"
                logs.append(f"[{get_current_time()}] Web data collection failed: {e}")

        if "collect_kb_data" in execution_plan:
            try:
                kb_result = collect_kb_data(parsed_obj.companies, parsed_obj.time_range)
                logs.append(f"[{get_current_time()}] KB data collected")
            except Exception as e:
                status = "partial_success"
                logs.append(f"[{get_current_time()}] KB data collection failed: {e}")

        if "extract_key_updates" in execution_plan or "summarize_findings" in execution_plan:
            try:
                # analyzer 目前接收的是 WebSearchResult 对象列表，因此这里先兼容转换
                from app.schemas.task_schema import WebSearchResult
                web_items = [WebSearchResult(**item) for item in web_results]
                analysis_result = analyze_data(web_items, kb_result)
                logs.append(f"[{get_current_time()}] Analysis completed")
            except Exception as e:
                status = "partial_success"
                logs.append(f"[{get_current_time()}] Analysis failed: {e}")

        if "generate_report" in execution_plan:
            try:
                report_result = generate_report(
                    user_query=user_query,
                    companies=parsed_obj.companies,
                    time_range=parsed_obj.time_range,
                    analysis_result=analysis_result
                )
                logs.append(f"[{get_current_time()}] Report generated and saved: {report_result.get('saved_path', '')}")
            except Exception as e:
                status = "partial_success"
                logs.append(f"[{get_current_time()}] Report generation failed: {e}")

        logs.append(f"[{get_current_time()}] Task execution finished")

    except Exception as e:
        status = "failed"
        error_message = str(e)
        logs.append(f"[{get_current_time()}] Task execution failed: {e}")

    result = {
        "task_id": task_id,
        "status": status,
        "parsed_task": parsed_task,
        "execution_plan": execution_plan,
        "web_results": web_results,
        "kb_result": kb_result,
        "analysis_result": analysis_result,
        "report_result": report_result,
        "logs": logs,
        "error_message": error_message,
    }

    try:
        save_task_history(
            task_id=task_id,
            user_query=user_query,
            parsed_task=result["parsed_task"],
            execution_plan=result["execution_plan"],
            analysis_result=result["analysis_result"],
            report_result=result["report_result"],
            logs=result["logs"]
        )
    except Exception as e:
        result["logs"].append(f"[{get_current_time()}] Save history failed: {e}")

    return result