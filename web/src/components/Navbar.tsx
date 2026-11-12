import { AnimatePresence, motion } from "framer-motion";
import { ArrowRight, LifeBuoy, Menu, X } from "lucide-react";
import { useEffect, useState } from "react";
import { Link, NavLink, useLocation } from "react-router";
import { useI18n } from "../i18n/I18n";
import LanguageSelector from "./LanguageSelector";
import Logo from "./Logo";

export default function Navbar() {
  const { t } = useI18n();
  const [open, setOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const { pathname, hash } = useLocation();
  useEffect(() => setOpen(false), [pathname, hash]);
  useEffect(() => {
    const on = () => setScrolled(window.scrollY > 8);
    on(); window.addEventListener("scroll", on, { passive: true });
    return () => window.removeEventListener("scroll", on);
  }, []);

  const links = [
    { to: "/", label: t("nav_home") },
    { to: "/#how-it-works", label: t("nav_how") },
    { to: "/#what-we-help-with", label: t("nav_help") },
    { to: "/resources", label: t("nav_res") },
    { to: "/about", label: t("nav_about") },
  ];
  const active = (to: string) => (to === "/" ? pathname === "/" && !hash : to.startsWith("/#") ? pathname === "/" && hash === to.slice(1) : pathname.startsWith(to));

  return (
    <header className={`sticky top-0 z-40 bg-ivory/90 backdrop-blur-md transition-shadow ${scrolled ? "shadow-[0_1px_0_#E6DED2]" : ""}`}>
      <div className="mx-auto flex max-w-[1280px] items-center gap-4 px-5 py-4 md:px-8">
        <Logo />
        <nav className="mx-auto hidden xl:flex items-center gap-0.5" aria-label="Main">
          {links.map(l => (
            <NavLink key={l.to} to={l.to} className={`whitespace-nowrap rounded-full px-3 py-2 text-[14px] font-medium transition-colors hover:bg-cream ${active(l.to) ? "text-ink bg-cream" : "text-stone"}`}>
              {l.label}
            </NavLink>
          ))}
        </nav>
        <div className="ml-auto xl:ml-0 flex items-center gap-2">
          <LanguageSelector className="hidden sm:inline-flex" />
          <Link to="/#help-now" className="grid size-11 place-items-center rounded-full border border-line hover:border-ink/30 text-alert" aria-label={t("emergency_link")} title={t("emergency_link")}>
            <LifeBuoy className="size-5" />
          </Link>
          <Link to="/assistant" className="btn-green hidden md:inline-flex">{t("get_help")}<ArrowRight className="size-4" /></Link>
          <button className="grid size-11 place-items-center rounded-full border border-line xl:hidden" onClick={() => setOpen(o => !o)}
            aria-expanded={open} aria-controls="mobile-nav" aria-label={open ? t("close") : t("menu")}>
            {open ? <X className="size-5" /> : <Menu className="size-5" />}
          </button>
        </div>
      </div>
      <AnimatePresence>
        {open && (
          <motion.nav id="mobile-nav" aria-label="Main" className="xl:hidden overflow-hidden border-t border-line"
            initial={{ height: 0, opacity: 0 }} animate={{ height: "auto", opacity: 1 }} exit={{ height: 0, opacity: 0 }} transition={{ duration: .25 }}>
            <div className="flex flex-col gap-1 px-5 py-4 md:px-8">
              {links.map(l => <Link key={l.to} to={l.to} className="rounded-2xl px-3 py-3 text-[17px] font-medium hover:bg-cream">{l.label}</Link>)}
              <div className="mt-3 flex flex-wrap gap-2">
                <LanguageSelector className="inline-flex sm:hidden" />
                <Link to="/assistant" className="btn-green md:hidden">{t("get_help")}<ArrowRight className="size-4" /></Link>
              </div>
            </div>
          </motion.nav>
        )}
      </AnimatePresence>
    </header>
  );
}
