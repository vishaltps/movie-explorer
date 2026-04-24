import type { Meta, MovieDetail, MovieRead } from '../../shared/types';

export type MovieListParams = {
  genre_id?: number;
  director_id?: number;
  actor_id?: number;
  year?: number;
  year_min?: number;
  year_max?: number;
  search?: string;
  sort?: string;
  page?: number;
  page_size?: number;
};

export type MovieListResponse = {
  items: MovieRead[];
  meta: Meta | null;
};

export type MovieDetailResponse = {
  item: MovieDetail;
  meta: Meta | null;
};
