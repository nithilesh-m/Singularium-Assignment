import { useState } from "react";
import ReactDOM from "react-dom/client";
import "./styles.css";
import TaskForm from "./components/TaskForm.jsx";
import BulkJSON from "./components/BulkJSON.jsx";
import StrategySelector from "./components/StrategySelector.jsx";
import TaskList from "./components/TaskList.jsx";
import { analyzeTasks, getSuggestions } from "./api.js";

export default function App() {
  const [draftTasks, setDraftTasks] = useState([]);
  const [strategy, setStrategy] = useState("smart_balance");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const addTask = (task) => {
    setDraftTasks((prev) => [...prev, task]);
  };

  const addManyTasks = (bulkTasks) => {
    setDraftTasks((prev) => [...prev, ...bulkTasks]);
  };

  const handleAnalyze = async () => {
    if (!draftTasks.length) {
      setError("Add at least one task before analyzing.");
      return;
    }

    setLoading(true);
    setError("");
    setSuccess("");
    try {
      const response = await analyzeTasks(draftTasks, strategy);
      setResults(response.results);
      setSuccess(`Analyzed ${response.results.length} tasks.`);
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSuggest = async () => {
    setLoading(true);
    setError("");
    setSuccess("");
    try {
      const response = await getSuggestions();
      setResults(response.results);
      setSuccess("Loaded saved suggestions.");
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setLoading(false);
    }
  };

  const clearDrafts = () => setDraftTasks([]);

  return (
    <div className="shell">
      <h1>Smart Task Analyzer</h1>
      <p>
        Provide tasks individually or via JSON, pick a strategy, and let the
        scoring engine rank work for you.
      </p>

      <TaskForm onAdd={addTask} />
      <BulkJSON onAddMany={addManyTasks} />
      <StrategySelector value={strategy} onChange={setStrategy} />

      <div className="panel">
        <h2>Queued Tasks ({draftTasks.length})</h2>
        {draftTasks.length === 0 ? (
          <p>No tasks queued yet.</p>
        ) : (
          <ul>
            {draftTasks.map((task, index) => (
              <li key={`${task.title}-${index}`}>
                <strong>{task.title}</strong> · due {task.due_date || "unscheduled"} ·{" "}
                {task.estimated_hours}h · importance {task.importance}
              </li>
            ))}
          </ul>
        )}
        <div className="actions">
          <button type="button" onClick={handleAnalyze} disabled={loading}>
            {loading ? "Analyzing..." : "Analyze Tasks"}
          </button>
          <button type="button" onClick={handleSuggest} disabled={loading}>
            {loading ? "Fetching..." : "Get Suggestions"}
          </button>
          <button type="button" onClick={clearDrafts} disabled={!draftTasks.length}>
            Clear Drafts
          </button>
        </div>
        {error && <p className="error">{error}</p>}
        {success && <p className="success">{success}</p>}
      </div>

      <TaskList tasks={results} />
    </div>
  );
}

const container = document.getElementById("root");
if (container && !container.dataset.mounted) {
  container.dataset.mounted = "true";
  ReactDOM.createRoot(container).render(<App />);
}

