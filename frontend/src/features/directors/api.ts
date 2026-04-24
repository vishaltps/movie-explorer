import { apiGet } from '../../shared/lib/apiClient';
import type {
  DirectorDetail,
  DirectorRead,
  MovieRead,
} from '../../shared/types';

export type DirectorListParams = {
  search?: string;
  sort?: string;
  page?: number;
  page_size?: number;
};

export async function listDirectors(params: DirectorListParams) {
  const response = await apiGet<DirectorRead[]>('/directors', params);
  return { items: response.data, meta: response.meta };
}

export async function getDirector(directorId: number) {
  const response = await apiGet<DirectorDetail>(`/directors/${directorId}`);
  return { item: response.data, meta: response.meta };
}

export async function getDirectorMovies(
  directorId: number,
  page = 1,
  pageSize = 20,
) {
  const response = await apiGet<MovieRead[]>(
    `/directors/${directorId}/movies`,
    {
      page,
      page_size: pageSize,
    },
  );
  return { items: response.data, meta: response.meta };
}
