from typing import TypedDict, List, Dict, Any


class AgentState(TypedDict):
    user_query: str
    parsed_task: Dict[str, Any]
    plan: List[str]
    web_data: List[Dict[str, Any]]
    kb_data: str
    analysis_result: str
    comparison_result: str
    final_report: str
    logs: List[str]