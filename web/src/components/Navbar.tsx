import { AnimatePresence, motion } from "framer-motion";
import { ArrowRight, ExternalLink, Menu, Phone, X } from "lucide-react";
import { useEffect, useState } from "react";
import { Link, NavLink, useLocation } from "react-router";
import { useI18n } from "../i18n/I18n";
import LanguageSelector from "./LanguageSelector";
import Logo from "./Logo";

// A masthead: a slim deep-green strip with the emergency line and language, then the name set in the centre
// with the sections split either side, like the front page of a paper.
export default function Navbar() {
  const { t } = useI18n();
  const [open, setOpen] = useState(false);
  const { pathname, hash } = useLocation();
  useEffect(() => setOpen(false), [pathname, hash]);

  const links = [
    { to: "/", label: t("nav_home") },
    { to: "/#how-it-works", label: t("nav_how") },
    { to: "/#what-we-help-with", label: t("nav_help") },
    { to: "/resources", label: t("nav_res") },
    { to: "/about", label: t("nav_about") },
  ];
  const active = (to: string) => (to === "/" ? pathname === "/" && !hash : to.startsWith("/#") ? pathname === "/" && hash === to.slice(1) : pathname.startsWith(to));
  const item = (l: typeof links[0]) => (
    <NavLink key={l.to} to={l.to} aria-current={active(l.to) ? "page" : undefined}
      className={`whitespace-nowrap text-[14px] underline-offset-[6px] transition-colors hover:text-ink hover:underline hover:decoration-line
        ${active(l.to) ? "text-ink underline decoration-forest decoration-1" : "text-stone"}`}>{l.label}</NavLink>
  );

  return (
    <>
      <div className="bg-deep text-ivory">
        <div className="mx-auto flex h-9 max-w-[1280px] items-center gap-5 px-5 text-[13px] md:px-8">
          <a href="tel:1930" className="inline-flex items-center gap-1.5 font-medium hover:underline underline-offset-4">
            <Phone className="size-3.5" />{t("call_short")}
          </a>
          <a href="https://cybercrime.gov.in" target="_blank" rel="noopener noreferrer" className="hidden items-center gap-1 text-ivory/75 hover:text-ivory sm:inline-flex">
            cybercrime.gov.in<ExternalLink className="size-3" />
          </a>
          <LanguageSelector tone="dark" className="ml-auto inline-flex" />
        </div>
      </div>
      <header className="sticky top-0 z-40 border-b border-line bg-ivory/95 backdrop-blur-sm">
        <div className="mx-auto grid h-[64px] max-w-[1280px] grid-cols-[1fr_auto] items-center gap-6 px-5 md:px-8 xl:grid-cols-[minmax(0,1fr)_auto_minmax(0,1fr)]">
          <nav className="hidden items-center gap-7 xl:flex" aria-label="Main">{links.slice(0, 3).map(item)}</nav>
          <Logo />
          <div className="flex items-center justify-end gap-7">
            <nav className="hidden items-center gap-7 xl:flex" aria-label="More">{links.slice(3).map(item)}</nav>
            <Link to="/assistant" className="btn-green hidden !px-4 !py-2 text-[14px] md:inline-flex">{t("get_help")}<ArrowRight className="size-4" /></Link>
            <button className="-mr-1.5 grid size-9 place-items-center rounded-[6px] text-ink hover:bg-ink/[.04] xl:hidden" onClick={() => setOpen(o => !o)}
              aria-expanded={open} aria-controls="mobile-nav" aria-label={open ? t("close") : t("menu")}>
              {open ? <X className="size-5" /> : <Menu className="size-5" />}
            </button>
          </div>
        </div>
        <AnimatePresence>
          {open && (
            <motion.nav id="mobile-nav" aria-label="Main" className="overflow-hidden border-t border-line xl:hidden"
              initial={{ height: 0, opacity: 0 }} animate={{ height: "auto", opacity: 1 }} exit={{ height: 0, opacity: 0 }} transition={{ duration: .25 }}>
              <div className="flex flex-col px-5 py-2 md:px-8">
                {links.map(l => <Link key={l.to} to={l.to} className="border-b border-line py-3.5 font-display text-[20px] last:border-0">{l.label}</Link>)}
                <Link to="/assistant" className="btn-green my-4 md:hidden">{t("get_help")}<ArrowRight className="size-4" /></Link>
              </div>
            </motion.nav>
          )}
        </AnimatePresence>
      </header>
    </>
  );
}
