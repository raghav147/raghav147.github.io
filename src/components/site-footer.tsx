export function SiteFooter() {
  return (
    <footer className="mt-16 border-t border-slate-200 bg-white">
      <div className="mx-auto flex w-full max-w-6xl flex-col justify-between gap-2 px-6 py-8 text-sm text-slate-600 md:flex-row">
        <p>© {new Date().getFullYear()} Raghav. All rights reserved.</p>
        <p>Built with Next.js + Tailwind CSS.</p>
      </div>
    </footer>
  );
}
