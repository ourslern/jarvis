export function Card({ title, children, className = "" }: any) {
  return (
    <div className={`card ${className}`}>
      {title && <h2>{title}</h2>}
      {children}
    </div>
  );
}
