export function ContainerList({ containers = [] }: any) {
  return (
    <div className="list">
      {containers.map((c: any) => (
        <div key={c.name} className="row">
          <span>{c.status === "running" ? "🟢" : "⚪"} {c.name}</span>
          <span>{c.status}</span>
        </div>
      ))}
    </div>
  );
}
