import { useMemo } from 'react';
import { useSearchParams } from 'react-router-dom';

import { EmptyState } from '../../../shared/components/EmptyState';
import { ErrorState } from '../../../shared/components/ErrorState';
import { PageSection } from '../../../shared/components/PageSection';
import { Pagination } from '../../../shared/components/Pagination';
import { Spinner } from '../../../shared/components/Spinner';
import { useDocumentTitle } from '../../../shared/hooks/useDocumentTitle';
import { ActorList } from '../components/ActorList';
import { useActors } from '../hooks';

export default function ActorsListPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const page = Number.parseInt(searchParams.get('page') ?? '1', 10) || 1;
  const search = searchParams.get('search') ?? '';
  const params = useMemo(
    () => ({ page, search: search || undefined, page_size: 12 }),
    [page, search],
  );
  const query = useActors(params);
  useDocumentTitle('Actors');

  return (
    <PageSection
      eyebrow="Cast"
      title="Actors"
      description="Explore performers across the catalog and jump into the films that connect them."
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
          placeholder="Search actors..."
          value={search}
        />
      }
    >
      {query.isLoading ? (
        <Spinner className="py-20" label="Loading actors" />
      ) : null}
      {query.isError ? (
        <ErrorState message="Actors could not be loaded right now." />
      ) : null}
      {!query.isLoading && !query.isError && query.data?.items.length === 0 ? (
        <EmptyState
          title="No actors matched"
          message="Try a different search term to broaden the cast list."
        />
      ) : null}
      {query.data?.items.length ? (
        <>
          <ActorList actors={query.data.items} />
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
