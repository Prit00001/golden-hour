import { ArrowRight, ExternalLink, Info, Phone } from "lucide-react";
import { Link } from "react-router";
import { useI18n } from "../i18n/I18n";
import Reveal from "./Reveal";

export default function EmergencyHelp() {
  const { t } = useI18n();
  return (
    <section id="help-now" className="mx-auto max-w-[1280px] px-5 pt-24 md:px-8">
      <Reveal className="rounded-[32px] bg-cream p-6 md:p-10">
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-[minmax(0,1fr)_minmax(0,2fr)] lg:gap-10">
          <div>
            <p className="eyebrow !text-alert">1930 · cybercrime.gov.in</p>
            <h2 className="mt-3 text-[clamp(2rem,4vw,3rem)] font-extrabold leading-[1.05] tracking-[-.03em]">{t("em_h")}</h2>
            <p className="mt-4 text-[16px] leading-relaxed text-stone">{t("em_p")}</p>
          </div>
          <div className="grid gap-4 sm:grid-cols-3">
            <div className="flex flex-col rounded-[24px] bg-alert p-5 text-ivory">
              <p className="text-[14px] font-medium opacity-90">{t("em_1930_t")}</p>
              <p className="mt-2 font-display text-[52px] font-extrabold leading-none tracking-tight">1930</p>
              <a href="tel:1930" className="btn mt-auto bg-ivory pt-3 text-alert hover:bg-white"><Phone className="size-4" />{t("em_call")}</a>
            </div>
            <div className="flex flex-col rounded-[24px] border border-line bg-ivory p-5">
              <p className="text-[14px] font-medium text-stone">{t("em_portal_t")}</p>
              <p className="mt-2 [overflow-wrap:anywhere] font-display text-[20px] font-bold leading-tight">cybercrime.gov.in</p>
              <a href="https://cybercrime.gov.in" target="_blank" rel="noopener noreferrer" className="btn-dark mt-6 sm:mt-auto">{t("em_portal_b")}<ExternalLink className="size-4" /></a>
            </div>
            <div className="flex flex-col rounded-[24px] bg-mint p-5">
              <p className="text-[14px] font-medium text-forest">{t("em_bank_t")}</p>
              <p className="mt-2 text-[15px] leading-snug">{t("em_bank_p")}</p>
              <Link to="/bank-email" className="btn-green mt-6">{t("em_bank_b")}<ArrowRight className="size-4" /></Link>
            </div>
          </div>
        </div>
        <p className="mt-8 flex gap-2.5 border-t border-line pt-5 text-[13px] leading-relaxed text-stone">
          <Info className="mt-0.5 size-4 shrink-0" />{t("disclaimer")}
        </p>
      </Reveal>
    </section>
  );
}
