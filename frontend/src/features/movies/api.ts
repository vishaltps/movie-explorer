import { apiGet } from '../../shared/lib/apiClient';
import type { MovieDetail, MovieRead, ReviewRead } from '../../shared/types';

import type {
  MovieListParams,
  MovieDetailResponse,
  MovieListResponse,
} from './types';

export async function listMovies(
  params: MovieListParams,
): Promise<MovieListResponse> {
  const response = await apiGet<MovieRead[]>('/movies', params);
  return { items: response.data, meta: response.meta ?? null };
}

export async function getMovie(movieId: number): Promise<MovieDetailResponse> {
  const response = await apiGet<MovieDetail>(`/movies/${movieId}`);
  return { item: response.data, meta: response.meta ?? null };
}

export async function listMovieReviews(
  movieId: number,
  page = 1,
  pageSize = 20,
) {
  const response = await apiGet<ReviewRead[]>(`/movies/${movieId}/reviews`, {
    page,
    page_size: pageSize,
  });
  return { items: response.data, meta: response.meta };
}
