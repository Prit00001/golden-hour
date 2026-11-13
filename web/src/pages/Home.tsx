import { ArrowRight } from "lucide-react";
import { Link } from "react-router";
import EmergencyHelp from "../components/EmergencyHelp";
import EvidenceChecklist from "../components/EvidenceChecklist";
import FraudCategories from "../components/FraudCategories";
import Hero from "../components/Hero";
import HowItWorks from "../components/HowItWorks";
import ImpactStats from "../components/ImpactStats";
import Photo from "../components/Photo";
import ResourceCard from "../components/ResourceCard";
import Reveal from "../components/Reveal";
import { useI18n } from "../i18n/I18n";
import { RESOURCES } from "../lib/data";

export default function Home() {
  const { t } = useI18n();
  return (
    <>
      <Hero />
      <ImpactStats />
      <EmergencyHelp />
      <FraudCategories />
      <HowItWorks />

      <section className="mx-auto max-w-[1280px] px-5 pt-24 md:px-8">
        <Reveal className="grid grid-cols-1 gap-8 lg:grid-cols-[minmax(0,1fr)_minmax(0,1.7fr)]">
          <div>
            <p className="eyebrow">{t("ev_eyebrow")}</p>
            <h2 className="mt-3 text-[clamp(2rem,3.6vw,2.9rem)] leading-[1.08] tracking-[-.012em]">{t("ev_h")}</h2>
          </div>
          <EvidenceChecklist />
        </Reveal>
      </section>

      <section className="mx-auto max-w-[1280px] px-5 pt-24 md:px-8">
        <Reveal className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <p className="eyebrow">{t("res_eyebrow")}</p>
            <h2 className="mt-3 max-w-xl text-[clamp(2rem,3.6vw,2.9rem)] leading-[1.08] tracking-[-.012em]">{t("res_h")}</h2>
          </div>
          <Link to="/resources" className="btn-line">{t("res_all")}<ArrowRight className="size-4" /></Link>
        </Reveal>
        <div className="mt-12 grid grid-cols-1 gap-x-10 gap-y-12 md:grid-cols-3">
          {RESOURCES.slice(0, 3).map((a, k) => <Reveal key={a.slug} delay={k * .08}><ResourceCard a={a} /></Reveal>)}
        </div>
      </section>

      <section className="band mt-24 border-t border-line">
        <Reveal className="mx-auto grid max-w-[1280px] grid-cols-1 items-center gap-10 px-5 py-20 md:px-8 lg:grid-cols-2 lg:gap-20">
          <Photo src="/images/about.jpg" alt="A son helping his father with his phone" tone={1} className="aspect-[4/3] w-full rounded-[12px]" />
          <div>
            <p className="eyebrow">{t("about_eyebrow")}</p>
            <h2 className="mt-3 text-[clamp(2rem,3.6vw,2.9rem)] leading-[1.08] tracking-[-.012em]">{t("about_h")}</h2>
            <p className="mt-5 text-[17px] leading-relaxed text-stone">{t("about_p")}</p>
            <Link to="/about" className="btn-line mt-8">{t("about_more")}<ArrowRight className="size-4" /></Link>
          </div>
        </Reveal>
      </section>
    </>
  );
}
