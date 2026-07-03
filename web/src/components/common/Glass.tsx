import type { ReactNode } from "react";

export function Glass({
  children,
  className = "",
}: {
  children: ReactNode;
  className?: string;
}) {
  return (
    <div
      className={`rounded-3xl border border-white/10 bg-white/5 p-6 shadow-2xl backdrop-blur-xl ${className}`}
    >
      {children}
    </div>
  );
}
