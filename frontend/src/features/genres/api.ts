import { apiGet } from '../../shared/lib/apiClient';
import type { GenreRead, MovieRead } from '../../shared/types';

export async function listGenres() {
  const response = await apiGet<GenreRead[]>('/genres');
  return { items: response.data, meta: response.meta };
}

export async function getGenre(genreId: number) {
  const response = await apiGet<GenreRead>(`/genres/${genreId}`);
  return { item: response.data, meta: response.meta };
}

export async function getGenreMovies(genreId: number, page = 1, pageSize = 20) {
  const response = await apiGet<MovieRead[]>(`/genres/${genreId}/movies`, {
    page,
    page_size: pageSize,
  });
  return { items: response.data, meta: response.meta };
}
