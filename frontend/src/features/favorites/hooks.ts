import { useEffect, useMemo, useState } from 'react';

import {
  readFavorites,
  writeFavorites,
  type StoredFavorite,
} from '../../shared/lib/localStorage';
import type { MovieRead } from '../../shared/types';

function toFavorite(
  movie: Pick<
    MovieRead,
    'id' | 'title' | 'release_year' | 'poster_url' | 'average_rating'
  >,
): StoredFavorite {
  return {
    id: movie.id,
    title: movie.title,
    release_year: movie.release_year,
    poster_url: movie.poster_url ?? null,
    average_rating: movie.average_rating ?? null,
  };
}

export function useFavorites() {
  const [favorites, setFavorites] = useState<StoredFavorite[]>(() =>
    readFavorites(),
  );

  useEffect(() => {
    const sync = () => setFavorites(readFavorites());
    window.addEventListener('movie-explorer:favorites-updated', sync);
    window.addEventListener('storage', sync);
    return () => {
      window.removeEventListener('movie-explorer:favorites-updated', sync);
      window.removeEventListener('storage', sync);
    };
  }, []);

  const favoriteIds = useMemo(
    () => new Set(favorites.map((favorite) => favorite.id)),
    [favorites],
  );

  const toggleFavorite = (
    movie: Pick<
      MovieRead,
      'id' | 'title' | 'release_year' | 'poster_url' | 'average_rating'
    >,
  ) => {
    const exists = favoriteIds.has(movie.id);
    const next = exists
      ? favorites.filter((favorite) => favorite.id !== movie.id)
      : [toFavorite(movie), ...favorites];
    writeFavorites(next);
    setFavorites(next);
  };

  return {
    favorites,
    favoriteIds,
    isFavorite: (movieId: number) => favoriteIds.has(movieId),
    toggleFavorite,
  };
}
