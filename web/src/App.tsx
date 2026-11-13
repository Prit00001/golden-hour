import { MotionConfig, motion } from "framer-motion";
import { lazy, Suspense, useEffect } from "react";
import { Route, Routes, useLocation } from "react-router";
import Footer from "./components/Footer";
import FooterBar from "./components/FooterBar";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";

// Home ships in the main bundle; every other page loads the first time it's opened.
const Assistant = lazy(() => import("./pages/Assistant"));
const ComplaintGenerator = lazy(() => import("./pages/ComplaintGenerator"));
const Resources = lazy(() => import("./pages/Resources"));
const Article = lazy(() => import("./pages/Resources").then(m => ({ default: m.Article })));
const About = lazy(() => import("./pages/About"));
const Track = lazy(() => import("./pages/Track"));
const Legal = lazy(() => import("./pages/Legal").then(m => ({ default: m.Legal })));
const NotFound = lazy(() => import("./pages/Legal").then(m => ({ default: m.NotFound })));

export default function App() {
  const { pathname, hash } = useLocation();
  useEffect(() => {  // new page: start at the top, or at the #section the link points to
    if (hash) document.getElementById(hash.slice(1))?.scrollIntoView();
    else window.scrollTo({ top: 0, behavior: "instant" });  // not the CSS smooth scroll: a new page starts at the top
  }, [pathname, hash]);

  return (
    <MotionConfig reducedMotion="user">
      {/* The site sits on an ivory sheet inside a beige frame, like a printed page. */}
      <div className="mx-auto mb-[calc(3.5rem+env(safe-area-inset-bottom))] max-w-[1400px] bg-ivory md:mt-3 md:rounded-[32px] md:shadow-[0_1px_0_#0000000a,0_30px_60px_-30px_#25251f33] overflow-clip">
        <Navbar />
        <main className="min-h-[60vh]">
          <Suspense fallback={<div className="min-h-[60vh]" aria-busy="true" />}>
            {/* Each page fades in on arrival; keyed by path so it replays on every navigation. */}
            <motion.div key={pathname} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: .4, ease: [.22, 1, .36, 1] }}>
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/assistant" element={<Assistant />} />
                <Route path="/complaint-generator" element={<ComplaintGenerator mode="complaint" />} />
                <Route path="/bank-email" element={<ComplaintGenerator mode="bank" />} />
                <Route path="/resources" element={<Resources />} />
                <Route path="/resources/:slug" element={<Article />} />
                <Route path="/about" element={<About />} />
                <Route path="/track" element={<Track />} />
                <Route path="/privacy" element={<Legal kind="privacy" />} />
                <Route path="/terms" element={<Legal kind="terms" />} />
                <Route path="*" element={<NotFound />} />
              </Routes>
            </motion.div>
          </Suspense>
        </main>
        <Footer />
      </div>
      <FooterBar />
    </MotionConfig>
  );
}
