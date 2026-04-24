import { Link } from 'react-router-dom';

import { EmptyState } from '../../../shared/components/EmptyState';
import { MoviePoster } from '../../../shared/components/MoviePoster';
import { PageSection } from '../../../shared/components/PageSection';
import { RatingStars } from '../../../shared/components/RatingStars';
import { useDocumentTitle } from '../../../shared/hooks/useDocumentTitle';
import { useFavorites } from '../hooks';

export default function FavoritesPage() {
  const { favorites } = useFavorites();
  useDocumentTitle('Favorites');

  return (
    <PageSection
      eyebrow="Local picks"
      title="Favorites"
      description="Your saved movies stay in local storage, ready for quick revisits."
    >
      {favorites.length === 0 ? (
        <EmptyState
          title="No favorites yet"
          message="Save movies from the catalog and they’ll show up here."
          action={
            <Link
              className="rounded-full bg-amber-700 px-5 py-3 text-sm font-semibold text-white"
              to="/movies"
            >
              Browse movies
            </Link>
          }
        />
      ) : (
        <div className="grid gap-5 sm:grid-cols-2 xl:grid-cols-3">
          {favorites.map((movie) => (
            <Link
              key={movie.id}
              className="panel rounded-[1.75rem] p-4 transition hover:-translate-y-1"
              to={`/movies/${movie.id}`}
            >
              <MoviePoster
                alt={`${movie.title} poster`}
                className="w-full"
                src={movie.poster_url}
              />
              <div className="mt-4">
                <p className="text-sm uppercase tracking-[0.2em] text-[color:var(--accent)]">
                  {movie.release_year}
                </p>
                <h3 className="mt-1 text-xl font-semibold">{movie.title}</h3>
                <div className="mt-3">
                  <RatingStars rating={movie.average_rating} />
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </PageSection>
  );
}
