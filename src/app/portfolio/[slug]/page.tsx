import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import Link from 'next/link';
import { projects } from '@/data/projects';

type ProjectPageProps = {
  params: {
    slug: string;
  };
};

export function generateStaticParams() {
  return projects.map((project) => ({ slug: project.slug }));
}

export function generateMetadata({ params }: ProjectPageProps): Metadata {
  const project = projects.find((entry) => entry.slug === params.slug);

  if (!project) {
    return {
      title: 'Project not found',
      description: 'The selected project could not be found.'
    };
  }

  return {
    title: project.title,
    description: project.subtitle
  };
}

export default function ProjectPage({ params }: ProjectPageProps) {
  const project = projects.find((entry) => entry.slug === params.slug);

  if (!project) {
    notFound();
  }

  const sections = [
    { heading: 'Problem', body: project.problem },
    { heading: 'Research', body: project.research },
    { heading: 'Insights', body: project.insights },
    { heading: 'Concepts', body: project.concepts },
    { heading: 'Prototype', body: project.prototype },
    { heading: 'Outcome', body: project.outcome },
    { heading: 'Reflections', body: project.reflections }
  ];

  return (
    <article className="space-y-8 rounded-2xl bg-white p-8 shadow-sm ring-1 ring-slate-200">
      <div className="space-y-3">
        <p className="text-sm font-medium uppercase tracking-wide text-accent">{project.timeline}</p>
        <h1 className="text-3xl font-bold">{project.title}</h1>
        <p className="text-lg text-slate-700">{project.subtitle}</p>
      </div>

      <dl className="grid gap-4 rounded-xl bg-slate-50 p-5 md:grid-cols-3">
        <div>
          <dt className="text-sm font-semibold text-slate-600">Role</dt>
          <dd>{project.role}</dd>
        </div>
        <div>
          <dt className="text-sm font-semibold text-slate-600">Tools</dt>
          <dd>{project.tools.join(', ')}</dd>
        </div>
        <div>
          <dt className="text-sm font-semibold text-slate-600">Tags</dt>
          <dd>{project.tags.join(', ')}</dd>
        </div>
      </dl>

      <section className="prose-content max-w-none">
        <h2 className="text-2xl font-semibold">Summary</h2>
        <p>{project.summary}</p>
        {sections.map((section) => (
          <div key={section.heading}>
            <h2>{section.heading}</h2>
            <p>{section.body}</p>
          </div>
        ))}
      </section>

      {project.links && (
        <section aria-label="Project links" className="flex flex-wrap gap-4">
          {project.links.live && (
            <Link href={project.links.live} className="font-medium text-accent hover:underline">
              Live experience
            </Link>
          )}
          {project.links.repository && (
            <Link href={project.links.repository} className="font-medium text-accent hover:underline">
              Repository
            </Link>
          )}
          {project.links.caseStudy && (
            <Link href={project.links.caseStudy} className="font-medium text-accent hover:underline">
              Full case study
            </Link>
          )}
        </section>
      )}

      <Link href="/portfolio" className="inline-block font-medium text-accent hover:underline">
        ← Back to portfolio
      </Link>
    </article>
  );
}
