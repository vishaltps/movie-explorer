import { Link } from 'react-router-dom';

import { FavoriteToggleButton } from '../../favorites/components/FavoriteToggleButton';
import { MoviePoster } from '../../../shared/components/MoviePoster';
import { Pill } from '../../../shared/components/Pill';
import { RatingStars } from '../../../shared/components/RatingStars';
import type { MovieRead } from '../../../shared/types';

type MovieCardProps = {
  movie: MovieRead;
};

export function MovieCard({ movie }: MovieCardProps) {
  return (
    <article className="panel group flex h-full flex-col rounded-[1.75rem] p-4 transition hover:-translate-y-1">
      <div className="relative">
        <Link
          aria-label={`Open ${movie.title}`}
          className="ring-focus block rounded-[1.5rem]"
          to={`/movies/${movie.id}`}
        >
          <MoviePoster
            alt={`${movie.title} poster`}
            className="w-full"
            src={movie.poster_url ?? null}
          />
        </Link>
        <div className="absolute right-3 top-3">
          <FavoriteToggleButton movie={movie} />
        </div>
      </div>
      <div className="mt-4 flex flex-1 flex-col">
        <Link className="ring-focus block rounded-xl" to={`/movies/${movie.id}`}>
          <div className="flex items-start justify-between gap-3">
            <div>
              <p className="text-sm uppercase tracking-[0.2em] text-[color:var(--accent)]">
                {movie.release_year}
              </p>
              <h3 className="mt-1 text-xl font-semibold group-hover:text-amber-700">
                {movie.title}
              </h3>
            </div>
          </div>
          <p className="mt-3 text-sm text-[color:var(--muted)]">
            {movie.director
              ? `Directed by ${movie.director.name}`
              : 'Director unavailable'}
          </p>
          <div className="mt-3">
            <RatingStars rating={movie.average_rating ?? null} />
          </div>
        </Link>
        <div className="mt-4 flex flex-wrap gap-2">
          {movie.genres.map((genre) => (
            <Link key={genre.id} to={`/genres/${genre.id}`}>
              <Pill>{genre.name}</Pill>
            </Link>
          ))}
        </div>
      </div>
    </article>
  );
}
