export type { components, operations, paths } from './api-generated';

import type { components } from './api-generated';

export type PaginationMeta = components['schemas']['PaginationMeta'];
export type Meta = components['schemas']['Meta'];
export type ErrorPayload = components['schemas']['ErrorPayload'];
export type GenreRead = components['schemas']['GenreRead'];
export type DirectorRead = components['schemas']['DirectorRead'];
export type DirectorDetail = components['schemas']['DirectorDetail'];
export type ActorRead = components['schemas']['ActorRead'];
export type ActorDetail = components['schemas']['ActorDetail'];
export type ReviewRead = components['schemas']['ReviewRead'];
export type MovieRead = components['schemas']['MovieRead'];
export type MovieDetail = components['schemas']['MovieDetail'];

export type Envelope<T> = {
  success?: boolean;
  data?: T | null;
  error?: ErrorPayload | null;
  meta?: Meta | null;
};
