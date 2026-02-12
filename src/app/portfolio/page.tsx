import type { Metadata } from 'next';
import Link from 'next/link';
import { projects } from '@/data/projects';

export const metadata: Metadata = {
  title: 'Portfolio',
  description: 'Explore detailed portfolio case studies including process, outcomes, and lessons learned.'
};

export default function PortfolioPage() {
  return (
    <section className="space-y-6">
      <h1 className="text-3xl font-bold">Portfolio</h1>
      <p className="max-w-3xl text-slate-700">
        A curated collection of product design projects spanning fintech, healthcare, and digital services.
      </p>
      <div className="grid gap-6 md:grid-cols-2">
        {projects.map((project) => (
          <article key={project.slug} className="rounded-xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
            <h2 className="text-xl font-semibold">{project.title}</h2>
            <p className="mt-2 text-slate-700">{project.summary}</p>
            <p className="mt-3 text-sm text-slate-500">Role: {project.role}</p>
            <Link href={`/portfolio/${project.slug}`} className="mt-4 inline-block text-accent hover:underline">
              View project
            </Link>
          </article>
        ))}
      </div>
    </section>
  );
}
