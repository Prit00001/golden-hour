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

  return (
    <header className="sticky top-0 z-40 border-b border-line bg-ivory/95 backdrop-blur-sm">
      <div className="mx-auto flex h-[68px] max-w-[1280px] items-center gap-6 px-5 md:px-8">
        <Logo />
        <nav className="hidden h-full items-center gap-7 xl:ml-10 xl:flex" aria-label="Main">
          {links.map(l => (
            <NavLink key={l.to} to={l.to} aria-current={active(l.to) ? "page" : undefined}
              className={`relative flex h-full items-center whitespace-nowrap text-[14px] transition-colors hover:text-ink
                after:absolute after:inset-x-0 after:bottom-[-1px] after:h-px after:bg-forest after:transition-transform after:duration-300
                ${active(l.to) ? "text-ink after:scale-x-100" : "text-stone after:scale-x-0 hover:after:scale-x-100 hover:after:bg-line"}`}>
              {l.label}
            </NavLink>
          ))}
        </nav>
        <div className="ml-auto flex items-center gap-1.5">
          <LanguageSelector className="hidden sm:inline-flex" />
          <Link to="/#help-now" className="grid size-9 place-items-center rounded-[6px] text-alert transition-colors hover:bg-ink/[.04]" aria-label={t("emergency_link")} title={t("emergency_link")}>
            <LifeBuoy className="size-[18px]" />
          </Link>
          <Link to="/assistant" className="btn-green ml-2 hidden !py-2 text-[14px] md:inline-flex">{t("get_help")}<ArrowRight className="size-4" /></Link>
          <button className="grid size-9 place-items-center rounded-[6px] text-ink hover:bg-ink/[.04] xl:hidden" onClick={() => setOpen(o => !o)}
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
              {links.map(l => <Link key={l.to} to={l.to} className="rounded-[6px] px-3 py-3 text-[17px] font-medium hover:bg-cream">{l.label}</Link>)}
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
