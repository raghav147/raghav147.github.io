import Link from 'next/link';
import type { Metadata } from 'next';
import { projects } from '@/data/projects';

export const metadata: Metadata = {
  title: 'Home',
  description: 'Welcome to Raghav’s portfolio featuring UX case studies and product design work.'
};

export default function HomePage() {
  return (
    <div className="space-y-14">
      <section className="space-y-5 rounded-2xl bg-white p-8 shadow-sm ring-1 ring-slate-200">
        <p className="text-sm font-medium uppercase tracking-[0.2em] text-accent">Product Designer</p>
        <h1 className="text-4xl font-bold leading-tight md:text-5xl">Designing thoughtful digital experiences with measurable impact.</h1>
        <p className="max-w-3xl text-lg text-slate-700">
          I help teams translate user needs into elegant products. My practice blends research, systems thinking, and rapid prototyping to ship experiences people trust.
        </p>
        <div className="flex flex-wrap gap-3">
          <Link href="/portfolio" className="rounded-md bg-ink px-4 py-2 font-medium text-white no-underline hover:bg-slate-800">
            View portfolio
          </Link>
          <Link href="/contact" className="rounded-md border border-slate-300 px-4 py-2 font-medium no-underline hover:border-accent hover:text-accent">
            Get in touch
          </Link>
        </div>
      </section>

      <section aria-labelledby="featured-work" className="space-y-5">
        <h2 id="featured-work" className="text-2xl font-semibold">Featured projects</h2>
        <div className="grid gap-6 md:grid-cols-2">
          {projects.map((project) => (
            <article key={project.slug} className="rounded-xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
              <p className="mb-2 text-sm text-slate-500">{project.timeline}</p>
              <h3 className="text-xl font-semibold">{project.title}</h3>
              <p className="mt-2 text-slate-700">{project.subtitle}</p>
              <div className="mt-4 flex flex-wrap gap-2">
                {project.tags.map((tag) => (
                  <span key={tag} className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700">
                    {tag}
                  </span>
                ))}
              </div>
              <Link href={`/portfolio/${project.slug}`} className="mt-5 inline-block font-medium text-accent hover:underline">
                Read case study
              </Link>
            </article>
          ))}
        </div>
      </section>
    </div>
  );
}
