import { motion } from "framer-motion";
import { ArrowRight, FileText, Languages, ListChecks } from "lucide-react";
import { Link } from "react-router";
import { useI18n } from "../i18n/I18n";
import ImageCarousel from "./ImageCarousel";

export default function Hero() {
  const { t, tl } = useI18n();
  const icons = [Languages, ListChecks, FileText];
  return (
    <section className="pt-8 md:pt-14">
      <div className="mx-auto grid grid-cols-1 max-w-[1280px] gap-8 px-5 md:px-8 lg:grid-cols-[minmax(0,1.35fr)_minmax(0,1fr)] lg:items-end">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: .7, ease: [.22, 1, .36, 1] }}>
          <p className="inline-flex items-center gap-2 rounded-full border border-line px-3.5 py-1.5 text-[13px] font-medium text-stone">
            <span className="size-1.5 rounded-full bg-gold" />{t("hero_tag")}
          </p>
          <h1 className="mt-5 text-[clamp(2.4rem,6.2vw,5.4rem)] font-extrabold leading-[1.02] tracking-[-.035em]">{t("hero_h")}</h1>
        </motion.div>
        <motion.div className="lg:pb-3" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: .7, delay: .12, ease: [.22, 1, .36, 1] }}>
          <p className="text-[17px] leading-relaxed text-stone">{t("hero_p")}</p>
          <div className="mt-6 flex flex-wrap gap-3">
            <Link to="/assistant" className="btn-green">{t("hero_cta")}<ArrowRight className="size-4" /></Link>
            <Link to="/#how-it-works" className="btn-line">{t("hero_cta2")}</Link>
          </div>
        </motion.div>
      </div>
      <div className="mt-12 md:mt-16"><ImageCarousel /></div>
      <ul className="mx-auto mt-10 grid max-w-[1280px] gap-3 px-5 sm:grid-cols-3 md:px-8">
        {tl("trust").map((label, k) => {
          const Icon = icons[k];
          return (
            <li key={k} className="flex items-center gap-3 rounded-2xl border border-line px-4 py-3.5">
              <span className="grid size-9 shrink-0 place-items-center rounded-full bg-mint text-forest"><Icon className="size-[18px]" /></span>
              <span className="text-[15px] font-semibold">{label}</span>
            </li>
          );
        })}
      </ul>
    </section>
  );
}
