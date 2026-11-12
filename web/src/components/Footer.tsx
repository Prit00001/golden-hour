import { ExternalLink, Phone } from "lucide-react";
import { Link } from "react-router";
import en from "../i18n/en";
import Logo from "./Logo";

export default function Footer() {
  const t = (k: keyof typeof en) => en[k] as string;  // the footer stays in English whatever language is picked
  const links: [string, string][] = [["/", t("nav_home")], ["/#how-it-works", t("nav_how")], ["/assistant", t("get_help_short")],
    ["/resources", t("nav_res")], ["/about", t("nav_about")], ["/privacy", t("privacy")], ["/terms", t("terms")]];
  return (
    <footer className="bg-cream" lang="en">
      <div className="mx-auto grid grid-cols-1 max-w-[1280px] gap-10 px-5 py-14 md:px-8 md:grid-cols-[minmax(0,1.4fr)_1fr_minmax(0,1fr)]">
        <div>
          <Logo />
          <p className="mt-4 max-w-xs font-display text-[22px] font-bold leading-snug">{t("foot_tag")}</p>
        </div>
        <div>
          <h2 className="eyebrow">{t("foot_explore")}</h2>
          <ul className="mt-4 grid gap-2 text-[15px]">
            {links.map(([to, label]) => <li key={to}><Link to={to} className="text-stone hover:text-ink">{label}</Link></li>)}
          </ul>
        </div>
        <div>
          <h2 className="eyebrow">{t("foot_official")}</h2>
          <ul className="mt-4 grid gap-3 text-[15px]">
            <li><a href="tel:1930" className="inline-flex items-center gap-2 font-semibold text-alert hover:underline"><Phone className="size-4" />{t("foot_helpline")}: 1930</a></li>
            <li><a href="https://cybercrime.gov.in" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 font-semibold hover:underline">
              {t("foot_portal")}: cybercrime.gov.in<ExternalLink className="size-3.5" /></a></li>
          </ul>
        </div>
      </div>
      <div className="mx-auto max-w-[1280px] border-t border-line px-5 py-6 md:px-8">
        <p className="max-w-4xl text-[13px] leading-relaxed text-stone">{t("foot_disclaimer")}</p>
        <p className="mt-3 text-[13px] text-stone">© 2026 Golden Hour · Built on Gnani.ai Prisma + Timbre</p>
      </div>
    </footer>
  );
}
