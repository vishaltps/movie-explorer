import { useQuery } from '@tanstack/react-query';

import { getGenre, getGenreMovies, listGenres } from './api';

export function useGenres() {
  return useQuery({
    queryKey: ['genres'],
    queryFn: () => listGenres(),
  });
}

export function useGenre(genreId: number) {
  return useQuery({
    queryKey: ['genre', genreId],
    queryFn: () => getGenre(genreId),
    enabled: Number.isFinite(genreId),
  });
}

export function useGenreMovies(genreId: number, page = 1) {
  return useQuery({
    queryKey: ['genre-movies', genreId, page],
    queryFn: () => getGenreMovies(genreId, page),
    enabled: Number.isFinite(genreId),
  });
}
