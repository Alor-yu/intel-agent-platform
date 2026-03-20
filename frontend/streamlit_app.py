import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

import streamlit as st
import requests
import pandas as pd
from rag.ingestion import (
    extract_text_from_upload,
    append_to_knowledge_base,
    read_knowledge_base,
    clear_knowledge_base,
    reset_knowledge_base,
)

API_BASE_URL = "http://127.0.0.1:8000/api"

st.set_page_config(
    page_title="企业情报分析 Agent 工作流平台",
    layout="wide"
)

if "user_query" not in st.session_state:
    st.session_state.user_query = "分析过去7天Perplexity和Kimi的产品动态，输出竞品日报"

if "last_result" not in st.session_state:
    st.session_state.last_result = None


def fetch_task_history():
    try:
        response = requests.get(f"{API_BASE_URL}/task/history", timeout=30)
        response.raise_for_status()
        result = response.json()
        return result.get("data", {}).get("items", [])
    except Exception:
        return []


def fetch_task_detail(task_id: str):
    try:
        response = requests.get(f"{API_BASE_URL}/task/history/{task_id}", timeout=30)
        response.raise_for_status()
        result = response.json()
        if result.get("success"):
            return result.get("data")
        return None
    except Exception:
        return None


def build_result_from_history(detail: dict) -> dict:
    if not detail:
        return None

    return {
        "success": True,
        "data": {
            "task_id": detail.get("task_id"),
            "status": "success",
            "parsed_task": detail.get("parsed_task", {}),
            "execution_plan": detail.get("execution_plan", []),
            "analysis_result": detail.get("analysis_result", {}),
            "report_result": detail.get("report_result", {}),
            "logs": detail.get("logs", []),
            "error_message": None
        }
    }


st.title("企业情报分析 Agent 工作流平台")
st.caption("面向竞品分析与行业研究的智能工作流系统：自动完成任务解析、执行规划、信息检索、分析与报告生成。")

with st.sidebar:
    st.header("任务历史")

    clear_all = st.button("清空全部历史", use_container_width=True)

    if clear_all:
        try:
            response = requests.delete(f"{API_BASE_URL}/task/history", timeout=30)
            response.raise_for_status()
            st.session_state.last_result = None
            st.success("全部历史已清空。")
            st.rerun()
        except Exception as e:
            st.error(f"清空历史失败：{e}")

    history_items = fetch_task_history()

    if history_items:
        for item in history_items[:10]:
            st.markdown(f"**时间：** {item['created_at']}")
            st.markdown(f"**任务：** {item['user_query'][:40]}{'...' if len(item['user_query']) > 40 else ''}")
            st.caption(f"task_id: {item['task_id']}")

            col_view, col_delete = st.columns(2)

            with col_view:
                if st.button(f"查看 {item['id']}", key=f"history_view_{item['task_id']}", use_container_width=True):
                    detail = fetch_task_detail(item["task_id"])
                    if detail:
                        st.session_state.last_result = build_result_from_history(detail)
                        st.session_state.user_query = detail.get("user_query", st.session_state.user_query)
                        st.rerun()
                    else:
                        st.warning("历史任务详情加载失败。")

            with col_delete:
                if st.button(f"删除 {item['id']}", key=f"history_delete_{item['task_id']}", use_container_width=True):
                    try:
                        response = requests.delete(f"{API_BASE_URL}/task/history/{item['task_id']}", timeout=30)
                        response.raise_for_status()
                        st.success("历史任务已删除。")
                        st.rerun()
                    except Exception as e:
                        st.error(f"删除历史失败：{e}")

            st.divider()
    else:
        st.info("暂无任务历史")
        
with st.container():
    st.info("建议先启动后端服务：uvicorn app.main:app --reload")

left_col, right_col = st.columns([1, 2])

with left_col:
    st.subheader("任务输入")

    st.markdown("**快捷示例**")

    if st.button("示例 1：AI 搜索竞品日报", use_container_width=True):
        st.session_state.user_query = "分析过去7天Perplexity和Kimi的产品动态，输出竞品日报"

    if st.button("示例 2：长文本能力竞品分析", use_container_width=True):
        st.session_state.user_query = "分析过去30天Kimi和Claude在长文本处理方面的产品动态，输出竞品分析报告"

    if st.button("示例 3：通用行业研究", use_container_width=True):
        st.session_state.user_query = "分析过去7天AI搜索赛道的发展动态，输出行业观察报告"

    st.session_state.user_query = st.text_area(
        "请输入分析任务",
        value=st.session_state.user_query,
        height=180
    )

    run_button = st.button("开始执行任务", type="primary", use_container_width=True)
    clear_result_button = st.button("清空结果", use_container_width=True)

    if clear_result_button:
        st.session_state.last_result = None

    st.markdown("---")
    st.subheader("知识库上传")
    uploaded_file = st.file_uploader(
        "上传 txt / md / pdf 文件",
        type=["txt", "md", "pdf"]
    )

    if uploaded_file is not None:
        if st.button("追加到知识库", use_container_width=True):
            try:
                file_bytes = uploaded_file.read()
                extracted_text = extract_text_from_upload(uploaded_file.name, file_bytes)
                save_path = append_to_knowledge_base(uploaded_file.name, extracted_text)
                st.success(f"文件已写入知识库：{save_path}")
            except Exception as e:
                st.error(f"知识库上传失败：{e}")

    st.markdown("---")
    st.subheader("知识库管理")

    manage_col1, manage_col2 = st.columns(2)

    with manage_col1:
        if st.button("预览知识库", use_container_width=True):
            try:
                kb_text = read_knowledge_base()
                st.session_state["kb_preview"] = kb_text
            except Exception as e:
                st.error(f"读取知识库失败：{e}")

    with manage_col2:
        if st.button("恢复默认知识库", use_container_width=True):
            try:
                reset_path = reset_knowledge_base()
                st.success(f"知识库已恢复默认内容：{reset_path}")
                st.session_state["kb_preview"] = read_knowledge_base()
            except Exception as e:
                st.error(f"重置知识库失败：{e}")

    if st.button("清空知识库", use_container_width=True):
        try:
            clear_path = clear_knowledge_base()
            st.warning(f"知识库已清空：{clear_path}")
            st.session_state["kb_preview"] = ""
        except Exception as e:
            st.error(f"清空知识库失败：{e}")

    kb_preview = st.session_state.get("kb_preview", "")
    if kb_preview:
        with st.expander("查看当前知识库内容", expanded=False):
            st.text_area("知识库预览", value=kb_preview, height=250)

