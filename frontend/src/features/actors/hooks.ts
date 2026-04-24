import { useQuery } from '@tanstack/react-query';

import {
  getActor,
  getActorMovies,
  listActors,
  type ActorListParams,
} from './api';

export function useActors(params: ActorListParams) {
  return useQuery({
    queryKey: ['actors', params],
    queryFn: () => listActors(params),
  });
}

export function useActor(actorId: number) {
  return useQuery({
    queryKey: ['actor', actorId],
    queryFn: () => getActor(actorId),
    enabled: Number.isFinite(actorId),
  });
}

export function useActorMovies(actorId: number) {
  return useQuery({
    queryKey: ['actor-movies', actorId],
    queryFn: () => getActorMovies(actorId),
    enabled: Number.isFinite(actorId),
  });
}
