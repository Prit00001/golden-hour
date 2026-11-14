import { ChevronDown, Globe } from "lucide-react";
import { LANGS, useI18n, type Lang } from "../i18n/I18n";

// tone "dark" sits on the deep-green strip at the top of the page.
export default function LanguageSelector({ className = "", tone = "light" }: { className?: string; tone?: "light" | "dark" }) {
  const { lang, setLang, t } = useI18n();
  const colors = tone === "dark" ? "text-ivory/85 hover:text-ivory focus:border-ivory/40" : "text-stone hover:border-line hover:text-ink focus:border-forest";
  return (
    <label className={`relative items-center ${className || "inline-flex"}`}>
      <Globe className={`pointer-events-none absolute left-2 size-[15px] ${tone === "dark" ? "text-ivory/70" : "text-stone"}`} aria-hidden="true" />
      <span className="sr-only">{t("language")}</span>
      <select value={lang} onChange={e => setLang(e.target.value as Lang)}
        className={`cursor-pointer appearance-none rounded-[6px] border border-transparent bg-transparent py-1 pl-7 pr-6 text-[13px] transition-colors focus:outline-none ${colors}`}>
        {LANGS.map(l => <option key={l.code} value={l.code} className="text-ink">{l.native}</option>)}
      </select>
      <ChevronDown className={`pointer-events-none absolute right-1.5 size-3.5 ${tone === "dark" ? "text-ivory/70" : "text-stone"}`} aria-hidden="true" />
    </label>
  );
}
