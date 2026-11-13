import { motion, useReducedMotion } from "framer-motion";
import { ArrowRight, ChevronLeft, ChevronRight } from "lucide-react";
import { useEffect, useState } from "react";
import { Link } from "react-router";
import { useI18n } from "../i18n/I18n";
import Photo from "./Photo";

const SLIDES = [  // AI-generated for Golden Hour (see web/public/images/README.md)
  { src: "/images/hero-1.jpg", alt: "A woman on a phone call at home, taking notes as she gets guidance" },
  { src: "/images/hero-2.jpg", alt: "A man on his sofa checking a payment notification on his phone" },
  { src: "/images/hero-3.jpg", alt: "A helpline worker with a headset, speaking warmly" },
  { src: "/images/hero-4.jpg", alt: "A woman on her balcony holding her phone, relieved after getting help" },
];

// One photograph at a time, in the page's own width, crossfading: no cut-off neighbours at the edges.
export default function ImageCarousel() {
  const { t } = useI18n();
  const [i, setI] = useState(0);
  const [paused, setPaused] = useState(false);
  const still = useReducedMotion();
  const n = SLIDES.length, go = (d: number) => setI(x => (x + d + n) % n);
  useEffect(() => {
    if (paused || still) return;
    const id = setInterval(() => go(1), 6500);
    return () => clearInterval(id);
  }, [paused, still]);

  return (
    <div className="mx-auto max-w-[1280px] px-5 md:px-8" aria-roledescription="carousel"
      onMouseEnter={() => setPaused(true)} onMouseLeave={() => setPaused(false)}>
      <motion.div className="relative h-[clamp(320px,min(44vw,48vh),580px)] touch-pan-y overflow-hidden rounded-[10px] bg-cream"
        drag="x" dragConstraints={{ left: 0, right: 0 }} dragElastic={.08}
        onDragEnd={(_, d) => Math.abs(d.offset.x) > 60 && go(d.offset.x < 0 ? 1 : -1)}>
        {SLIDES.map((s, k) => (
          <motion.div key={s.src} className="absolute inset-0" aria-hidden={k !== i} initial={false}
            animate={{ opacity: k === i ? 1 : 0 }} transition={{ duration: 1.1, ease: [.4, 0, .2, 1] }}>
            <Photo src={s.src} alt={s.alt} tone={k} className="size-full" />
          </motion.div>
        ))}
        <div className="absolute bottom-4 left-4 right-4 rounded-[8px] border border-line bg-paper p-5 md:bottom-7 md:left-7 md:right-auto md:w-[360px]">
          <p className="font-display text-[21px] leading-tight">{t("float_t")}</p>
          <p className="mt-1 text-[14px] text-stone">{t("float_p")}</p>
          <Link to="/assistant" className="btn-green mt-4 w-full sm:w-auto">{t("start")}<ArrowRight className="size-4" /></Link>
        </div>
      </motion.div>
      <div className="mt-4 flex items-center justify-between gap-4">
        <div className="flex flex-1 gap-1.5" aria-hidden="true">
          {SLIDES.map((_, k) => <span key={k} className={`h-px flex-1 max-w-16 transition-colors duration-500 ${k === i ? "bg-ink" : "bg-ink/15"}`} />)}
        </div>
        <span className="font-display text-[15px] tabular-nums text-stone" aria-live="polite">{String(i + 1).padStart(2, "0")} / {String(n).padStart(2, "0")}</span>
        <div className="flex gap-1.5">
          <button className="grid size-9 place-items-center rounded-[6px] border border-line transition-colors hover:border-ink/40 hover:bg-ink/[.03]" onClick={() => go(-1)} aria-label={t("prev")}><ChevronLeft className="size-[18px]" /></button>
          <button className="grid size-9 place-items-center rounded-[6px] border border-line transition-colors hover:border-ink/40 hover:bg-ink/[.03]" onClick={() => go(1)} aria-label={t("next")}><ChevronRight className="size-[18px]" /></button>
        </div>
      </div>
    </div>
  );
}
