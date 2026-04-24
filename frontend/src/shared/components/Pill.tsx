import type { PropsWithChildren } from 'react';

type PillProps = PropsWithChildren<{
  tone?: 'default' | 'accent';
}>;

export function Pill({ tone = 'default', children }: PillProps) {
  return (
    <span
      className={[
        'inline-flex items-center rounded-full px-3 py-1 text-xs font-medium',
        tone === 'accent'
          ? 'bg-amber-100 text-amber-900'
          : 'bg-slate-100 text-slate-700',
      ].join(' ')}
    >
      {children}
    </span>
  );
}
