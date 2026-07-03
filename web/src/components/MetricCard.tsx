export function MetricCard({ title, value, subtitle, icon }: any) {
  return (
    <div className="card metric-card">
      <div className="metric-header">
        <span>{icon}</span>
        <span>{title}</span>
      </div>
      <div className="metric-value">{value}</div>
      <div className="metric-subtitle">{subtitle}</div>
    </div>
  );
}
