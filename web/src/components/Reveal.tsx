import { motion } from "framer-motion";
import type { ReactNode } from "react";

// Fade up once when scrolled into view. MotionConfig reducedMotion="user" turns this off for people who ask.
export default function Reveal({ children, delay = 0, className = "" }: { children: ReactNode; delay?: number; className?: string }) {
  return (
    <motion.div className={className} initial={{ opacity: 0, y: 24 }} whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-60px" }} transition={{ duration: .6, delay, ease: [.22, 1, .36, 1] }}>
      {children}
    </motion.div>
  );
}
