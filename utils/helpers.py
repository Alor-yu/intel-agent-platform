import uuid
from datetime import datetime
import json


def generate_task_id() -> str:
    return str(uuid.uuid4())


def get_current_time() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def safe_json_loads(text: str):
    try:
        return json.loads(text)
    except Exception:
        return None