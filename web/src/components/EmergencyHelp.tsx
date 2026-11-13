import { ArrowRight, ExternalLink, Info, Phone } from "lucide-react";
import { Link } from "react-router";
import { useI18n } from "../i18n/I18n";
import Reveal from "./Reveal";

export default function EmergencyHelp() {
  const { t } = useI18n();
  return (
    <section id="help-now" className="band mt-20 border-y border-line">
      <Reveal className="mx-auto max-w-[1280px] px-5 py-16 md:px-8 md:py-20">
        <div className="grid grid-cols-1 gap-10 lg:grid-cols-[minmax(0,1fr)_minmax(0,2fr)] lg:gap-16">
          <div>
            <p className="eyebrow !text-alert">1930 · cybercrime.gov.in</p>
            <h2 className="mt-3 text-[clamp(2rem,3.6vw,2.9rem)] leading-[1.08] tracking-[-.012em]">{t("em_h")}</h2>
            <p className="mt-4 text-[16px] leading-relaxed text-stone">{t("em_p")}</p>
          </div>
          {/* Three options side by side, split by rules; red is kept for the emergency number alone. */}
          <div className="grid grid-cols-1 border-t border-line sm:grid-cols-3 sm:border-t-0">
            <div className="flex flex-col border-b border-line py-6 sm:border-b-0 sm:border-r sm:py-0 sm:pr-7">
              <p className="text-[14px] text-stone">{t("em_1930_t")}</p>
              <p className="mt-2 font-display text-[56px] leading-none text-alert">1930</p>
              <a href="tel:1930" className="btn-red mt-6 self-start sm:mt-auto"><Phone className="size-4" />{t("em_call")}</a>
            </div>
            <div className="flex flex-col border-b border-line py-6 sm:border-b-0 sm:border-r sm:px-7 sm:py-0">
              <p className="text-[14px] text-stone">{t("em_portal_t")}</p>
              <p className="mt-3 [overflow-wrap:anywhere] font-display text-[26px] leading-tight">cybercrime.gov.in</p>
              <a href="https://cybercrime.gov.in" target="_blank" rel="noopener noreferrer" className="btn-line mt-6 self-start sm:mt-auto">{t("em_portal_b")}<ExternalLink className="size-4" /></a>
            </div>
            <div className="flex flex-col py-6 sm:py-0 sm:pl-7">
              <p className="text-[14px] text-stone">{t("em_bank_t")}</p>
              <p className="mt-3 text-[15px] leading-relaxed">{t("em_bank_p")}</p>
              <Link to="/bank-email" className="btn-green mt-6 self-start sm:mt-auto">{t("em_bank_b")}<ArrowRight className="size-4" /></Link>
            </div>
          </div>
        </div>
        <p className="mt-12 flex gap-2.5 border-t border-line pt-5 text-[13px] leading-relaxed text-stone">
          <Info className="mt-0.5 size-4 shrink-0" />{t("disclaimer")}
        </p>
      </Reveal>
    </section>
  );
}
