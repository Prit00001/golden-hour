import { ArrowRight, type LucideIcon } from "lucide-react";
import { Link } from "react-router";
import { useI18n } from "../i18n/I18n";
import { CATEGORIES } from "../lib/data";
import Reveal from "./Reveal";

// One quiet icon style everywhere: thin forest-green line, no tinted container.
export function LineIcon({ icon: Icon, className = "" }: { icon: LucideIcon; className?: string }) {
  return <Icon className={`size-6 text-forest ${className}`} strokeWidth={1.5} aria-hidden="true" />;
}

export default function FraudCategories() {
  const { t, tl } = useI18n();
  const titles = tl("cat_t"), descs = tl("cat_p");
  return (
    <section id="what-we-help-with" className="mx-auto max-w-[1280px] px-5 pt-24 md:px-8">
      <Reveal>
        <p className="eyebrow">{t("cat_eyebrow")}</p>
        <h2 className="mt-3 max-w-2xl text-[clamp(2rem,3.6vw,2.9rem)] leading-[1.08] tracking-[-.012em]">{t("cat_h")}</h2>
      </Reveal>
      {/* A ruled grid rather than floating cards: the dividers do the separating. */}
      <div className="mt-10 grid grid-cols-1 border-t border-line sm:grid-cols-2 lg:grid-cols-3">
        {CATEGORIES.map((c, k) => (
          <Reveal key={c.id} delay={k * .05} className="border-b border-line sm:[&:nth-child(odd)]:border-r lg:border-r lg:[&:nth-child(3n)]:border-r-0">
            <Link to={`/assistant?category=${c.id}`} className="group flex h-full flex-col px-1 py-8 transition-colors hover:bg-paper sm:px-7">
              <LineIcon icon={c.icon} />
              <h3 className="mt-6 text-[18px] font-semibold leading-snug">{titles[k]}</h3>
              <p className="mt-2 text-[15px] leading-relaxed text-stone">{descs[k]}</p>
              <span className="mt-auto inline-flex items-center gap-1.5 pt-6 text-[14px] font-medium text-forest">
                {t("cat_cta")}<ArrowRight className="size-4 transition-transform duration-300 group-hover:translate-x-1" />
              </span>
            </Link>
          </Reveal>
        ))}
      </div>
    </section>
  );
}
