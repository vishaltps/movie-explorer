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
    <article className="panel group flex flex-row gap-4 rounded-2xl p-3 transition hover:-translate-y-0.5">
      <Link
        aria-label={`Open ${movie.title}`}
        className="ring-focus shrink-0 rounded-xl"
        to={`/movies/${movie.id}`}
      >
        <MoviePoster
          alt={`${movie.title} poster`}
          className="w-20"
          src={movie.poster_url ?? null}
        />
      </Link>
      <div className="flex min-w-0 flex-1 flex-col justify-between py-1">
        <Link className="ring-focus block rounded-xl" to={`/movies/${movie.id}`}>
          <p className="text-xs uppercase tracking-[0.2em] text-[color:var(--accent)]">
            {movie.release_year}
          </p>
          <h3 className="mt-0.5 truncate text-base font-semibold group-hover:text-amber-700">
            {movie.title}
          </h3>
          <p className="mt-1 truncate text-xs text-[color:var(--muted)]">
            {movie.director
              ? `Directed by ${movie.director.name}`
              : 'Director unavailable'}
          </p>
          <div className="mt-2">
            <RatingStars rating={movie.average_rating ?? null} />
          </div>
        </Link>
        <div className="mt-2 flex flex-wrap gap-1.5">
          {movie.genres.slice(0, 3).map((genre) => (
            <Link key={genre.id} to={`/genres/${genre.id}`}>
              <Pill>{genre.name}</Pill>
            </Link>
          ))}
        </div>
      </div>
      <div className="shrink-0 self-start pt-1">
        <FavoriteToggleButton movie={movie} />
      </div>
    </article>
  );
}
