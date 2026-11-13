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
      <div className="mt-2 h-[3px] overflow-hidden bg-line" role="progressbar" aria-valuenow={pct} aria-valuemin={0} aria-valuemax={100}>
        <motion.div className="h-full bg-forest" initial={false} animate={{ width: `${pct}%` }} transition={{ duration: .5 }} />
      </div>
      <ul className={`mt-5 grid grid-cols-1 gap-x-8 border-t border-line ${compact ? "" : "sm:grid-cols-2 lg:grid-cols-3"}`}>
        {items.map((label, k) => {
          const on = done.includes(k);
          return (
            <li key={k} className="border-b border-line">
              <button type="button" onClick={() => toggle(k)} aria-pressed={on}
                className="group flex w-full items-center gap-3 py-3.5 text-left text-[15px]">
                <span className={`grid size-[18px] shrink-0 place-items-center rounded-[4px] border transition-colors ${on ? "border-forest bg-forest text-ivory" : "border-ink/30 group-hover:border-forest"}`}>
                  {on && <Check className="size-3" strokeWidth={3} />}
                </span>
                <span className={`transition-colors ${on ? "text-stone line-through decoration-forest/50" : "group-hover:text-forest"}`}>{label}</span>
              </button>
            </li>
          );
        })}
      </ul>
      <p className="mt-6 flex gap-2.5 border-l-2 border-alert pl-3.5 text-[14px] leading-relaxed text-alert">
        <ShieldAlert className="mt-0.5 size-4 shrink-0" />{t("ev_warn")}
      </p>
    </div>
  );
}
