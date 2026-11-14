import { ArrowRight } from "lucide-react";
import { Link } from "react-router";
import { useI18n } from "../i18n/I18n";
import Photo from "./Photo";

// One photograph, in the page's own width, with the call to action laid over it. AI-generated for Golden Hour
// (see web/public/images/README.md).
export default function HeroPhoto() {
  const { t } = useI18n();
  return (
    <div className="mx-auto max-w-[1280px] px-5 md:px-8">
      <div className="relative h-[clamp(320px,min(44vw,48vh),580px)] overflow-hidden rounded-[10px] bg-cream">
        <Photo src="/images/hero-1.jpg" alt="A woman on a phone call at home, taking notes as she gets guidance" tone={0}
          className="size-full" priority="high" />
        <div className="absolute bottom-4 left-4 right-4 rounded-[8px] border border-line bg-paper p-5 md:bottom-7 md:left-7 md:right-auto md:w-[360px]">
          <p className="font-display text-[21px] leading-tight">{t("float_t")}</p>
          <p className="mt-1 text-[14px] text-stone">{t("float_p")}</p>
          <Link to="/assistant" className="btn-green mt-4 w-full sm:w-auto">{t("start")}<ArrowRight className="size-4" /></Link>
        </div>
      </div>
    </div>
  );
}
