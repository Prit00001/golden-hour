import { motion } from "framer-motion";
import { ArrowRight, FileText, Languages, ListChecks } from "lucide-react";
import { Link } from "react-router";
import { useI18n } from "../i18n/I18n";
import HeroPhoto from "./HeroPhoto";

export default function Hero() {
  const { t, tl } = useI18n();
  const icons = [Languages, ListChecks, FileText];
  const rise = (delay = 0) => ({ initial: { opacity: 0, y: 16 }, animate: { opacity: 1, y: 0 }, transition: { duration: .7, delay, ease: [.22, 1, .36, 1] as const } });
  return (
    <section className="pt-12 md:pt-16">
      <div className="mx-auto grid max-w-[1280px] grid-cols-1 gap-x-16 gap-y-7 px-5 md:px-8 lg:grid-cols-[minmax(0,1.2fr)_minmax(0,1fr)] lg:items-end">
        <motion.div {...rise()}>
          <p className="flex items-center gap-3 text-[13px] text-stone"><span className="h-px w-8 bg-gold" />{t("hero_tag")}</p>
          <h1 className="mt-5 text-[clamp(2.5rem,5vw,4.1rem)] leading-[1.04] tracking-[-.015em]">{t("hero_h")}</h1>
        </motion.div>
        <motion.div className="lg:pb-2" {...rise(.12)}>
          <p className="max-w-[46ch] text-[17px] leading-[1.65] text-stone">{t("hero_p")}</p>
          <div className="mt-7 flex flex-wrap items-center gap-3">
            <Link to="/assistant" className="btn-green">{t("hero_cta")}<ArrowRight className="size-4" /></Link>
            <Link to="/#how-it-works" className="btn-line">{t("hero_cta2")}</Link>
          </div>
        </motion.div>
      </div>
      <div className="mt-12 md:mt-14"><HeroPhoto /></div>
      <ul className="mx-auto mt-10 grid max-w-[1280px] grid-cols-1 px-5 sm:grid-cols-3 md:px-8">
        {tl("trust").map((label, k) => {
          const Icon = icons[k];
          return (
            <li key={k} className={`flex items-center gap-3 py-3 sm:py-1 ${k ? "border-t border-line sm:border-t-0 sm:border-l sm:pl-6" : ""}`}>
              <Icon className="size-[18px] shrink-0 text-forest" strokeWidth={1.6} />
              <span className="text-[15px]">{label}</span>
            </li>
          );
        })}
      </ul>
    </section>
  );
}
