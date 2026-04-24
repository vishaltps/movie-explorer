import type { PropsWithChildren, ReactNode } from 'react';

type PageSectionProps = PropsWithChildren<{
  eyebrow?: string;
  title: string;
  description?: string;
  actions?: ReactNode;
}>;

export function PageSection({
  eyebrow,
  title,
  description,
  actions,
  children,
}: PageSectionProps) {
  return (
    <section className="mb-8">
      <div className="mb-4 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          {eyebrow ? (
            <p className="text-xs uppercase tracking-[0.3em] text-[color:var(--accent)]">
              {eyebrow}
            </p>
          ) : null}
          <h2 className="mt-2 text-3xl font-semibold tracking-tight">
            {title}
          </h2>
          {description ? (
            <p className="mt-2 max-w-2xl text-[color:var(--muted)]">
              {description}
            </p>
          ) : null}
        </div>
        {actions ? <div>{actions}</div> : null}
      </div>
      {children}
    </section>
  );
}
