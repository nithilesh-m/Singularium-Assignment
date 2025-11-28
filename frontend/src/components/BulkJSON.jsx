import { useState } from "react";

export default function BulkJSON({ onAddMany }) {
  const [rawJson, setRawJson] = useState("");
  const [error, setError] = useState("");

  const handleAdd = () => {
    try {
      const parsed = JSON.parse(rawJson || "[]");
      if (!Array.isArray(parsed)) {
        setError("JSON must be an array of tasks.");
        return;
      }
      if (!parsed.length) {
        setError("No tasks found in JSON array.");
        return;
      }
      onAddMany(parsed);
      setRawJson("");
      setError("");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="panel">
      <h2>Bulk JSON Import</h2>
      <label htmlFor="bulk-json">Paste JSON array</label>
      <textarea
        id="bulk-json"
        value={rawJson}
        onChange={(e) => setRawJson(e.target.value)}
        placeholder='[{"title": "Prepare deck", "estimated_hours": 2}]'
      />
      {error && <p className="error">{error}</p>}
      <button type="button" onClick={handleAdd}>
        Add bulk tasks
      </button>
    </div>
  );
}

