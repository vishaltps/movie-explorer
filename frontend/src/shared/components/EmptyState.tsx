import type { ReactNode } from 'react';

type EmptyStateProps = {
  title: string;
  message: string;
  action?: ReactNode;
};

export function EmptyState({ title, message, action }: EmptyStateProps) {
  return (
    <div className="panel rounded-[1.75rem] px-6 py-10 text-center">
      <h3 className="text-2xl font-semibold">{title}</h3>
      <p className="mx-auto mt-3 max-w-xl text-[color:var(--muted)]">
        {message}
      </p>
      {action ? <div className="mt-5">{action}</div> : null}
    </div>
  );
}
