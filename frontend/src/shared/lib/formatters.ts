export function formatRuntime(runtimeMinutes: number | null | undefined) {
  if (!runtimeMinutes) {
    return 'Runtime unavailable';
  }

  const hours = Math.floor(runtimeMinutes / 60);
  const minutes = runtimeMinutes % 60;

  if (hours === 0) {
    return `${minutes}m`;
  }

  return `${hours}h ${minutes}m`;
}

export function formatRating(rating: number | null | undefined) {
  if (rating == null) {
    return 'Not yet rated';
  }

  return `${rating.toFixed(1)} / 5`;
}

export function formatYearRange(
  year: number | null | undefined,
  yearMin?: number | null,
  yearMax?: number | null,
) {
  if (year) {
    return String(year);
  }

  if (yearMin && yearMax) {
    return `${yearMin}-${yearMax}`;
  }

  if (yearMin) {
    return `From ${yearMin}`;
  }

  if (yearMax) {
    return `Until ${yearMax}`;
  }

  return 'Any year';
}

export function formatDate(value: string) {
  return new Intl.DateTimeFormat(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  }).format(new Date(value));
}
