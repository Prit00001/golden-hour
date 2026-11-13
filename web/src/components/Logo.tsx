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

// The header mark is drawn, not boxed: a half sun on the horizon line, so it sits in the page like a printed masthead.
function HorizonMark() {
  return (
    <svg viewBox="0 0 32 22" className="h-[18px] w-[26px]" aria-hidden="true">
      <path d="M7 17a9 9 0 0 1 18 0z" fill="#A88748" />
      <path d="M16 2.5v3.2M7.6 6.2l2 2M24.4 6.2l-2 2" stroke="#A88748" strokeWidth="1.6" strokeLinecap="round" />
      <path d="M2 18.5h28" stroke="#25251F" strokeWidth="1.6" strokeLinecap="round" />
    </svg>
  );
}

export default function Logo() {
  return (
    <Link to="/" className="flex shrink-0 items-center gap-2.5" aria-label="Golden Hour — home">
      <HorizonMark />
      <span className="font-display text-[17px] font-medium uppercase tracking-[.14em]">Golden Hour</span>
    </Link>
  );
}
