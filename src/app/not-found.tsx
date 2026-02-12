import Link from 'next/link';

export default function NotFound() {
  return (
    <section className="space-y-4 rounded-2xl bg-white p-8 text-center shadow-sm ring-1 ring-slate-200">
      <h1 className="text-3xl font-bold">Project not found</h1>
      <p className="text-slate-700">The page you are looking for does not exist or has moved.</p>
      <Link href="/portfolio" className="font-medium text-accent hover:underline">
        Back to portfolio
      </Link>
    </section>
  );
}
