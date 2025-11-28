"""REST Framework serializers for the Smart Task Analyzer."""
from datetime import datetime
from typing import Any, Dict, List

from rest_framework import serializers

from .schema import normalize_task


ALLOWED_STRATEGIES = {
    "fastest_wins",
    "high_impact",
    "deadline_driven",
    "smart_balance",
}


class TaskSerializer(serializers.Serializer):
    """Serializer that validates and normalizes a single task payload."""

    def to_internal_value(self, data: Any) -> Dict[str, Any]:
        if not isinstance(data, dict):
            raise serializers.ValidationError("Each task must be an object.")

        normalized = normalize_task(data)

        if not normalized["title"]:
            raise serializers.ValidationError("Task title is required.")

        importance = normalized["importance"]
        if importance < 0 or importance > 10:
            raise serializers.ValidationError("Importance must be between 0 and 10.")

        estimated_hours = normalized["estimated_hours"]
        if estimated_hours < 0:
            raise serializers.ValidationError("Estimated hours must be ≥ 0.")

        if normalized["due_date"]:
            try:
                datetime.strptime(normalized["due_date"], "%Y-%m-%d")
            except ValueError as exc:
                raise serializers.ValidationError(
                    "due_date must be in YYYY-MM-DD format."
                ) from exc

        dependencies = normalized["dependencies"]
        if not isinstance(dependencies, list):
            raise serializers.ValidationError("Dependencies must be a list.")
        for dep in dependencies:
            if not isinstance(dep, str):
                raise serializers.ValidationError("Each dependency must be a string.")

        return normalized


class AnalyzeRequestSerializer(serializers.Serializer):
    """Serializer for the analyze endpoint payload."""

    def to_internal_value(self, data: Any) -> Dict[str, Any]:
        if not isinstance(data, dict):
            raise serializers.ValidationError("Payload must be a JSON object.")

        tasks = data.get("tasks")
        if not isinstance(tasks, list) or not tasks:
            raise serializers.ValidationError("`tasks` must be a non-empty list.")

        normalized_tasks: List[Dict[str, Any]] = []
        for task_data in tasks:
            serializer = TaskSerializer(data=task_data)
            serializer.is_valid(raise_exception=True)
            normalized_tasks.append(serializer.validated_data)

        strategy = data.get("strategy", "smart_balance")
        if strategy not in ALLOWED_STRATEGIES:
            raise serializers.ValidationError(
                f"strategy must be one of {sorted(ALLOWED_STRATEGIES)}"
            )

        return {"tasks": normalized_tasks, "strategy": strategy}

