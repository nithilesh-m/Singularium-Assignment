"""Scoring logic for the Smart Task Analyzer."""
from __future__ import annotations

from datetime import date, datetime
from typing import Dict, Iterable, List, Set


def _parse_due_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def _dependency_graph(tasks: Iterable[Dict]) -> Dict[str, List[str]]:
    return {task["title"]: task.get("dependencies", []) for task in tasks}


def _detect_cycles(graph: Dict[str, List[str]]) -> Set[str]:
    """Return a set of node titles that participate in at least one cycle."""
    visited: Set[str] = set()
    stack: Set[str] = set()
    cyclic: Set[str] = set()

    def visit(node: str) -> None:
        if node in stack:
            cyclic.update(stack)
            return
        if node in visited:
            return
        visited.add(node)
        stack.add(node)
        for neighbor in graph.get(node, []):
            if neighbor in graph:  # ignore unknown references
                visit(neighbor)
        stack.remove(node)

    for node in graph:
        if node not in visited:
            visit(node)
    return cyclic


def _dependents_count(tasks: Iterable[Dict]) -> Dict[str, int]:
    reversed_map: Dict[str, Set[str]] = {}
    for task in tasks:
        title = task["title"]
        for dep in task.get("dependencies", []):
            reversed_map.setdefault(dep, set()).add(title)
    return {title: len(dependents) for title, dependents in reversed_map.items()}


def _urgency_score(due: date | None, today: date) -> float:
    if not due:
        return 0.35  # unknown deadline gets moderate priority
    days_out = (due - today).days
    if days_out < 0:
        return 1.0 + min(abs(days_out) / 14, 0.5)  # overdue boost
    if days_out == 0:
        return 1.0
    window = 30
    return max(0.2, 1 - (days_out / window))


def _effort_score(hours: int) -> float:
    if hours <= 2:
        return 1.0
    if hours <= 6:
        return 0.8
    if hours <= 12:
        return 0.6
    return 0.4


def _dependency_score(title: str, dependents_map: Dict[str, int]) -> float:
    dependents = dependents_map.get(title, 0)
    if dependents == 0:
        return 0.3
    if dependents == 1:
        return 0.6
    return min(1.0, 0.6 + (dependents - 1) * 0.15)


def score_task(task: Dict, dependents_map: Dict[str, int], cyclic: Set[str]) -> Dict:
    today = date.today()
    due = _parse_due_date(task.get("due_date"))

    urgency = _urgency_score(due, today)
    importance = task.get("importance", 0) / 10
    effort = _effort_score(task.get("estimated_hours", 0))
    dependency = _dependency_score(task["title"], dependents_map)
    penalty = 0.3 if task["title"] in cyclic else 0.0

    composite = (
        urgency * 0.35 + importance * 0.35 + effort * 0.15 + dependency * 0.15
    )
    final_score = max(composite - penalty, 0) * 100

    explanation_parts = [
        f"Urgency={urgency:.2f}",
        f"Importance={importance:.2f}",
        f"EffortFit={effort:.2f}",
        f"DependencyImpact={dependency:.2f}",
    ]
    if penalty:
        explanation_parts.append("CyclePenalty=" + f"{penalty:.2f}")

    return {
        **task,
        "score": round(final_score, 2),
        "explanation": ", ".join(explanation_parts),
    }


def sort_tasks(scored_tasks: List[Dict], strategy: str) -> List[Dict]:
    def due_key(task: Dict) -> tuple:
        due = _parse_due_date(task.get("due_date"))
        return (due is None, due or date.max)

    if strategy == "fastest_wins":
        return sorted(
            scored_tasks,
            key=lambda t: (t.get("estimated_hours", 0), -t["score"]),
        )
    if strategy == "high_impact":
        return sorted(
            scored_tasks,
            key=lambda t: (-t.get("importance", 0), -t["score"]),
        )
    if strategy == "deadline_driven":
        return sorted(scored_tasks, key=lambda t: due_key(t))
    # smart_balance default
    return sorted(scored_tasks, key=lambda t: -t["score"])


def analyze_tasks(tasks: List[Dict], strategy: str) -> List[Dict]:
    graph = _dependency_graph(tasks)
    cyclic_nodes = _detect_cycles(graph)
    dependents_map = _dependents_count(tasks)
    scored = [score_task(task, dependents_map, cyclic_nodes) for task in tasks]
    return sort_tasks(scored, strategy)

