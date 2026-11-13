import { ExternalLink } from "lucide-react";
import { useI18n } from "../i18n/I18n";
import Reveal from "./Reveal";

const SOURCE = "https://scroll.in/latest/1084796/indians-lost-rs-22845-crore-to-cyber-fraud-in-2024-a-206-rise-from-previous-year-centre";

// Every figure here is from one verified source (MHA's Lok Sabha reply); don't add a number without one.
export default function ImpactStats() {
  const { t } = useI18n();
  const stats = [[t("n1"), t("stat1")], [t("n2"), t("stat2")], [t("n3"), t("stat3")]];
  return (
    <section className="mx-auto max-w-[1280px] px-5 pt-20 md:px-8">
      <Reveal className="grid grid-cols-1 gap-8 border-y border-line py-10 lg:grid-cols-[minmax(0,1fr)_minmax(0,2fr)] lg:items-center">
        <div>
          <p className="eyebrow">{t("stats_eyebrow")}</p>
          <h2 className="mt-3 text-[clamp(1.6rem,3vw,2.25rem)] leading-[1.1] tracking-[-.01em]">{t("stats_h")}</h2>
        </div>
        <div>
          <dl className="grid grid-cols-1 gap-6 sm:grid-cols-3">
            {stats.map(([n, label], k) => (
              <div key={k}>
                <dt className="sr-only">{label}</dt>
                <dd className={`font-display text-[clamp(1.6rem,2.6vw,2.15rem)] font-medium leading-none tracking-tight whitespace-nowrap ${k === 2 ? "text-forest" : ""}`}>{n}</dd>
                <dd className="mt-2 text-[14px] leading-snug text-stone">{label}</dd>
              </div>
            ))}
          </dl>
          <a href={SOURCE} target="_blank" rel="noopener noreferrer" className="mt-6 inline-flex items-center gap-1.5 text-[12px] text-stone hover:text-ink">
            {t("stats_src")}<ExternalLink className="size-3" />
          </a>
        </div>
      </Reveal>
    </section>
  );
}
