const priorityLabel = (score) => {
  if (score >= 80) return { label: "High", className: "pill high" };
  if (score >= 50) return { label: "Medium", className: "pill medium" };
  return { label: "Low", className: "pill low" };
};

export default function TaskList({ tasks }) {
  if (!tasks.length) {
    return (
      <div className="panel">
        <h2>Analyzed Tasks</h2>
        <p>No tasks analyzed yet.</p>
      </div>
    );
  }

  return (
    <div className="panel task-list">
      <h2>Analyzed Tasks</h2>
      <table className="tasks-table">
        <thead>
          <tr>
            <th>Title</th>
            <th>Due</th>
            <th>Hours</th>
            <th>Importance</th>
            <th>Score</th>
            <th>Priority</th>
            <th>Explanation</th>
          </tr>
        </thead>
        <tbody>
          {tasks.map((task) => {
            const priority = priorityLabel(task.score);
            return (
              <tr key={`${task.title}-${task.score}-${task.explanation}`}>
                <td>{task.title}</td>
                <td>{task.due_date || "—"}</td>
                <td>{task.estimated_hours}</td>
                <td>{task.importance}</td>
                <td>{task.score}</td>
                <td>
                  <span className={priority.className}>{priority.label}</span>
                </td>
                <td>{task.explanation}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

