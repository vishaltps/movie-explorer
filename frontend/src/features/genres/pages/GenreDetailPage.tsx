import { Link, useSearchParams, useParams } from 'react-router-dom';

import { EmptyState } from '../../../shared/components/EmptyState';
import { ErrorState } from '../../../shared/components/ErrorState';
import { MovieGrid } from '../../movies/components/MovieGrid';
import { PageSection } from '../../../shared/components/PageSection';
import { Pagination } from '../../../shared/components/Pagination';
import { Spinner } from '../../../shared/components/Spinner';
import { useDocumentTitle } from '../../../shared/hooks/useDocumentTitle';
import { useGenre, useGenreMovies } from '../hooks';

export default function GenreDetailPage() {
  const { genreId } = useParams();
  const [searchParams, setSearchParams] = useSearchParams();
  const id = Number(genreId);
  const page = Number.parseInt(searchParams.get('page') ?? '1', 10) || 1;
  const genreQuery = useGenre(id);
  const moviesQuery = useGenreMovies(id, page);

  useDocumentTitle(genreQuery.data?.item.name ?? 'Genre');

  if (genreQuery.isLoading) {
    return <Spinner className="py-24" label="Loading genre" />;
  }

  if (genreQuery.isError || !genreQuery.data) {
    return <ErrorState message="The genre details could not be loaded." />;
  }

  return (
    <>
      <PageSection
        eyebrow="Genre"
        title={genreQuery.data.item.name}
        description={`Slug: ${genreQuery.data.item.slug}`}
        actions={
          <Link
            className="rounded-full border border-[color:var(--border)] bg-white px-4 py-2 text-sm"
            to="/genres"
          >
            Back to genres
          </Link>
        }
      />
      <PageSection
        title="Movies in this genre"
        description="A paginated slice of matching movies."
      >
        {moviesQuery.isLoading ? (
          <Spinner className="py-16" label="Loading movies" />
        ) : null}
        {moviesQuery.isError ? (
          <ErrorState message="Genre movies could not be loaded." />
        ) : null}
        {!moviesQuery.isLoading &&
        !moviesQuery.isError &&
        moviesQuery.data?.items.length === 0 ? (
          <EmptyState
            title="No movies found"
            message="This genre currently has no linked movies."
          />
        ) : null}
        {moviesQuery.data?.items.length ? (
          <>
            <MovieGrid movies={moviesQuery.data.items} />
            <Pagination
              onPageChange={(nextPage) => {
                const next = new URLSearchParams(searchParams);
                next.set('page', String(nextPage));
                setSearchParams(next);
              }}
              page={page}
              totalPages={moviesQuery.data.meta?.pagination?.total_pages ?? 1}
            />
          </>
        ) : null}
      </PageSection>
    </>
  );
}
