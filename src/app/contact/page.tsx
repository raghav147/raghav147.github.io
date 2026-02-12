import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Contact',
  description: 'Get in touch with Raghav for design opportunities and collaborations.'
};

export default function ContactPage() {
  return (
    <section className="max-w-3xl space-y-6 rounded-2xl bg-white p-8 shadow-sm ring-1 ring-slate-200">
      <h1 className="text-3xl font-bold">Contact</h1>
      <p className="text-slate-700">
        I&apos;m currently open to full-time roles, contract work, and strategic design collaborations.
      </p>
      <ul className="space-y-3 text-slate-700">
        <li>
          Email:{' '}
          <a href="mailto:raghav@example.com" className="font-medium text-accent hover:underline">
            raghav@example.com
          </a>
        </li>
        <li>
          LinkedIn:{' '}
          <a href="https://www.linkedin.com" className="font-medium text-accent hover:underline">
            linkedin.com/in/raghav
          </a>
        </li>
        <li>
          Location: Remote / US
        </li>
      </ul>
    </section>
  );
}
