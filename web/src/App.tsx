import { MotionConfig } from "framer-motion";
import { useEffect } from "react";
import { Route, Routes, useLocation } from "react-router";
import Footer from "./components/Footer";
import Navbar from "./components/Navbar";
import About from "./pages/About";
import Assistant from "./pages/Assistant";
import ComplaintGenerator from "./pages/ComplaintGenerator";
import Home from "./pages/Home";
import { Legal, NotFound } from "./pages/Legal";
import Resources, { Article } from "./pages/Resources";

export default function App() {
  const { pathname, hash } = useLocation();
  useEffect(() => {  // new page: start at the top, or at the #section the link points to
    if (hash) document.getElementById(hash.slice(1))?.scrollIntoView();
    else window.scrollTo({ top: 0, behavior: "instant" });  // not the CSS smooth scroll: a new page starts at the top
  }, [pathname, hash]);

  return (
    <MotionConfig reducedMotion="user">
      {/* The site sits on an ivory sheet inside a beige frame, like a printed page. */}
      <div className="mx-auto max-w-[1400px] bg-ivory md:my-3 md:rounded-[32px] md:shadow-[0_1px_0_#0000000a,0_30px_60px_-30px_#25251f33] overflow-clip">
        <Navbar />
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/assistant" element={<Assistant />} />
            <Route path="/complaint-generator" element={<ComplaintGenerator mode="complaint" />} />
            <Route path="/bank-email" element={<ComplaintGenerator mode="bank" />} />
            <Route path="/resources" element={<Resources />} />
            <Route path="/resources/:slug" element={<Article />} />
            <Route path="/about" element={<About />} />
            <Route path="/privacy" element={<Legal kind="privacy" />} />
            <Route path="/terms" element={<Legal kind="terms" />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </MotionConfig>
  );
}
