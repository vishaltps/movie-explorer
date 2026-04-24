import type { MovieListParams } from '../../features/movies/types';

function parsePositiveInt(value: string | null) {
  if (!value) {
    return undefined;
  }

  const parsed = Number.parseInt(value, 10);
  return Number.isNaN(parsed) || parsed <= 0 ? undefined : parsed;
}

export function readMovieListParams(
  searchParams: URLSearchParams,
): MovieListParams {
  return {
    search: searchParams.get('search') ?? undefined,
    genre_id: parsePositiveInt(searchParams.get('genre_id')),
    director_id: parsePositiveInt(searchParams.get('director_id')),
    actor_id: parsePositiveInt(searchParams.get('actor_id')),
    year: parsePositiveInt(searchParams.get('year')),
    year_min: parsePositiveInt(searchParams.get('year_min')),
    year_max: parsePositiveInt(searchParams.get('year_max')),
    sort: searchParams.get('sort') ?? undefined,
    page: parsePositiveInt(searchParams.get('page')) ?? 1,
    page_size: parsePositiveInt(searchParams.get('page_size')) ?? 12,
  };
}

export function writeSearchParams(
  current: URLSearchParams,
  patch: Record<string, string | number | undefined | null>,
) {
  const next = new URLSearchParams(current);

  for (const [key, value] of Object.entries(patch)) {
    if (value == null || value === '') {
      next.delete(key);
    } else {
      next.set(key, String(value));
    }
  }

  return next;
}
