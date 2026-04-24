import type { ReactNode } from 'react';

type ErrorStateProps = {
  title?: string;
  message: string;
  action?: ReactNode;
};

export function ErrorState({
  title = 'Something went wrong',
  message,
  action,
}: ErrorStateProps) {
  return (
    <div
      className="panel rounded-[1.75rem] border-red-300/80 bg-red-50/80 px-6 py-10 text-center"
      role="alert"
    >
      <h3 className="text-2xl font-semibold text-[color:var(--error)]">
        {title}
      </h3>
      <p className="mx-auto mt-3 max-w-xl text-[color:var(--muted)]">
        {message}
      </p>
      {action ? <div className="mt-5">{action}</div> : null}
    </div>
  );
}
