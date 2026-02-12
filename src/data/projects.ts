export type Project = {
  slug: string;
  title: string;
  subtitle: string;
  tags: string[];
  role: string;
  timeline: string;
  tools: string[];
  summary: string;
  problem: string;
  research: string;
  insights: string;
  concepts: string;
  prototype: string;
  outcome: string;
  reflections: string;
  images: string[];
  links?: {
    live?: string;
    repository?: string;
    caseStudy?: string;
  };
};

export const projects: Project[] = [
  {
    slug: 'finflow-mobile-banking-redesign',
    title: 'FinFlow Mobile Banking Redesign',
    subtitle: 'Simplifying goal-based savings journeys for young professionals.',
    tags: ['UX Research', 'Product Design', 'Prototyping'],
    role: 'Lead Product Designer',
    timeline: '12 weeks',
    tools: ['Figma', 'Miro', 'Maze', 'Notion'],
    summary:
      'A complete redesign of a mobile banking experience focused on reducing setup friction for automated savings goals.',
    problem:
      'The existing app had a 52% drop-off during savings goal creation, and customers struggled to understand how recurring transfers affected account balance.',
    research:
      'I interviewed 14 customers, analyzed support chat transcripts, and conducted a funnel review with analytics data from onboarding and transfer flows.',
    insights:
      'Users needed transparent transfer previews, plain language explanations, and nudges tied to pay-cycle habits instead of generic monthly reminders.',
    concepts:
      'We explored three concepts: wizard-style setup, conversational setup, and dashboard-first quick start. The final direction blended dashboard context with guided setup.',
    prototype:
      'Interactive high-fidelity prototypes were tested with 10 participants. Success rate increased from 48% to 90% for creating a first savings goal.',
    outcome:
      'Post-launch, completed goal setups grew by 37% and weekly active use of goal tracking rose by 22% over six weeks.',
    reflections:
      'Early collaboration with risk and compliance teams prevented rework. Next iteration should personalize suggestions based on spending categories.',
    images: ['/images/finflow-overview.svg', '/images/finflow-goal-flow.svg'],
    links: {
      caseStudy: '#',
      repository: '#'
    }
  },
  {
    slug: 'careloop-telehealth-experience',
    title: 'CareLoop Telehealth Experience',
    subtitle: 'Reducing anxiety during remote care appointments.',
    tags: ['Service Design', 'UI Design', 'Accessibility'],
    role: 'Senior UX Designer',
    timeline: '10 weeks',
    tools: ['FigJam', 'Figma', 'Dovetail', 'Zoom'],
    summary: 'A patient-facing telehealth product that improved appointment preparedness and follow-up adherence.',
    problem:
      'Patients frequently missed critical appointment prep steps and forgot care instructions after calls, leading to repeat support requests.',
    research:
      'Research included diary studies, clinician interviews, and accessibility audits focused on older adults and low-vision users.',
    insights:
      'Clear timeline cues and pre-visit checklists helped users feel in control, while concise post-visit summaries reduced confusion.',
    concepts:
      'We developed modular timeline components that support booking, prep, appointment, and follow-up states with high-contrast status indicators.',
    prototype:
      'Tested keyboard-first and screen-reader workflows with 6 participants, refining announcements and interactive states to improve accessibility.',
    outcome:
      'Prep completion improved by 41%, and satisfaction scores increased by 18 points in pilot clinics.',
    reflections:
      'Accessibility must be integrated from day one. Future versions should support multilingual reminders and caregiver collaboration.',
    images: ['/images/careloop-timeline.svg', '/images/careloop-summary.svg'],
    links: {
      live: '#'
    }
  }
];
