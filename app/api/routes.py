from fastapi import APIRouter
from app.schemas.task_schema import TaskRequest, APIResponse
from utils.helpers import generate_task_id, get_current_time
from utils.db import (
    init_db,
    get_task_history,
    get_task_by_id,
    delete_task_by_id,
    clear_task_history,
)
from agent.planner import parse_task, plan_task
from agent.executor import run_task
from tools.web_search import collect_web_data
from tools.kb_search import collect_kb_data
from tools.analyzer import analyze_data
from tools.report_generator import generate_report

router = APIRouter()

init_db()


@router.get("/health")
def health_check():
    return APIResponse(
        success=True,
        message="API is healthy",
        data={"time": get_current_time()}
    )


@router.post("/task/parse-demo")
def parse_demo(task: TaskRequest):
    return APIResponse(
        success=True,
        message="Task received successfully",
        data={
            "task_id": generate_task_id(),
            "user_query": task.user_query,
            "received_at": get_current_time()
        }
    )


@router.post("/task/parse")
def parse_user_task(task: TaskRequest):
    parsed = parse_task(task.user_query)

    return APIResponse(
        success=True,
        message="Task parsed successfully",
        data={
            "task_id": generate_task_id(),
            "user_query": task.user_query,
            "parsed_task": parsed.model_dump(),
            "parsed_at": get_current_time()
        }
    )


@router.post("/task/plan")
def plan_user_task(task: TaskRequest):
    parsed = parse_task(task.user_query)
    plan = plan_task(parsed)

    return APIResponse(
        success=True,
        message="Task planned successfully",
        data={
            "task_id": generate_task_id(),
            "user_query": task.user_query,
            "parsed_task": parsed.model_dump(),
            "execution_plan": plan,
            "planned_at": get_current_time()
        }
    )


@router.post("/task/web-search")
def run_web_search(task: TaskRequest):
    parsed = parse_task(task.user_query)
    results = collect_web_data(parsed.companies, parsed.time_range)

    return APIResponse(
        success=True,
        message="Web search completed successfully",
        data={
            "task_id": generate_task_id(),
            "user_query": task.user_query,
            "parsed_task": parsed.model_dump(),
            "search_results": [item.model_dump() for item in results],
            "searched_at": get_current_time()
        }
    )


@router.post("/task/kb-search")
def run_kb_search(task: TaskRequest):
    parsed = parse_task(task.user_query)
    kb_result = collect_kb_data(parsed.companies, parsed.time_range)

    return APIResponse(
        success=True,
        message="KB search completed successfully",
        data={
            "task_id": generate_task_id(),
            "user_query": task.user_query,
            "parsed_task": parsed.model_dump(),
            "kb_result": kb_result,
            "searched_at": get_current_time()
        }
    )


@router.post("/task/analyze")
def run_analysis(task: TaskRequest):
    parsed = parse_task(task.user_query)
    web_results = collect_web_data(parsed.companies, parsed.time_range)
    kb_result = collect_kb_data(parsed.companies, parsed.time_range)
    analysis = analyze_data(web_results, kb_result)

    return APIResponse(
        success=True,
        message="Analysis completed successfully",
        data={
            "task_id": generate_task_id(),
            "user_query": task.user_query,
            "parsed_task": parsed.model_dump(),
            "analysis_result": analysis,
            "analyzed_at": get_current_time()
        }
    )


@router.post("/task/report")
def run_report(task: TaskRequest):
    parsed = parse_task(task.user_query)
    web_results = collect_web_data(parsed.companies, parsed.time_range)
    kb_result = collect_kb_data(parsed.companies, parsed.time_range)
    analysis = analyze_data(web_results, kb_result)
    report = generate_report(
        user_query=task.user_query,
        companies=parsed.companies,
        time_range=parsed.time_range,
        analysis_result=analysis
    )

    return APIResponse(
        success=True,
        message="Report generated successfully",
        data={
            "task_id": generate_task_id(),
            "user_query": task.user_query,
            "parsed_task": parsed.model_dump(),
            "report_result": report,
            "generated_at": get_current_time()
        }
    )


@router.post("/task/run")
def run_full_task(task: TaskRequest):
    result = run_task(task.user_query)

    return APIResponse(
        success=True,
        message="Task executed successfully",
        data={
            "user_query": task.user_query,
            **result,
            "executed_at": get_current_time()
        }
    )


@router.get("/task/history")
def read_task_history(limit: int = 20):
    history = get_task_history(limit=limit)
    return APIResponse(
        success=True,
        message="Task history fetched successfully",
        data={"items": history}
    )


@router.get("/task/history/{task_id}")
def read_task_detail(task_id: str):
    item = get_task_by_id(task_id)
    if not item:
        return APIResponse(
            success=False,
            message="Task not found",
            data=None
        )

    return APIResponse(
        success=True,
        message="Task detail fetched successfully",
        data=item
    )
@router.delete("/task/history/{task_id}")
def remove_task_history_item(task_id: str):
    ok = delete_task_by_id(task_id)
    if not ok:
        return APIResponse(
            success=False,
            message="Task not found",
            data=None
        )

    return APIResponse(
        success=True,
        message="Task deleted successfully",
        data={"task_id": task_id}
    )


@router.delete("/task/history")
def remove_all_task_history():
    clear_task_history()
    return APIResponse(
        success=True,
        message="All task history cleared successfully",
        data=None
    )