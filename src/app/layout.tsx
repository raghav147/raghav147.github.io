import type { Metadata } from 'next';
import './globals.css';
import { SiteNav } from '@/components/site-nav';
import { SiteFooter } from '@/components/site-footer';

export const metadata: Metadata = {
  title: {
    default: 'Raghav | Product Designer Portfolio',
    template: '%s | Raghav Portfolio'
  },
  description:
    'Portfolio website showcasing product design case studies, process, and outcomes by Raghav.',
  openGraph: {
    title: 'Raghav | Product Designer Portfolio',
    description:
      'Portfolio website showcasing product design case studies, process, and outcomes by Raghav.',
    type: 'website'
  }
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen">
        <a href="#main-content" className="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:bg-white focus:p-2">
          Skip to content
        </a>
        <SiteNav />
        <main id="main-content" className="mx-auto w-full max-w-6xl px-6 py-10">
          {children}
        </main>
        <SiteFooter />
      </body>
    </html>
  );
}
