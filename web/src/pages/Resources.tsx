import { ArrowLeft, ExternalLink, Phone } from "lucide-react";
import { Link, useParams } from "react-router";
import { Illustration } from "../components/FraudCategories";
import NotTranslated from "../components/NotTranslated";
import ResourceCard from "../components/ResourceCard";
import Reveal from "../components/Reveal";
import { useI18n } from "../i18n/I18n";
import { RESOURCES, REVIEWED } from "../lib/data";
import { NotFound } from "./Legal";

export default function Resources() {
  const { t } = useI18n();
  return (
    <div className="mx-auto max-w-[1280px] px-5 pb-24 pt-12 md:px-8 md:pt-16">
      <NotTranslated />
      <Reveal>
        <p className="eyebrow">{t("res_eyebrow")}</p>
        <h1 className="mt-4 max-w-3xl text-[clamp(2.4rem,6vw,4.5rem)] font-extrabold leading-[1.02] tracking-[-.035em]">{t("res_h")}</h1>
      </Reveal>
      <div className="mt-12 grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
        {RESOURCES.map((a, k) => <Reveal key={a.slug} delay={(k % 3) * .08}><ResourceCard a={a} /></Reveal>)}
      </div>
    </div>
  );
}

export function Article() {
  const { slug } = useParams();
  const { t } = useI18n();
  const a = RESOURCES.find(r => r.slug === slug);
  if (!a) return <NotFound />;
  return (
    <article className="mx-auto max-w-3xl px-5 pb-24 pt-10 md:pt-14" lang="en">
      <NotTranslated />
      <Link to="/resources" className="inline-flex items-center gap-1.5 text-[14px] font-medium text-stone hover:text-ink"><ArrowLeft className="size-4" />{t("res_all")}</Link>
      <Reveal>
        <h1 className="mt-6 text-[clamp(2rem,5vw,3.25rem)] font-extrabold leading-[1.05] tracking-[-.03em]">{a.title}</h1>
        <p className="mt-4 text-[18px] text-stone">{a.desc}</p>
        <Illustration icon={a.icon} tint={a.tint} className="mt-8 h-48" />
      </Reveal>
      <div className="mt-10 grid gap-8">
        {a.body.map(s => (
          <section key={s.h}>
            <h2 className="text-[22px] font-bold">{s.h}</h2>
            {s.p && <p className="mt-2 text-[17px] leading-relaxed text-stone">{s.p}</p>}
            {s.list && <ul className="mt-3 grid gap-2">{s.list.map(x => (
              <li key={x} className="flex gap-3 text-[17px] leading-relaxed text-stone"><span className="mt-3 size-1.5 shrink-0 rounded-full bg-gold" />{x}</li>
            ))}</ul>}
          </section>
        ))}
      </div>
      <section className="mt-12 border-t border-line pt-6">
        <h2 className="text-[15px] font-bold">Sources</h2>
        <ul className="mt-3 grid gap-2">
          {a.sources.map(src => (
            <li key={src.url}><a href={src.url} target="_blank" rel="noopener noreferrer" className="inline-flex items-start gap-1.5 text-[14px] text-stone underline-offset-4 hover:text-ink hover:underline">
              {src.label}<ExternalLink className="mt-1 size-3 shrink-0" /></a></li>
          ))}
        </ul>
        <p className="mt-3 text-[13px] text-stone">Last reviewed {REVIEWED}. Procedures change: always follow what official channels tell you.</p>
      </section>
      <div className="mt-8 flex flex-wrap items-center gap-3 rounded-[24px] bg-cream p-6">
        <p className="mr-auto font-display text-[20px] font-bold">{t("em_h")}</p>
        <a href="tel:1930" className="btn-red"><Phone className="size-4" />{t("em_call")}</a>
        {a.slug === "follow-up-complaint" && <Link to="/track" className="btn-line">Open the follow-up tracker</Link>}
        <Link to="/assistant" className="btn-green">{t("get_help")}</Link>
      </div>
    </article>
  );
}
