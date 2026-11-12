import { Link } from "react-router";

// A sun on the horizon: the first hour after fraud, and the hope in it.
export function SunMark({ className = "size-8" }: { className?: string }) {
  return (
    <svg viewBox="0 0 32 32" className={className} aria-hidden="true">
      <circle cx="16" cy="16" r="15" fill="#25251F" />
      <path d="M8 20a8 8 0 0 1 16 0z" fill="#B99559" />
      <path d="M16 7v2.5M9.6 9.6l1.8 1.8M22.4 9.6l-1.8 1.8" stroke="#B99559" strokeWidth="1.6" strokeLinecap="round" />
      <path d="M6 22.5h20" stroke="#FAF7F0" strokeWidth="1.8" strokeLinecap="round" />
    </svg>
  );
}

export default function Logo() {
  return (
    <Link to="/" className="flex items-center gap-2.5 shrink-0" aria-label="Golden Hour — home">
      <SunMark />
      <span className="font-display text-[15px] font-extrabold tracking-[.18em]">GOLDEN HOUR</span>
    </Link>
  );
}
