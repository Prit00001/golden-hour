import { motion } from "framer-motion";
import { ArrowRight, FileText, Languages, ListChecks } from "lucide-react";
import { useState, type FormEvent } from "react";
import { Link, useNavigate } from "react-router";
import { useI18n } from "../i18n/I18n";
import ImageCarousel from "./ImageCarousel";

export default function Hero() {
  const { t, tl } = useI18n();
  const navigate = useNavigate();
  const [text, setText] = useState("");
  const icons = [Languages, ListChecks, FileText];
  // The first thing a panicking visitor does here is say what happened: the assistant opens with it already sent.
  // Passed as router state, never in the URL, so it stays out of history and server logs.
  const start = (e: FormEvent) => { e.preventDefault(); navigate("/assistant", { state: text.trim() ? { initial: text.trim() } : undefined }); };

  return (
    <section className="pt-6 md:pt-10">
      <div className="mx-auto grid grid-cols-1 max-w-[1280px] gap-8 px-5 md:px-8 lg:grid-cols-[minmax(0,1.25fr)_minmax(0,1fr)] lg:items-end">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: .7, ease: [.22, 1, .36, 1] }}>
          <p className="inline-flex items-center gap-2 rounded-full border border-line px-3.5 py-1.5 text-[13px] font-medium text-stone">
            <span className="size-1.5 rounded-full bg-gold" />{t("hero_tag")}
          </p>
          <h1 className="mt-5 text-[clamp(2.3rem,5.2vw,4.4rem)] font-extrabold leading-[1.03] tracking-[-.035em]">{t("hero_h")}</h1>
        </motion.div>
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: .7, delay: .12, ease: [.22, 1, .36, 1] }}>
          <p className="text-[16px] leading-relaxed text-stone">{t("hero_p")}</p>
          <form onSubmit={start} className="mt-5 flex flex-col gap-2 rounded-[22px] border border-line bg-white p-2 shadow-[0_18px_40px_-28px_#25251f55] focus-within:border-forest sm:flex-row sm:items-center">
            <label htmlFor="hero-say" className="sr-only">{t("input_ph")}</label>
            <input id="hero-say" value={text} onChange={e => setText(e.target.value)} maxLength={500} autoComplete="off" placeholder={t("input_ph")}
              className="min-w-0 flex-1 bg-transparent px-3 py-3 text-[16px] placeholder:text-stone/70 focus:outline-none" />
            <button className="btn-green shrink-0">{t("hero_cta")}<ArrowRight className="size-4" /></button>
          </form>
          <Link to="/#how-it-works" className="mt-3 inline-flex items-center gap-1.5 px-1 text-[14px] font-semibold text-stone hover:text-ink">
            {t("hero_cta2")}<ArrowRight className="size-3.5" />
          </Link>
        </motion.div>
      </div>
      <div className="mt-8 md:mt-10"><ImageCarousel /></div>
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