with right_col:
    st.subheader("执行结果")

if run_button:
    if not st.session_state.user_query.strip():
        st.session_state.last_result = {
            "success": False,
            "data": {
                "status": "failed",
                "error_message": "请输入任务内容后再执行。"
            }
        }
    else:
        with right_col:
            with st.spinner("任务执行中，请稍候..."):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/task/run",
                        json={"user_query": st.session_state.user_query},
                        timeout=60
                    )
                    response.raise_for_status()
                    result = response.json()
                    st.session_state.last_result = result

                except requests.exceptions.ConnectionError:
                    st.session_state.last_result = {
                        "success": False,
                        "data": {
                            "status": "failed",
                            "error_message": "无法连接后端接口。请确认 FastAPI 服务已启动：uvicorn app.main:app --reload"
                        }
                    }
                except requests.exceptions.Timeout:
                    st.session_state.last_result = {
                        "success": False,
                        "data": {
                            "status": "failed",
                            "error_message": "接口请求超时。"
                        }
                    }
                except requests.exceptions.RequestException as e:
                    st.session_state.last_result = {
                        "success": False,
                        "data": {
                            "status": "failed",
                            "error_message": f"请求失败：{e}"
                        }
                    }
                except Exception as e:
                    st.session_state.last_result = {
                        "success": False,
                        "data": {
                            "status": "failed",
                            "error_message": f"发生未知错误：{e}"
                        }
                    }

with right_col:
    cached_result = st.session_state.get("last_result")

    if cached_result:
        if not cached_result.get("success"):
            data = cached_result.get("data", {})
            st.error("任务执行失败。")
            st.json({
                "status": data.get("status", "failed"),
                "error_message": data.get("error_message")
            })
        else:
            data = cached_result.get("data", {})
            analysis_result = data.get("analysis_result", {})
            report_result = data.get("report_result", {})

            task_status = data.get("status", "success")
            error_message = data.get("error_message")

            st.markdown("### 最近一次执行结果")

            if task_status == "success":
                st.success("任务执行完成。")
            elif task_status == "partial_success":
                st.warning("任务部分完成，部分步骤执行失败。")
            else:
                st.error("任务执行失败。")

            st.markdown("### 执行状态")
            st.json({
                "status": task_status,
                "error_message": error_message
            })

            if error_message:
                st.error(f"错误信息：{error_message}")

            top_col1, top_col2 = st.columns(2)

            with top_col1:
                st.markdown("### 任务解析结果")
                st.json(data.get("parsed_task", {}))

            with top_col2:
                st.markdown("### 执行计划")
                st.json(data.get("execution_plan", []))

            st.markdown("### 分析摘要")
            summary = analysis_result.get("summary", "")
            if summary:
                st.write(summary)
            else:
                st.info("暂无分析摘要。")

            st.markdown("### 关键动态")
            key_updates = analysis_result.get("key_updates", [])
            if key_updates:
                for idx, item in enumerate(key_updates, start=1):
                    st.markdown(f"{idx}. {item}")
            else:
                st.info("暂无关键动态。")

            st.markdown("### 竞品对比表")
            comparison_rows = report_result.get("comparison_rows", [])
            if comparison_rows:
                df = pd.DataFrame(comparison_rows)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("暂无竞品对比表。")

            st.markdown("### 最终 Markdown 报告")
            report_markdown = report_result.get("report_markdown", "")
            if report_markdown:
                with st.expander("展开查看完整报告", expanded=True):
                    st.markdown(report_markdown)
            else:
                st.info("暂无报告内容。")

            st.markdown("### 执行日志")
            logs = data.get("logs", [])
            if logs:
                with st.expander("展开查看执行日志", expanded=False):
                    for log in logs:
                        st.code(log)
            else:
                st.info("暂无日志信息。")

            st.markdown("### 报告文件")
            saved_path = report_result.get("saved_path", "")
            if saved_path:
                st.success(f"报告已保存到：{saved_path}")
                try:
                    with open(saved_path, "r", encoding="utf-8") as f:
                        report_content = f.read()

                    st.download_button(
                        label="下载 Markdown 报告",
                        data=report_content,
                        file_name=saved_path.split("\\")[-1].split("/")[-1],
                        mime="text/markdown",
                        use_container_width=True
                    )
                except Exception as e:
                    st.warning(f"报告文件读取失败：{e}")
            else:
                st.info("暂无保存文件路径。")
    else:
        st.info("暂无执行结果，请先在左侧提交任务。")