import { ArrowRight } from "lucide-react";
import { Link } from "react-router";
import { useI18n } from "../i18n/I18n";
import type { Article } from "../lib/data";
import { LineIcon } from "./FraudCategories";

export default function ResourceCard({ a }: { a: Article }) {
  const { t } = useI18n();
  return (
    <Link to={`/resources/${a.slug}`} lang="en" className="group flex h-full flex-col border-t border-ink/15 pt-6 transition-colors hover:border-forest">
      <div className="flex items-center justify-between">
        <LineIcon icon={a.icon} className="size-5" />
        <p className="text-[13px] text-stone">{a.minutes} min read</p>
      </div>
      <h3 className="mt-5 font-display text-[23px] font-normal leading-snug">{a.title}</h3>
      <p className="mt-2 text-[15px] leading-relaxed text-stone">{a.desc}</p>
      <span className="mt-auto inline-flex items-center gap-1.5 pt-5 text-[14px] font-medium text-forest">
        {t("read_more")}<ArrowRight className="size-4 transition-transform duration-300 group-hover:translate-x-1" />
      </span>
    </Link>
  );
}
