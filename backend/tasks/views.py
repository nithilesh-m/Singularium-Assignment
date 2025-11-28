"""API views for the Smart Task Analyzer."""
from datetime import datetime
from typing import Dict, List

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from task_analyzer.mongodb import db
from .scoring import analyze_tasks
from .serializers import AnalyzeRequestSerializer


class AnalyzeTasksView(APIView):
    """Accepts ad-hoc tasks and returns prioritized scoring."""

    def post(self, request):
        serializer = AnalyzeRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data

        scored_tasks = analyze_tasks(validated["tasks"], validated["strategy"])
        self._persist_tasks(scored_tasks, validated["strategy"])

        return Response(
            {
                "strategy": validated["strategy"],
                "results": scored_tasks,
            },
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def _persist_tasks(scored_tasks: List[Dict], strategy: str) -> None:
        for task in scored_tasks:
            record = {
                "title": task.get("title"),
                "due_date": task.get("due_date"),
                "estimated_hours": task.get("estimated_hours"),
                "importance": task.get("importance"),
                "dependencies": task.get("dependencies", []),
                "score": task.get("score"),
                "explanation": task.get("explanation"),
                "strategy": strategy,
                "created_at": datetime.utcnow(),
            }
            db.tasks.insert_one(record)


class SuggestTasksView(APIView):
    """Returns the top ranked tasks that were previously saved."""

    def get(self, request):
        stored = list(db.tasks.find().sort("created_at", -1).limit(200))
        base_tasks: List[Dict] = []
        for doc in stored:
            base_tasks.append(
                {
                    "title": doc.get("title", ""),
                    "due_date": doc.get("due_date"),
                    "estimated_hours": doc.get("estimated_hours", 0),
                    "importance": doc.get("importance", 0),
                    "dependencies": doc.get("dependencies", []),
                    "source_id": str(doc.get("_id")),
                }
            )

        if not base_tasks:
            return Response({"results": []}, status=status.HTTP_200_OK)

        scored = analyze_tasks(base_tasks, "smart_balance")[:3]
        return Response({"results": scored}, status=status.HTTP_200_OK)

