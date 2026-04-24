import { useMemo } from 'react';
import { Link, useSearchParams } from 'react-router-dom';

import { EmptyState } from '../../../shared/components/EmptyState';
import { ErrorState } from '../../../shared/components/ErrorState';
import { PageSection } from '../../../shared/components/PageSection';
import { Pagination } from '../../../shared/components/Pagination';
import { Spinner } from '../../../shared/components/Spinner';
import { useDocumentTitle } from '../../../shared/hooks/useDocumentTitle';
import { useDirectors } from '../hooks';

export default function DirectorsListPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const page = Number.parseInt(searchParams.get('page') ?? '1', 10) || 1;
  const search = searchParams.get('search') ?? '';
  const params = useMemo(
    () => ({ page, search: search || undefined, page_size: 12 }),
    [page, search],
  );
  const query = useDirectors(params);
  useDocumentTitle('Directors');

  return (
    <PageSection
      eyebrow="Filmmakers"
      title="Directors"
      description="Browse the creative voices behind the catalog’s films."
      actions={
        <input
          className="ring-focus rounded-full border border-[color:var(--border)] bg-white px-4 py-3"
          onChange={(event) => {
            const next = new URLSearchParams(searchParams);
            if (event.target.value) {
              next.set('search', event.target.value);
            } else {
              next.delete('search');
            }
            next.set('page', '1');
            setSearchParams(next);
          }}
          placeholder="Search directors..."
          value={search}
        />
      }
    >
      {query.isLoading ? (
        <Spinner className="py-20" label="Loading directors" />
      ) : null}
      {query.isError ? (
        <ErrorState message="Directors could not be loaded right now." />
      ) : null}
      {!query.isLoading && !query.isError && query.data?.items.length === 0 ? (
        <EmptyState
          title="No directors matched"
          message="Try a broader search term."
        />
      ) : null}
      {query.data?.items.length ? (
        <>
          <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
            {query.data.items.map((director) => (
              <Link
                key={director.id}
                className="panel rounded-[1.5rem] p-5 transition hover:-translate-y-1"
                to={`/directors/${director.id}`}
              >
                <p className="text-xs uppercase tracking-[0.25em] text-[color:var(--accent)]">
                  Director
                </p>
                <h3 className="mt-2 text-xl font-semibold">{director.name}</h3>
                <p className="mt-2 text-sm text-[color:var(--muted)]">
                  {director.birth_year
                    ? `Born ${director.birth_year}`
                    : 'Birth year unavailable'}
                </p>
              </Link>
            ))}
          </div>
          <Pagination
            onPageChange={(nextPage) => {
              const next = new URLSearchParams(searchParams);
              next.set('page', String(nextPage));
              setSearchParams(next);
            }}
            page={page}
            totalPages={query.data.meta?.pagination?.total_pages ?? 1}
          />
        </>
      ) : null}
    </PageSection>
  );
}
