import { Globe } from "lucide-react";
import { LANGS, useI18n, type Lang } from "../i18n/I18n";

export default function LanguageSelector({ className = "" }: { className?: string }) {
  const { lang, setLang, t } = useI18n();
  return (
    <label className={`relative items-center ${className || "inline-flex"}`}>
      <Globe className="pointer-events-none absolute left-3.5 size-4 text-stone" aria-hidden="true" />
      <span className="sr-only">{t("language")}</span>
      <select value={lang} onChange={e => setLang(e.target.value as Lang)}
        className="cursor-pointer appearance-none rounded-full border border-line bg-ivory py-2.5 pl-9 pr-4 text-[14px] font-medium hover:border-ink/30 focus:border-forest focus:outline-none">
        {LANGS.map(l => <option key={l.code} value={l.code}>{l.native}</option>)}
      </select>
    </label>
  );
}
