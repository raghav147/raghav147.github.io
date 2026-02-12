import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'About',
  description: 'Learn about Raghav, design values, and approach to product design.'
};

export default function AboutPage() {
  return (
    <section className="prose-content max-w-3xl rounded-2xl bg-white p-8 shadow-sm ring-1 ring-slate-200">
      <h1 className="text-3xl font-bold">About me</h1>
      <p>
        I&apos;m a product designer with a focus on solving complex workflow and service challenges. I partner closely with product managers, engineers, and stakeholders to shape high-impact experiences from discovery through delivery.
      </p>
      <h2>How I work</h2>
      <p>
        I use an iterative process grounded in user research, prototyping, and measurable outcomes. My approach balances systems-level thinking with attention to details that make interfaces feel intuitive and inclusive.
      </p>
      <h2>Values</h2>
      <p>
        Clarity over complexity, accessibility by default, and design decisions rooted in evidence. I enjoy mentoring teams, facilitating workshops, and translating ambiguity into clear product direction.
      </p>
    </section>
  );
}
