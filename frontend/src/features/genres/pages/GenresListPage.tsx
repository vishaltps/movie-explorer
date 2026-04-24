import { Link } from 'react-router-dom';

import { ErrorState } from '../../../shared/components/ErrorState';
import { PageSection } from '../../../shared/components/PageSection';
import { Spinner } from '../../../shared/components/Spinner';
import { useDocumentTitle } from '../../../shared/hooks/useDocumentTitle';
import { useGenres } from '../hooks';

export default function GenresListPage() {
  const query = useGenres();
  useDocumentTitle('Genres');

  return (
    <PageSection
      eyebrow="Browse by tone"
      title="Genres"
      description="Use genres as a fast jump point into different slices of the catalog."
    >
      {query.isLoading ? (
        <Spinner className="py-20" label="Loading genres" />
      ) : null}
      {query.isError ? (
        <ErrorState message="Genres could not be loaded right now." />
      ) : null}
      {query.data?.items.length ? (
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          {query.data.items.map((genre) => (
            <Link
              key={genre.id}
              className="panel rounded-[1.5rem] p-5 transition hover:-translate-y-1"
              to={`/genres/${genre.id}`}
            >
              <p className="text-xs uppercase tracking-[0.25em] text-[color:var(--accent)]">
                Genre
              </p>
              <h3 className="mt-2 text-xl font-semibold">{genre.name}</h3>
              <p className="mt-2 text-sm text-[color:var(--muted)]">
                Slug: {genre.slug}
              </p>
            </Link>
          ))}
        </div>
      ) : null}
    </PageSection>
  );
}
