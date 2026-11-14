import { ArrowLeft, ArrowRight, BookOpen, ExternalLink, Landmark, Phone } from "lucide-react";
import { Link, useParams } from "react-router";
import { LineIcon } from "../components/FraudCategories";
import NotTranslated from "../components/NotTranslated";
import Reveal from "../components/Reveal";
import { useI18n } from "../i18n/I18n";
import { OFFICIAL, RESOURCE_GROUPS, RESOURCES, REVIEWED } from "../lib/data";
import { NotFound } from "./Legal";

export default function Resources() {
  const { t } = useI18n();
  const bySlug = Object.fromEntries(RESOURCES.map(a => [a.slug, a]));
  return (
    <div className="mx-auto max-w-[1280px] px-5 pb-24 pt-12 md:px-8 md:pt-16">
      <NotTranslated />
      <Reveal>
        <p className="eyebrow">{t("res_eyebrow")}</p>
        <h1 className="mt-4 max-w-3xl text-[clamp(2.4rem,5.5vw,4rem)] leading-[1.06] tracking-[-.012em]">{t("res_h")}</h1>
        <p className="mt-5 flex flex-wrap gap-x-6 gap-y-2 text-[14px] text-stone" lang="en">
          <span className="inline-flex items-center gap-2"><BookOpen className="size-4 text-forest" />Golden Hour guide: our plain-language explainer</span>
          <span className="inline-flex items-center gap-2"><Landmark className="size-4 text-gold-ink" />Government website: the official source</span>
        </p>
      </Reveal>
      <div className="mt-12 border-t border-ink/15" lang="en">
        {RESOURCE_GROUPS.map(g => (
          <Reveal key={g.title} className="grid grid-cols-1 gap-4 border-b border-line py-8 lg:grid-cols-[minmax(0,1fr)_minmax(0,2fr)] lg:gap-12">
            <div>
              <h2 className="text-[24px] leading-snug">{g.title}</h2>
              <p className="mt-1.5 text-[15px] text-stone">{g.desc}</p>
            </div>
            <ul className="divide-y divide-line">
              {g.guides.map(slug => bySlug[slug]).map(a => (
                <li key={a.slug}>
                  <Link to={`/resources/${a.slug}`} className="group flex items-start gap-4 py-3.5">
                    <BookOpen className="mt-1 size-4 shrink-0 text-forest" aria-label="Golden Hour guide" />
                    <span className="min-w-0 flex-1"><span className="block text-[16px] font-medium group-hover:text-forest">{a.title}</span>
                      <span className="block text-[14px] text-stone">{a.desc} · {a.minutes} min read</span></span>
                    <ArrowRight className="mt-1 size-4 shrink-0 text-stone transition-transform group-hover:translate-x-0.5 group-hover:text-forest" />
                  </Link>
                </li>
              ))}
              {g.official.map(k => OFFICIAL[k]).map(o => (
                <li key={o.url}>
                  <a href={o.url} {...(o.url.startsWith("http") ? { target: "_blank", rel: "noopener noreferrer" } : {})} className="group flex items-start gap-4 py-3.5">
                    <Landmark className="mt-1 size-4 shrink-0 text-gold-ink" aria-label="Government website" />
                    <span className="min-w-0 flex-1"><span className="block text-[16px] font-medium group-hover:text-forest">{o.label}</span>
                      <span className="block text-[14px] text-stone">{o.desc}</span></span>
                    <ExternalLink className="mt-1 size-4 shrink-0 text-stone group-hover:text-forest" />
                  </a>
                </li>
              ))}
              {g.title.startsWith("Victim") && (
                <li><Link to="/track" className="group flex items-start gap-4 py-3.5">
                  <BookOpen className="mt-1 size-4 shrink-0 text-forest" aria-label="Golden Hour tool" />
                  <span className="min-w-0 flex-1"><span className="block text-[16px] font-medium group-hover:text-forest">Follow-up tracker</span>
                    <span className="block text-[14px] text-stone">Save your reference numbers and see what's due next.</span></span>
                  <ArrowRight className="mt-1 size-4 shrink-0 text-stone group-hover:text-forest" />
                </Link></li>
              )}
            </ul>
          </Reveal>
        ))}
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
        <LineIcon icon={a.icon} className="mt-10" />
        <h1 className="mt-4 text-[clamp(2rem,5vw,3.25rem)] leading-[1.08] tracking-[-.012em]">{a.title}</h1>
        <p className="mt-4 text-[18px] text-stone">{a.desc}</p>
      </Reveal>
      <div className="mt-10 grid gap-8">
        {a.body.map(s => (
          <section key={s.h}>
            <h2 className="text-[25px] leading-snug">{s.h}</h2>
            {s.p && <p className="mt-2 text-[17px] leading-relaxed text-stone">{s.p}</p>}
            {s.list && <ul className="mt-3 grid gap-2">{s.list.map(x => (
              <li key={x} className="flex gap-3 text-[17px] leading-relaxed text-stone"><span className="mt-3 size-1.5 shrink-0 rounded-full bg-gold" />{x}</li>
            ))}</ul>}
          </section>
        ))}
      </div>
      <section className="mt-12 border-t border-line pt-6">
        <h2 className="font-sans text-[15px] font-semibold">Sources</h2>
        <ul className="mt-3 grid gap-2">
          {a.sources.map(src => (
            <li key={src.url}><a href={src.url} target="_blank" rel="noopener noreferrer" className="inline-flex items-start gap-1.5 text-[14px] text-stone underline-offset-4 hover:text-ink hover:underline">
              {src.label}<ExternalLink className="mt-1 size-3 shrink-0" /></a></li>
          ))}
        </ul>
        <p className="mt-3 text-[13px] text-stone">Last reviewed {REVIEWED}. Procedures change: always follow what official channels tell you.</p>
      </section>
      <div className="mt-8 flex flex-wrap items-center gap-3 rounded-[8px] bg-cream p-6">
        <p className="mr-auto font-display text-[20px] font-bold">{t("em_h")}</p>
        <a href="tel:1930" className="btn-red"><Phone className="size-4" />{t("em_call")}</a>
        {a.slug === "follow-up-complaint" && <Link to="/track" className="btn-line">Open the follow-up tracker</Link>}
        <Link to="/assistant" className="btn-green">{t("get_help")}</Link>
      </div>
    </article>
  );
}
