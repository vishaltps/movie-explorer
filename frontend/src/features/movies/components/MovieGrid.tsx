import type { MovieRead } from '../../../shared/types';

import { MovieCard } from './MovieCard';

type MovieGridProps = {
  movies: MovieRead[];
};

export function MovieGrid({ movies }: MovieGridProps) {
  return (
    <div className="grid gap-5 sm:grid-cols-2 xl:grid-cols-3">
      {movies.map((movie) => (
        <MovieCard key={movie.id} movie={movie} />
      ))}
    </div>
  );
}
