import Link from 'next/link';

const navItems = [
  { href: '/', label: 'Home' },
  { href: '/about', label: 'About' },
  { href: '/portfolio', label: 'Portfolio' },
  { href: '/contact', label: 'Contact' }
];

export function SiteNav() {
  return (
    <header className="border-b border-slate-200 bg-white/90 backdrop-blur-sm">
      <div className="mx-auto flex w-full max-w-6xl items-center justify-between px-6 py-4">
        <Link href="/" className="text-lg font-semibold no-underline">
          Raghav Portfolio
        </Link>
        <nav aria-label="Primary" className="flex gap-5 text-sm md:text-base">
          {navItems.map((item) => (
            <Link key={item.href} href={item.href} className="no-underline hover:text-accent focus-visible:text-accent">
              {item.label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}
