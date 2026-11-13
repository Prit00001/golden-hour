import { Accessibility, ArrowRight, BrainCircuit, Heart, Languages, ShieldCheck } from "lucide-react";
import { Link } from "react-router";
import NotTranslated from "../components/NotTranslated";
import Photo from "../components/Photo";
import Reveal from "../components/Reveal";
import { useI18n } from "../i18n/I18n";

const VALUES = [
  { icon: Accessibility, h: "Accessibility", p: "Large type, plain words and voice input, so it works for someone who has never filed a complaint or doesn't read English." },
  { icon: Heart, h: "Empathy", p: "People arrive frightened and ashamed. We ask one thing at a time, never blame, and tell them clearly what to do first." },
  { icon: ShieldCheck, h: "Digital awareness", p: "Every answer also teaches the warning signs, so the same trick doesn't work twice." },
  { icon: Languages, h: "Multilingual inclusion", p: "The assistant speaks and understands Hindi, English, Bengali, Kannada, Tamil, Telugu and Marathi, and code-mixed Hinglish." },
  { icon: BrainCircuit, h: "Responsible AI", p: "Steps and complaint wording are fixed and reviewed, never made up. IDs are read back for you to confirm. Nothing you say is stored after the call." },
];

export default function About() {
  const { t } = useI18n();
  return (
    <div className="mx-auto max-w-[1280px] px-5 pb-24 pt-12 md:px-8 md:pt-16" lang="en">
      <NotTranslated />
      <Reveal className="grid grid-cols-1 gap-10 lg:grid-cols-[minmax(0,1.2fr)_minmax(0,1fr)] lg:items-end">
        <div>
          <p className="eyebrow">About us</p>
          <h1 className="mt-4 text-[clamp(2.4rem,6vw,4.75rem)] leading-[1.06] tracking-[-.012em]">We believe no one should face financial fraud alone.</h1>
        </div>
        <p className="text-[17px] leading-relaxed text-stone">Golden Hour was created to bridge the gap between experiencing financial fraud and knowing what to do next. We aim to make reporting guidance, complaint preparation and digital safety assistance accessible to everyone, regardless of their language or technical knowledge.</p>
      </Reveal>
      <Reveal className="mt-12"><Photo src="/images/about.jpg" alt="A son helping his father with his phone" tone={2} className="aspect-[16/7] w-full rounded-[12px]" />
        <p className="mt-2 text-[12px] text-stone">Illustrative image, AI-generated. The people shown are not real.</p></Reveal>

      <Reveal className="mx-auto mt-20 max-w-3xl">
        <h2 className="text-[28px] font-bold leading-tight">Why the first hour</h2>
        <div className="mt-4 grid gap-4 text-[17px] leading-relaxed text-stone">
          <p>When money is stolen over UPI or a bank transfer, it is usually moved on through several accounts within hours. India's 1930 helpline can ask banks to hold it — but only while it is still there.</p>
          <p>Most people spend that time panicking. They don't know whom to call first, can't find the transaction ID, and when they finally reach someone, they can't give the details fast enough. Golden Hour is built for that moment: it tells you what to do first, gathers exactly what 1930 and your bank will ask for, and hands you the complaint ready to send.</p>
          <p>It does not file anything, contact your bank, or promise your money back. It gets you to the right people faster, with the right details.</p>
        </div>
      </Reveal>

      <div className="mt-20 grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
        {VALUES.map((v, k) => (
          <Reveal key={v.h} delay={k * .06} className="card p-6">
            <v.icon className="size-6 text-forest" strokeWidth={1.5} />
            <h3 className="mt-5 text-[20px] font-bold">{v.h}</h3>
            <p className="mt-2 text-[15px] leading-relaxed text-stone">{v.p}</p>
          </Reveal>
        ))}
        <Reveal delay={.3} className="flex flex-col justify-between rounded-[8px] bg-ink p-6 text-ivory">
          <p className="font-display text-[24px] font-bold leading-snug">{t("foot_tag")}</p>
          <Link to="/assistant" className="btn mt-6 self-start bg-gold text-ink hover:bg-[#c9a66b]">{t("get_help")}<ArrowRight className="size-4" /></Link>
        </Reveal>
      </div>
    </div>
  );
}
