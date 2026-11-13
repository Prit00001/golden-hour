import { useState } from "react";
import { SunMark } from "./Logo";

const TONES = ["from-[#d9c6a3] to-[#efe4d0]", "from-[#c7d6c9] to-[#e9efe6]", "from-[#e3cfb7] to-[#f4ece0]",
  "from-[#cdbfa8] to-[#ece4d6]", "from-[#d4dccf] to-[#f1ede3]"];

// Your photo if the file is in web/public/images, otherwise a warm placeholder in the same frame.
// priority: the hero photo, loaded at once; everything else waits until it scrolls near the screen.
export default function Photo({ src, alt, tone = 0, className = "", priority }: { src: string; alt: string; tone?: number; className?: string; priority?: "high" | "low" }) {
  const [missing, setMissing] = useState(false);
  if (missing) return (
    <div role="img" aria-label={alt} className={`grid place-items-center bg-gradient-to-br ${TONES[tone % TONES.length]} ${className}`}>
      <SunMark className="size-16 opacity-25" />
    </div>
  );
  return <img src={src} alt={alt} onError={() => setMissing(true)} loading={priority ? "eager" : "lazy"} fetchPriority={priority ?? "auto"} decoding="async" className={`object-cover ${className}`} />;
}
