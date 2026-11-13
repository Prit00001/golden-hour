import { Link } from "react-router";
import NotTranslated from "../components/NotTranslated";

const PAGES = {
  privacy: { title: "Privacy Policy", body: [
    ["What we keep", "Nothing about your case. During a voice call, your audio is streamed to Gnani.ai to be transcribed and your replies are spoken back; the details you give live only in your browser tab and the open connection, and are gone when the call ends or you close the page. Server logs record timings only, never what you said."],
    ["The complaint and email generators", "These run entirely in your browser. The name, contact details and incident description you type are never sent to our server."],
    ["In your browser", "We remember your chosen language, the evidence items you've ticked and anything you enter in the follow-up tracker, in your browser's local storage, so they're still there next time. Clearing your browser data removes them."],
    ["Sharing with family", "The share and WhatsApp buttons on your action plan send your case summary only when you tap them, to the person you choose. We never send it anywhere ourselves."],
    ["No tracking", "No analytics, advertising or third-party scripts. Fonts are served from our own server."],
    ["Never share secrets", "We will never ask for your OTP, PIN, CVV, card number or passwords. Don't type them anywhere on this site."],
  ] },
  terms: { title: "Terms of Use", body: [
    ["What this is", "Golden Hour gives information and AI-assisted guidance after financial fraud. It is not a government portal, bank, law enforcement agency or legal service, and it is not affiliated with any of them."],
    ["What it doesn't do", "It does not file complaints, contact your bank, freeze accounts or recover money. You submit complaints yourself through official channels: the 1930 helpline, cybercrime.gov.in and your bank."],
    ["Check every draft", "Drafts are generated from what you enter and may contain mistakes. Read and correct them before you send or submit anything."],
    ["No guarantee", "Following these steps doesn't guarantee your money will be recovered. Guidance may change as official procedures change; always follow what official channels tell you."],
    ["Fair use", "Please don't misuse the service or try to overload it. Usage limits protect it for people who need it."],
  ] },
};

export function Legal({ kind }: { kind: keyof typeof PAGES }) {
  const page = PAGES[kind];
  return (
    <div className="mx-auto max-w-3xl px-5 pb-24 pt-12 md:pt-16" lang="en">
      <NotTranslated />
      <h1 className="text-[clamp(2.2rem,5vw,3.5rem)] tracking-[-.012em]">{page.title}</h1>
      <p className="mt-2 text-[14px] text-stone">Last updated 12 November 2026</p>
      <div className="mt-10 grid gap-8">
        {page.body.map(([h, p]) => <section key={h}><h2 className="text-[23px]">{h}</h2><p className="mt-2 text-[17px] leading-relaxed text-stone">{p}</p></section>)}
      </div>
    </div>
  );
}

export function NotFound() {
  return (
    <div className="mx-auto grid max-w-xl place-items-center px-5 py-32 text-center">
      <p className="font-display text-[80px] font-medium leading-none text-gold">404</p>
      <h1 className="mt-4 text-[28px] font-bold">This page doesn't exist.</h1>
      <p className="mt-2 text-stone">If you need help with a fraud right now, call 1930.</p>
      <div className="mt-6 flex gap-3"><Link to="/" className="btn-line">Home</Link><a href="tel:1930" className="btn-red">Call 1930</a></div>
    </div>
  );
}
