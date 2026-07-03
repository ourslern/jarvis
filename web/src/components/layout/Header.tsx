export function Header({ title, subtitle }: { title: string; subtitle: string }) {
  return (
    <header className="topbar">
      <div>
        <h1>{title}</h1>
        <p>{subtitle}</p>
      </div>
      <div className="status-pill">Online</div>
    </header>
  );
}
