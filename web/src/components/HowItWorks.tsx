import { useI18n } from "../i18n/I18n";
import Reveal from "./Reveal";

export default function HowItWorks() {
  const { t, tl } = useI18n();
  const titles = tl("how_t"), texts = tl("how_p");
  return (
    <section id="how-it-works" className="mx-auto max-w-[1280px] px-5 pt-24 md:px-8">
      <Reveal className="grid grid-cols-1 gap-4 md:grid-cols-[minmax(0,1fr)_minmax(0,1fr)] md:items-end">
        <div>
          <p className="eyebrow">{t("how_eyebrow")}</p>
          <h2 className="mt-3 text-[clamp(2.2rem,5vw,4rem)] font-extrabold leading-[1] tracking-[-.035em]">{t("how_h")}</h2>
        </div>
      </Reveal>
      <ol className="mt-12 grid grid-cols-1 gap-8 md:grid-cols-4 md:gap-6">
        {titles.map((title, k) => (
          <Reveal key={k} delay={k * .1}>
            <li className="relative border-t border-ink/15 pt-6">
              <span className="absolute -top-px left-0 h-px w-12 bg-gold" />
              <p className="font-display text-[44px] font-extrabold leading-none text-gold/80">0{k + 1}</p>
              <h3 className="mt-5 text-[20px] font-bold leading-tight">{title}</h3>
              <p className="mt-2 text-[15px] leading-relaxed text-stone">{texts[k]}</p>
            </li>
          </Reveal>
        ))}
      </ol>
    </section>
  );
}
