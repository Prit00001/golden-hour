import { motion } from "framer-motion";
import { Check, ShieldAlert } from "lucide-react";
import { useEffect, useState } from "react";
import { useI18n } from "../i18n/I18n";

const KEY = "gh-evidence";  // ticks stay in this browser only; nothing is sent anywhere
const load = (): number[] => { try { return JSON.parse(localStorage.getItem(KEY) || "[]"); } catch { return []; } };

export default function EvidenceChecklist({ compact = false }: { compact?: boolean }) {
  const { t, tl } = useI18n();
  const items = tl("ev_items");
  const [done, setDone] = useState<number[]>(load);
  useEffect(() => { try { localStorage.setItem(KEY, JSON.stringify(done)); } catch { /* not remembered */ } }, [done]);
  const toggle = (k: number) => setDone(d => d.includes(k) ? d.filter(x => x !== k) : [...d, k]);
  const pct = Math.round(100 * done.length / items.length);

  return (
    <div>
      <div className="flex items-center justify-between gap-4 text-[14px] font-medium">
        <span>{t("ev_count", { n: done.length, total: items.length })}</span><span className="text-stone">{pct}%</span>
      </div>
      <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-cream" role="progressbar" aria-valuenow={pct} aria-valuemin={0} aria-valuemax={100}>
        <motion.div className="h-full rounded-full bg-forest" initial={false} animate={{ width: `${pct}%` }} transition={{ duration: .5 }} />
      </div>
      <ul className={`mt-5 grid gap-2 ${compact ? "" : "sm:grid-cols-2 lg:grid-cols-3"}`}>
        {items.map((label, k) => {
          const on = done.includes(k);
          return (
            <li key={k}>
              <button type="button" onClick={() => toggle(k)} aria-pressed={on}
                className={`flex w-full items-center gap-3 rounded-2xl border px-4 py-3 text-left text-[15px] transition ${on ? "border-forest/30 bg-mint" : "border-line hover:border-ink/25"}`}>
                <span className={`grid size-6 shrink-0 place-items-center rounded-full border transition ${on ? "border-forest bg-forest text-ivory" : "border-ink/25"}`}>
                  {on && <Check className="size-3.5" strokeWidth={3} />}
                </span>
                <span className={on ? "text-forest" : ""}>{label}</span>
              </button>
            </li>
          );
        })}
      </ul>
      <p className="mt-5 flex gap-2.5 rounded-2xl bg-[#f6e3df] px-4 py-3 text-[14px] leading-relaxed text-alert">
        <ShieldAlert className="mt-0.5 size-4 shrink-0" />{t("ev_warn")}
      </p>
    </div>
  );
}
