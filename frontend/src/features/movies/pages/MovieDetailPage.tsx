import { Link, useParams } from 'react-router-dom';

import { FavoriteToggleButton } from '../../favorites/components/FavoriteToggleButton';
import { ErrorState } from '../../../shared/components/ErrorState';
import { MoviePoster } from '../../../shared/components/MoviePoster';
import { PageSection } from '../../../shared/components/PageSection';
import { Pill } from '../../../shared/components/Pill';
import { RatingStars } from '../../../shared/components/RatingStars';
import { Spinner } from '../../../shared/components/Spinner';
import { useDocumentTitle } from '../../../shared/hooks/useDocumentTitle';
import { formatRuntime } from '../../../shared/lib/formatters';
import { ReviewList } from '../components/ReviewList';
import { useMovie } from '../hooks';

export default function MovieDetailPage() {
  const { movieId } = useParams();
  const id = Number(movieId);
  const query = useMovie(id);

  useDocumentTitle(query.data?.item.title ?? 'Movie');

  if (query.isLoading) {
    return <Spinner className="py-24" label="Loading movie" />;
  }

  if (query.isError || !query.data) {
    return <ErrorState message="The movie details could not be loaded." />;
  }

  const movie = query.data.item;

  return (
    <>
      <PageSection
        eyebrow="Movie detail"
        title={movie.title}
        description={movie.synopsis ?? 'Synopsis unavailable for this title.'}
        actions={<FavoriteToggleButton movie={movie} />}
      >
        <div className="grid gap-6 lg:grid-cols-[280px_1fr]">
          <MoviePoster
            alt={`${movie.title} poster`}
            className="w-full"
            src={movie.poster_url ?? null}
          />
          <div className="panel rounded-[1.75rem] p-6">
            <div className="flex flex-wrap gap-2">
              <Pill tone="accent">{movie.release_year}</Pill>
              <Pill>{formatRuntime(movie.runtime_minutes)}</Pill>
            </div>
            <div className="mt-4">
              <RatingStars rating={movie.average_rating ?? null} />
            </div>
            <dl className="mt-6 space-y-4">
              <div>
                <dt className="text-sm font-semibold text-[color:var(--muted)]">
                  Director
                </dt>
                <dd className="mt-1">
                  {movie.director ? (
                    <Link
                      className="font-medium text-amber-800 hover:underline"
                      to={`/directors/${movie.director.id}`}
                    >
                      {movie.director.name}
                    </Link>
                  ) : (
                    'Director unavailable'
                  )}
                </dd>
              </div>
              <div>
                <dt className="text-sm font-semibold text-[color:var(--muted)]">
                  Genres
                </dt>
                <dd className="mt-2 flex flex-wrap gap-2">
                  {movie.genres.map((genre) => (
                    <Link key={genre.id} to={`/genres/${genre.id}`}>
                      <Pill>{genre.name}</Pill>
                    </Link>
                  ))}
                </dd>
              </div>
              <div>
                <dt className="text-sm font-semibold text-[color:var(--muted)]">
                  Actors
                </dt>
                <dd className="mt-2 flex flex-wrap gap-2">
                  {movie.actors.map((actor) => (
                    <Link key={actor.id} to={`/actors/${actor.id}`}>
                      <Pill>{actor.name}</Pill>
                    </Link>
                  ))}
                </dd>
              </div>
            </dl>
          </div>
        </div>
      </PageSection>
      <PageSection
        title="Reviews"
        description="Seeded audience notes included with this title."
      >
        <ReviewList reviews={movie.reviews} />
      </PageSection>
    </>
  );
}
