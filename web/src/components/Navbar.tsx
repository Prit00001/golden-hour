import { ArrowRight, ExternalLink, Phone } from "lucide-react";
import { Link, useLocation } from "react-router";
import { useI18n } from "../i18n/I18n";
import LanguageSelector from "./LanguageSelector";

// The only bar at the top: the emergency line, the official portal, language, and Get Help Now. Pages are linked
// from the footer and from the pages themselves.
export default function Navbar() {
  const { t } = useI18n();
  const { pathname } = useLocation();
  return (
    <div className="sticky top-0 z-40 bg-deep text-ivory">
      <div className="mx-auto flex h-12 max-w-[1280px] items-center gap-5 px-5 text-[13px] md:px-8">
        <a href="tel:1930" className="inline-flex items-center gap-1.5 font-medium underline-offset-4 hover:underline">
          <Phone className="size-3.5" /><span className="hidden whitespace-nowrap sm:inline">{t("call_short")}</span><span className="whitespace-nowrap sm:hidden">{t("em_call")}</span>
        </a>
        <a href="https://cybercrime.gov.in" target="_blank" rel="noopener noreferrer" className="hidden items-center gap-1 text-ivory/75 hover:text-ivory md:inline-flex">
          cybercrime.gov.in<ExternalLink className="size-3" />
        </a>
        <div className="ml-auto flex items-center gap-3">
          <LanguageSelector tone="dark" className="inline-flex" />
          {pathname !== "/assistant" && (
            <Link to="/assistant" className="inline-flex items-center gap-1.5 whitespace-nowrap rounded-[5px] bg-ivory px-3 py-1.5 text-[13px] font-medium text-deep transition-colors hover:bg-white">
              {t("get_help")}<ArrowRight className="size-3.5" />
            </Link>
          )}
        </div>
      </div>
    </div>
  );
}
