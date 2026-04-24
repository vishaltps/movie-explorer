import { useQuery } from '@tanstack/react-query';

import { getMovie, listMovies } from './api';
import type { MovieListParams } from './types';

export function useMovies(params: MovieListParams) {
  return useQuery({
    queryKey: ['movies', params],
    queryFn: () => listMovies(params),
  });
}

export function useMovie(movieId: number) {
  return useQuery({
    queryKey: ['movie', movieId],
    queryFn: () => getMovie(movieId),
    enabled: Number.isFinite(movieId),
  });
}
