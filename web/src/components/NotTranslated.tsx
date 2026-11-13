import { Languages } from "lucide-react";
import { useI18n } from "../i18n/I18n";

// Shown on English-only pages when another language is picked, so nothing pretends to be translated.
export default function NotTranslated() {
  const { lang, t } = useI18n();
  if (lang === "en") return null;
  return (
    <p className="mb-8 flex items-start gap-2.5 rounded-[6px] bg-mint px-4 py-3 text-[14px] text-forest">
      <Languages className="mt-0.5 size-4 shrink-0" />{t("not_translated")}
    </p>
  );
}
