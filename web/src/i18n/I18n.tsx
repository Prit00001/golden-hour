import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import bn from "./bn";
import en, { type Strings } from "./en";
import hi from "./hi";
import kn from "./kn";
import mr from "./mr";
import ta from "./ta";
import te from "./te";

// Only languages the voice assistant really speaks are offered. Adding one = a strings file here
// plus its questions and checklist in app/flow.py; nothing else changes.
export const LANGS = [
  { code: "en", native: "English" }, { code: "hi", native: "हिंदी" }, { code: "bn", native: "বাংলা" },
  { code: "kn", native: "ಕನ್ನಡ" }, { code: "ta", native: "தமிழ்" }, { code: "te", native: "తెలుగు" }, { code: "mr", native: "मराठी" },
] as const;
export type Lang = (typeof LANGS)[number]["code"];
const TABLES: Record<Lang, Partial<Strings>> = { en, hi, bn, kn, ta, te, mr };
type TextKey = { [K in keyof Strings]: Strings[K] extends string ? K : never }[keyof Strings];
type ListKey = { [K in keyof Strings]: Strings[K] extends string[] ? K : never }[keyof Strings];

const saved = (): Lang | null => { try { return localStorage.getItem("gh-lang") as Lang | null; } catch { return null; } };
const initial = (): Lang => {
  const s = saved();
  if (s && s in TABLES) return s;
  return (navigator.languages.map(l => l.split("-")[0]).find(l => l in TABLES) as Lang) || "en";
};

const Ctx = createContext({
  lang: "en" as Lang,
  setLang: (_: Lang) => {},
  t: (k: TextKey, vars?: Record<string, string | number>) => (vars ? k : en[k]) as string,
  tl: (k: ListKey) => en[k],
});

export function I18nProvider({ children }: { children: ReactNode }) {
  const [lang, setLangState] = useState<Lang>(initial);
  useEffect(() => { document.documentElement.lang = lang; }, [lang]);
  const setLang = (l: Lang) => { setLangState(l); try { localStorage.setItem("gh-lang", l); } catch { /* private mode: not remembered */ } };
  const table = TABLES[lang];
  const t = (k: TextKey, vars?: Record<string, string | number>) =>
    Object.entries(vars || {}).reduce((s, [v, x]) => s.replace(`{${v}}`, String(x)), (table[k] ?? en[k]) as string);
  const tl = (k: ListKey) => (table[k] ?? en[k]) as string[];
  return <Ctx.Provider value={{ lang, setLang, t, tl }}>{children}</Ctx.Provider>;
}
export const useI18n = () => useContext(Ctx);
