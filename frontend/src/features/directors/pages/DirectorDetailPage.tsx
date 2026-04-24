import { Link, useParams } from 'react-router-dom';

import { EmptyState } from '../../../shared/components/EmptyState';
import { ErrorState } from '../../../shared/components/ErrorState';
import { MovieGrid } from '../../movies/components/MovieGrid';
import { PageSection } from '../../../shared/components/PageSection';
import { Spinner } from '../../../shared/components/Spinner';
import { useDocumentTitle } from '../../../shared/hooks/useDocumentTitle';
import { useDirector, useDirectorMovies } from '../hooks';

export default function DirectorDetailPage() {
  const { directorId } = useParams();
  const id = Number(directorId);
  const directorQuery = useDirector(id);
  const moviesQuery = useDirectorMovies(id);

  useDocumentTitle(directorQuery.data?.item.name ?? 'Director');

  if (directorQuery.isLoading) {
    return <Spinner className="py-24" label="Loading director" />;
  }

  if (directorQuery.isError || !directorQuery.data) {
    return <ErrorState message="The director details could not be loaded." />;
  }

  return (
    <>
      <PageSection
        eyebrow="Director"
        title={directorQuery.data.item.name}
        description={
          directorQuery.data.item.bio ??
          `${directorQuery.data.item.name} does not yet have a biography in this catalog.`
        }
        actions={
          <Link
            className="rounded-full border border-[color:var(--border)] bg-white px-4 py-2 text-sm"
            to="/directors"
          >
            Back to directors
          </Link>
        }
      >
        <p className="text-sm text-[color:var(--muted)]">
          {directorQuery.data.item.birth_year
            ? `Born ${directorQuery.data.item.birth_year}`
            : 'Birth year unavailable'}
        </p>
      </PageSection>
      <PageSection
        title="Directed movies"
        description="Films linked to this director."
      >
        {moviesQuery.isLoading ? (
          <Spinner className="py-16" label="Loading movies" />
        ) : null}
        {moviesQuery.isError ? (
          <ErrorState message="Directed movies could not be loaded." />
        ) : null}
        {!moviesQuery.isLoading &&
        !moviesQuery.isError &&
        moviesQuery.data?.items.length === 0 ? (
          <EmptyState
            title="No movies listed"
            message="This director has no linked movies in the seed data."
          />
        ) : null}
        {moviesQuery.data?.items.length ? (
          <MovieGrid movies={moviesQuery.data.items} />
        ) : null}
      </PageSection>
    </>
  );
}
