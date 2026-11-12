import { ExternalLink, Phone } from "lucide-react";

// Pinned to the bottom of the screen on every page, so 1930 and the official portal are always one tap away.
// English like the footer. The page gets matching bottom padding in App so nothing hides behind it.
export default function FooterBar() {
  return (
    <div lang="en" className="fixed inset-x-0 bottom-0 z-30 border-t border-line bg-cream/95 pb-[env(safe-area-inset-bottom)] backdrop-blur-md">
      <div className="mx-auto flex h-14 max-w-[1280px] items-center gap-3 px-5 text-[13px] md:px-8">
        <p className="mr-auto min-w-0 text-stone leading-tight">
          <span className="hidden md:inline">Golden Hour is not a government service. Always report through official channels.</span>
          <span className="md:hidden text-[12px]">Not a government<br />service.</span>
        </p>
        <a href="tel:1930" className="btn-red btn-sm shrink-0"><Phone className="size-3.5" />Call 1930</a>
        <a href="https://cybercrime.gov.in" target="_blank" rel="noopener noreferrer" className="btn-line btn-sm shrink-0">
          <span className="hidden sm:inline">cybercrime.gov.in</span><span className="sm:hidden">Portal</span><ExternalLink className="size-3.5" />
        </a>
      </div>
    </div>
  );
}
