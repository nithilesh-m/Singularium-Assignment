"""Plain Python schema helpers for tasks."""
from typing import Any, Dict, List


def normalize_task(data: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize incoming task payloads into a consistent structure."""
    dependencies = data.get("dependencies", [])
    if isinstance(dependencies, str) and dependencies.strip():
        dependencies = [d.strip() for d in dependencies.split(",")]
    elif not isinstance(dependencies, list):
        dependencies = []

    def _to_int(value: Any, default: int = 0) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    due_date = data.get("due_date")
    if due_date is not None:
        due_date = str(due_date).strip() or None

    return {
        "title": str(data.get("title", "")).strip(),
        "due_date": due_date,
        "estimated_hours": max(0, _to_int(data.get("estimated_hours", 0))),
        "importance": max(0, _to_int(data.get("importance", 0))),
        "dependencies": dependencies or [],
    }

