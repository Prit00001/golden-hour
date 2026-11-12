import { ArrowRight } from "lucide-react";
import { Link } from "react-router";
import { useI18n } from "../i18n/I18n";
import type { Article } from "../lib/data";
import { Illustration } from "./FraudCategories";

export default function ResourceCard({ a }: { a: Article }) {
  const { t } = useI18n();
  return (
    <Link to={`/resources/${a.slug}`} lang="en" className="group flex h-full flex-col rounded-[24px] border border-line p-3 transition duration-300 hover:-translate-y-1 hover:border-ink/20">
      <Illustration icon={a.icon} tint={a.tint} className="h-40" />
      <div className="flex flex-1 flex-col px-2 pb-2 pt-4">
        <p className="text-[13px] text-stone">{a.minutes} min read</p>
        <h3 className="mt-1 text-[19px] font-bold leading-snug">{a.title}</h3>
        <p className="mt-2 text-[15px] leading-relaxed text-stone">{a.desc}</p>
        <span className="mt-auto inline-flex items-center gap-1.5 pt-5 text-[15px] font-semibold text-forest">
          {t("read_more")}<ArrowRight className="size-4 transition-transform group-hover:translate-x-1" />
        </span>
      </div>
    </Link>
  );
}
