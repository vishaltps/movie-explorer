import { apiGet } from '../../shared/lib/apiClient';
import type { ActorDetail, ActorRead, MovieRead } from '../../shared/types';

export type ActorListParams = {
  movie_id?: number;
  genre_id?: number;
  search?: string;
  sort?: string;
  page?: number;
  page_size?: number;
};

export async function listActors(params: ActorListParams) {
  const response = await apiGet<ActorRead[]>('/actors', params);
  return { items: response.data, meta: response.meta };
}

export async function getActor(actorId: number) {
  const response = await apiGet<ActorDetail>(`/actors/${actorId}`);
  return { item: response.data, meta: response.meta };
}

export async function getActorMovies(actorId: number, page = 1, pageSize = 20) {
  const response = await apiGet<MovieRead[]>(`/actors/${actorId}/movies`, {
    page,
    page_size: pageSize,
  });
  return { items: response.data, meta: response.meta };
}
