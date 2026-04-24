import { useQuery } from '@tanstack/react-query';

import {
  getDirector,
  getDirectorMovies,
  listDirectors,
  type DirectorListParams,
} from './api';

export function useDirectors(params: DirectorListParams) {
  return useQuery({
    queryKey: ['directors', params],
    queryFn: () => listDirectors(params),
  });
}

export function useDirector(directorId: number) {
  return useQuery({
    queryKey: ['director', directorId],
    queryFn: () => getDirector(directorId),
    enabled: Number.isFinite(directorId),
  });
}

export function useDirectorMovies(directorId: number) {
  return useQuery({
    queryKey: ['director-movies', directorId],
    queryFn: () => getDirectorMovies(directorId),
    enabled: Number.isFinite(directorId),
  });
}
