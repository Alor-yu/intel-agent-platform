import os
import sqlite3
import json
from typing import Optional, List, Dict, Any

DB_PATH = "db/app.db"


def get_conn():
    os.makedirs("db", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS task_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id TEXT NOT NULL,
        user_query TEXT NOT NULL,
        parsed_task TEXT,
        execution_plan TEXT,
        analysis_result TEXT,
        report_result TEXT,
        logs TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_task_history(
    task_id: str,
    user_query: str,
    parsed_task: Dict[str, Any],
    execution_plan: List[str],
    analysis_result: Dict[str, Any],
    report_result: Dict[str, Any],
    logs: List[str]
):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO task_history (
        task_id, user_query, parsed_task, execution_plan,
        analysis_result, report_result, logs
    ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        task_id,
        user_query,
        json.dumps(parsed_task, ensure_ascii=False),
        json.dumps(execution_plan, ensure_ascii=False),
        json.dumps(analysis_result, ensure_ascii=False),
        json.dumps(report_result, ensure_ascii=False),
        json.dumps(logs, ensure_ascii=False),
    ))

    conn.commit()
    conn.close()


def get_task_history(limit: int = 20) -> List[Dict[str, Any]]:
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM task_history
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    results = []
    for row in rows:
        results.append({
            "id": row["id"],
            "task_id": row["task_id"],
            "user_query": row["user_query"],
            "parsed_task": json.loads(row["parsed_task"]) if row["parsed_task"] else {},
            "execution_plan": json.loads(row["execution_plan"]) if row["execution_plan"] else [],
            "analysis_result": json.loads(row["analysis_result"]) if row["analysis_result"] else {},
            "report_result": json.loads(row["report_result"]) if row["report_result"] else {},
            "logs": json.loads(row["logs"]) if row["logs"] else [],
            "created_at": row["created_at"]
        })

    return results


def get_task_by_id(task_id: str) -> Optional[Dict[str, Any]]:
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM task_history
    WHERE task_id = ?
    LIMIT 1
    """, (task_id,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "id": row["id"],
        "task_id": row["task_id"],
        "user_query": row["user_query"],
        "parsed_task": json.loads(row["parsed_task"]) if row["parsed_task"] else {},
        "execution_plan": json.loads(row["execution_plan"]) if row["execution_plan"] else [],
        "analysis_result": json.loads(row["analysis_result"]) if row["analysis_result"] else {},
        "report_result": json.loads(row["report_result"]) if row["report_result"] else {},
        "logs": json.loads(row["logs"]) if row["logs"] else [],
        "created_at": row["created_at"]
    }
def delete_task_by_id(task_id: str) -> bool:
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM task_history WHERE task_id = ?", (task_id,))
    affected = cursor.rowcount

    conn.commit()
    conn.close()

    return affected > 0


def clear_task_history() -> None:
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM task_history")

    conn.commit()
    conn.close()