type SpinnerProps = {
  label?: string;
  className?: string;
};

export function Spinner({ label = 'Loading', className = '' }: SpinnerProps) {
  return (
    <div
      className={`flex flex-col items-center justify-center gap-4 ${className}`}
    >
      <div
        aria-hidden="true"
        className="h-10 w-10 animate-spin rounded-full border-4 border-amber-200 border-t-amber-700"
      />
      <p className="text-sm text-[color:var(--muted)]">{label}</p>
    </div>
  );
}
