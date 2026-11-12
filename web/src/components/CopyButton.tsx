import { Check, Copy } from "lucide-react";
import { useState } from "react";
import { useI18n } from "../i18n/I18n";

export default function CopyButton({ text, label }: { text: string; label?: string }) {
  const { t } = useI18n();
  const [done, setDone] = useState(false);
  const copy = async () => {
    try { await navigator.clipboard.writeText(text); setDone(true); setTimeout(() => setDone(false), 1500); } catch { /* clipboard blocked: the text is on screen to select */ }
  };
  return (
    <button type="button" onClick={copy} className="btn-line btn-sm">
      {done ? <Check className="size-3.5 text-forest" /> : <Copy className="size-3.5" />}{done ? t("copied") : label || t("copy")}
    </button>
  );
}
