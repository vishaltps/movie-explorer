import { Pill } from '../../../shared/components/Pill';

type ActiveFiltersProps = {
  filters: Array<{ key: string; label: string }>;
  onClear: (key: string) => void;
  onClearAll: () => void;
};

export function ActiveFilters({
  filters,
  onClear,
  onClearAll,
}: ActiveFiltersProps) {
  if (filters.length === 0) {
    return null;
  }

  return (
    <div className="mt-4 flex flex-wrap items-center gap-2">
      {filters.map((filter) => (
        <button
          key={filter.key}
          onClick={() => onClear(filter.key)}
          type="button"
        >
          <Pill tone="accent">{filter.label} ×</Pill>
        </button>
      ))}
      <button
        className="text-sm text-[color:var(--muted)] underline decoration-dotted"
        onClick={onClearAll}
        type="button"
      >
        Clear all
      </button>
    </div>
  );
}
