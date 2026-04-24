const FAVORITES_KEY = 'movie-explorer:favorites';

export type StoredFavorite = {
  id: number;
  title: string;
  release_year: number;
  poster_url: string | null;
  average_rating: number | null;
};

function isStoredFavorite(value: unknown): value is StoredFavorite {
  if (typeof value !== 'object' || value === null) {
    return false;
  }

  const record = value as Record<string, unknown>;
  return (
    typeof record.id === 'number' &&
    typeof record.title === 'string' &&
    typeof record.release_year === 'number'
  );
}

export function readFavorites() {
  if (typeof window === 'undefined') {
    return [] as StoredFavorite[];
  }

  try {
    const raw = window.localStorage.getItem(FAVORITES_KEY);
    if (!raw) {
      return [] as StoredFavorite[];
    }

    const parsed = JSON.parse(raw) as unknown;
    if (!Array.isArray(parsed)) {
      return [] as StoredFavorite[];
    }

    return parsed.filter(isStoredFavorite);
  } catch {
    return [] as StoredFavorite[];
  }
}

export function writeFavorites(favorites: StoredFavorite[]) {
  if (typeof window === 'undefined') {
    return;
  }

  window.localStorage.setItem(FAVORITES_KEY, JSON.stringify(favorites));
  window.dispatchEvent(new Event('movie-explorer:favorites-updated'));
}

export const favoritesStorageKey = FAVORITES_KEY;
