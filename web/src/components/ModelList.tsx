export function ModelList({ models = [] }: any) {
  return (
    <div className="list">
      {models.map((m: any) => (
        <div key={m.name} className="row">
          <span>{m.name}</span>
          <span>{m.size_gb} GB</span>
        </div>
      ))}
    </div>
  );
}
