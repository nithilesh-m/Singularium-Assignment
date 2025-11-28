import { useState } from "react";

const emptyTask = {
  title: "",
  due_date: "",
  estimated_hours: 1,
  importance: 5,
  dependencies: "",
};

export default function TaskForm({ onAdd }) {
  const [task, setTask] = useState(emptyTask);
  const [error, setError] = useState("");

  const update = (field, value) => {
    setTask((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!task.title.trim()) {
      setError("Title is required.");
      return;
    }

    const estimated = Number(task.estimated_hours);
    const importance = Number(task.importance);
    if (Number.isNaN(estimated) || estimated < 0) {
      setError("Estimated hours must be zero or greater.");
      return;
    }
    if (Number.isNaN(importance) || importance < 0 || importance > 10) {
      setError("Importance must be between 0 and 10.");
      return;
    }

    const formattedDependencies = task.dependencies
      ? task.dependencies.split(",").map((dep) => dep.trim()).filter(Boolean)
      : [];

    onAdd({
      title: task.title.trim(),
      due_date: task.due_date || null,
      estimated_hours: estimated,
      importance,
      dependencies: formattedDependencies,
    });

    setTask(emptyTask);
    setError("");
  };

  return (
    <div className="panel">
      <h2>Add Task</h2>
      <form className="form-grid" onSubmit={handleSubmit}>
        <div>
          <label htmlFor="title">Title</label>
          <input
            id="title"
            value={task.title}
            onChange={(e) => update("title", e.target.value)}
            placeholder="Research architecture"
            required
          />
        </div>
        <div>
          <label htmlFor="due_date">Due Date</label>
          <input
            id="due_date"
            type="date"
            value={task.due_date}
            onChange={(e) => update("due_date", e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="estimated_hours">Estimated Hours</label>
          <input
            id="estimated_hours"
            type="number"
            min="0"
            value={task.estimated_hours}
            onChange={(e) => update("estimated_hours", e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="importance">Importance (0-10)</label>
          <input
            id="importance"
            type="number"
            min="0"
            max="10"
            value={task.importance}
            onChange={(e) => update("importance", e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="dependencies">Dependencies (comma separated)</label>
          <input
            id="dependencies"
            value={task.dependencies}
            onChange={(e) => update("dependencies", e.target.value)}
            placeholder="Design review, API contract"
          />
        </div>
        {error && <p className="error">{error}</p>}
        <button type="submit">Add task</button>
      </form>
    </div>
  );
}

