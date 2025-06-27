export function Card({ children, className }) {
  return <div className={`bg-zinc-800 rounded-xl p-4 shadow ${className}`}>{children}</div>;
}

export function CardContent({ children }) {
  return <div className="p-2">{children}</div>;
}