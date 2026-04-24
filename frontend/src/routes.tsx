import { lazy, Suspense } from 'react';
import { Navigate, Outlet, createBrowserRouter } from 'react-router-dom';

import { AppShell } from './shared/components/AppShell';
import { ErrorState } from './shared/components/ErrorState';
import { Spinner } from './shared/components/Spinner';

const MoviesListPage = lazy(
  () => import('./features/movies/pages/MoviesListPage'),
);
const MovieDetailPage = lazy(
  () => import('./features/movies/pages/MovieDetailPage'),
);
const ActorsListPage = lazy(
  () => import('./features/actors/pages/ActorsListPage'),
);
const ActorDetailPage = lazy(
  () => import('./features/actors/pages/ActorDetailPage'),
);
const DirectorsListPage = lazy(
  () => import('./features/directors/pages/DirectorsListPage'),
);
const DirectorDetailPage = lazy(
  () => import('./features/directors/pages/DirectorDetailPage'),
);
const GenresListPage = lazy(
  () => import('./features/genres/pages/GenresListPage'),
);
const GenreDetailPage = lazy(
  () => import('./features/genres/pages/GenreDetailPage'),
);
const FavoritesPage = lazy(
  () => import('./features/favorites/pages/FavoritesPage'),
);

function RouteFrame() {
  return (
    <AppShell>
      <Suspense fallback={<Spinner label="Loading page" className="py-24" />}>
        <Outlet />
      </Suspense>
    </AppShell>
  );
}

function NotFoundPage() {
  return (
    <div className="py-16">
      <ErrorState
        title="Page not found"
        message="The page you requested does not exist or may have moved."
      />
    </div>
  );
}

export const router = createBrowserRouter([
  {
    path: '/',
    element: <RouteFrame />,
    children: [
      { index: true, element: <Navigate to="/movies" replace /> },
      { path: 'movies', element: <MoviesListPage /> },
      { path: 'movies/:movieId', element: <MovieDetailPage /> },
      { path: 'actors', element: <ActorsListPage /> },
      { path: 'actors/:actorId', element: <ActorDetailPage /> },
      { path: 'directors', element: <DirectorsListPage /> },
      { path: 'directors/:directorId', element: <DirectorDetailPage /> },
      { path: 'genres', element: <GenresListPage /> },
      { path: 'genres/:genreId', element: <GenreDetailPage /> },
      { path: 'favorites', element: <FavoritesPage /> },
      { path: '*', element: <NotFoundPage /> },
    ],
  },
]);
