import { motion, useReducedMotion } from "framer-motion";
import { ArrowRight, ChevronLeft, ChevronRight } from "lucide-react";
import { useEffect, useState } from "react";
import { Link } from "react-router";
import { useI18n } from "../i18n/I18n";
import Photo from "./Photo";

const SLIDES = [
  { src: "/images/hero-1.jpg", alt: "A person getting help on a phone call" },
  { src: "/images/hero-2.jpg", alt: "Someone checking their banking app on a smartphone" },
  { src: "/images/hero-3.jpg", alt: "A calm conversation with a support advisor" },
  { src: "/images/hero-4.jpg", alt: "Family members reviewing a message together" },
  { src: "/images/hero-5.jpg", alt: "A person relieved after getting the right help" },
];

// One full-colour card in the middle, its neighbours peeking in at the sides in greyscale.
export default function ImageCarousel() {
  const { t } = useI18n();
  const [i, setI] = useState(0);
  const [paused, setPaused] = useState(false);
  const still = useReducedMotion();
  const n = SLIDES.length, go = (d: number) => setI(x => (x + d + n) % n);
  useEffect(() => {
    if (paused || still) return;
    const id = setInterval(() => go(1), 6000);
    return () => clearInterval(id);
  }, [paused, still]);

  return (
    <div className="relative" onMouseEnter={() => setPaused(true)} onMouseLeave={() => setPaused(false)}
      aria-roledescription="carousel">
      <div className="relative h-[clamp(360px,46vw,600px)] overflow-hidden">
        {SLIDES.map((s, k) => {
          let off = k - i;
          if (off > n / 2) off -= n;
          if (off < -n / 2) off += n;
          const centre = off === 0;
          return (
            <motion.div key={s.src} className="absolute inset-y-0 left-1/2 w-[84%] md:w-[60%]"
              aria-hidden={!centre}
              initial={false}
              animate={{ x: `calc(-50% + ${off * 104}%)`, scale: centre ? 1 : .86, opacity: Math.abs(off) > 1 ? 0 : 1,
                filter: centre ? "grayscale(0)" : "grayscale(1)" }}
              transition={{ duration: .8, ease: [.22, 1, .36, 1] }}
              drag={centre ? "x" : false} dragConstraints={{ left: 0, right: 0 }} dragElastic={.2}
              onDragEnd={(_, d) => Math.abs(d.offset.x) > 60 && go(d.offset.x < 0 ? 1 : -1)}>
              <Photo src={s.src} alt={s.alt} tone={k} className="size-full rounded-[28px] md:rounded-[36px]" />
              {centre && (
                <motion.div className="absolute bottom-4 left-4 right-4 md:bottom-7 md:left-7 md:right-auto md:w-[360px] rounded-[22px] bg-ivory/95 p-5 shadow-[0_20px_40px_-20px_#25251f55] backdrop-blur"
                  initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: .35, duration: .5 }}>
                  <p className="font-display text-[19px] font-bold leading-tight">{t("float_t")}</p>
                  <p className="mt-1 text-[14px] text-stone">{t("float_p")}</p>
                  <Link to="/assistant" className="btn-green mt-4 w-full sm:w-auto">{t("start")}<ArrowRight className="size-4" /></Link>
                </motion.div>
              )}
            </motion.div>
          );
        })}
      </div>
      <div className="mt-5 flex items-center justify-center gap-3">
        <button className="grid size-11 place-items-center rounded-full border border-line hover:border-ink/40" onClick={() => go(-1)} aria-label={t("prev")}><ChevronLeft className="size-5" /></button>
        <div className="flex gap-1.5" aria-hidden="true">
          {SLIDES.map((_, k) => <span key={k} className={`h-1.5 rounded-full transition-all duration-500 ${k === i ? "w-6 bg-ink" : "w-1.5 bg-ink/20"}`} />)}
        </div>
        <button className="grid size-11 place-items-center rounded-full border border-line hover:border-ink/40" onClick={() => go(1)} aria-label={t("next")}><ChevronRight className="size-5" /></button>
      </div>
    </div>
  );
}
