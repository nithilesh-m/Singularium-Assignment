const STRATEGIES = [
  { value: "smart_balance", label: "Smart Balance" },
  { value: "fastest_wins", label: "Fastest Wins" },
  { value: "high_impact", label: "High Impact" },
  { value: "deadline_driven", label: "Deadline Driven" },
];

export default function StrategySelector({ value, onChange }) {
  return (
    <div className="panel">
      <h2>Scoring Strategy</h2>
      <label htmlFor="strategy">Select strategy</label>
      <select
        id="strategy"
        value={value}
        onChange={(event) => onChange(event.target.value)}
      >
        {STRATEGIES.map((strategy) => (
          <option key={strategy.value} value={strategy.value}>
            {strategy.label}
          </option>
        ))}
      </select>
    </div>
  );
}

