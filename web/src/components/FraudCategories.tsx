import { ArrowRight } from "lucide-react";
import { Link } from "react-router";
import { useI18n } from "../i18n/I18n";
import { CATEGORIES } from "../lib/data";
import Reveal from "./Reveal";

export function Illustration({ icon: Icon, tint, className = "" }: { icon: typeof CATEGORIES[0]["icon"]; tint: string; className?: string }) {
  // A horizon arc behind a single icon: one motif, recoloured per card.
  return (
    <div className={`relative overflow-hidden rounded-[20px] ${tint} ${className}`} aria-hidden="true">
      <svg viewBox="0 0 200 120" className="absolute inset-0 size-full transition-transform duration-700 group-hover:scale-110" preserveAspectRatio="xMidYMid slice">
        <circle cx="150" cy="120" r="70" fill="#FAF7F0" opacity=".55" />
        <circle cx="150" cy="120" r="42" fill="#B99559" opacity=".25" />
        <path d="M0 98h200" stroke="#25251F" strokeOpacity=".08" />
      </svg>
      <Icon className="absolute left-5 top-5 size-9 text-ink/80" strokeWidth={1.5} />
    </div>
  );
}

export default function FraudCategories() {
  const { t, tl } = useI18n();
  const titles = tl("cat_t"), descs = tl("cat_p");
  return (
    <section id="what-we-help-with" className="mx-auto max-w-[1280px] px-5 pt-24 md:px-8">
      <Reveal>
        <p className="eyebrow">{t("cat_eyebrow")}</p>
        <h2 className="mt-3 max-w-2xl text-[clamp(2rem,4vw,3rem)] font-extrabold leading-[1.05] tracking-[-.03em]">{t("cat_h")}</h2>
      </Reveal>
      <div className="-mx-5 mt-10 flex snap-x snap-mandatory scroll-px-5 gap-4 overflow-x-auto px-5 pb-4 md:mx-0 md:grid md:grid-cols-3 md:overflow-visible md:px-0">
        {CATEGORIES.map((c, k) => (
          <Reveal key={c.id} delay={k * .06} className="w-[78%] shrink-0 snap-start sm:w-[46%] md:w-auto">
            <Link to={`/assistant?category=${c.id}`} className="group flex h-full flex-col rounded-[24px] border border-line p-3 transition duration-300 hover:-translate-y-1 hover:border-ink/20 hover:shadow-[0_24px_40px_-28px_#25251f66]">
              <Illustration icon={c.icon} tint={c.tint} className="h-36" />
              <div className="flex flex-1 flex-col px-2 pb-2 pt-4">
                <h3 className="text-[20px] font-bold leading-tight">{titles[k]}</h3>
                <p className="mt-2 text-[15px] leading-relaxed text-stone">{descs[k]}</p>
                <span className="mt-auto inline-flex items-center gap-1.5 pt-5 text-[15px] font-semibold text-forest">
                  {t("cat_cta")}<ArrowRight className="size-4 transition-transform group-hover:translate-x-1" />
                </span>
              </div>
            </Link>
          </Reveal>
        ))}
      </div>
    </section>
  );
}
