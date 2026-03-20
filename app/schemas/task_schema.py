from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class TaskRequest(BaseModel):
    user_query: str = Field(..., description="用户输入的分析任务")


class ParsedTask(BaseModel):
    task_type: str = Field(default="competitive_analysis", description="任务类型")
    companies: List[str] = Field(default_factory=list, description="涉及的公司/产品")
    time_range: str = Field(default="7d", description="时间范围，例如 7d / 30d")
    output_format: str = Field(default="report", description="输出格式，例如 report / markdown")
    need_comparison: bool = Field(default=True, description="是否需要竞品对比")


class WebSearchResult(BaseModel):
    title: str = Field(..., description="搜索结果标题")
    content: str = Field(..., description="搜索结果摘要内容")
    url: Optional[str] = Field(default=None, description="来源链接")
    source: Optional[str] = Field(default="mock", description="数据来源")


class TaskResult(BaseModel):
    summary: str = Field(default="", description="摘要结论")
    key_updates: List[str] = Field(default_factory=list, description="关键动态")
    comparison_table: Optional[str] = Field(default=None, description="竞品对比表")
    report_markdown: str = Field(default="", description="最终 markdown 报告")


class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None

class TaskExecutionResult(BaseModel):
    task_id: str
    status: str = Field(default="success", description="任务状态：success / failed / partial_success")
    parsed_task: Dict[str, Any] = Field(default_factory=dict)
    execution_plan: List[str] = Field(default_factory=list)
    web_results: List[Dict[str, Any]] = Field(default_factory=list)
    kb_result: str = Field(default="")
    analysis_result: Dict[str, Any] = Field(default_factory=dict)
    report_result: Dict[str, Any] = Field(default_factory=dict)
    logs: List[str] = Field(default_factory=list)
    error_message: Optional[str] = Field(default=None, description="错误信息")