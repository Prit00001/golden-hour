import { Globe } from "lucide-react";
import { LANGS, useI18n, type Lang } from "../i18n/I18n";

export default function LanguageSelector({ className = "" }: { className?: string }) {
  const { lang, setLang, t } = useI18n();
  return (
    <label className={`relative items-center ${className || "inline-flex"}`}>
      <Globe className="pointer-events-none absolute left-2 size-[15px] text-stone" aria-hidden="true" />
      <span className="sr-only">{t("language")}</span>
      <select value={lang} onChange={e => setLang(e.target.value as Lang)}
        className="cursor-pointer appearance-none rounded-[6px] border border-transparent bg-transparent py-1.5 pl-7 pr-2 text-[14px] text-stone transition-colors hover:border-line hover:text-ink focus:border-forest focus:outline-none">
        {LANGS.map(l => <option key={l.code} value={l.code}>{l.native}</option>)}
      </select>
    </label>
  );
}
