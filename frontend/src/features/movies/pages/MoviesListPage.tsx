import { useSearchParams } from 'react-router-dom';

import { useActors } from '../../actors/hooks';
import { useDirectors } from '../../directors/hooks';
import { useGenres } from '../../genres/hooks';
import { EmptyState } from '../../../shared/components/EmptyState';
import { ErrorState } from '../../../shared/components/ErrorState';
import { PageSection } from '../../../shared/components/PageSection';
import { Pagination } from '../../../shared/components/Pagination';
import { Spinner } from '../../../shared/components/Spinner';
import { useDebouncedValue } from '../../../shared/hooks/useDebouncedValue';
import { useDocumentTitle } from '../../../shared/hooks/useDocumentTitle';
import {
  readMovieListParams,
  writeSearchParams,
} from '../../../shared/lib/searchParams';
import { ActiveFilters } from '../components/ActiveFilters';
import { MovieFilterBar } from '../components/MovieFilterBar';
import { MovieGrid } from '../components/MovieGrid';
import { useMovies } from '../hooks';

export default function MoviesListPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const rawParams = readMovieListParams(searchParams);
  const debouncedSearch = useDebouncedValue(rawParams.search ?? '', 300);
  const params = {
    ...rawParams,
    search: debouncedSearch || undefined,
  };

  const moviesQuery = useMovies(params);
  const genresQuery = useGenres();
  const directorsQuery = useDirectors({
    page: 1,
    page_size: 100,
    sort: 'name',
  });
  const actorsQuery = useActors({ page: 1, page_size: 100, sort: 'name' });

  useDocumentTitle('Movies');

  const activeFilters = [
    rawParams.search
      ? { key: 'search', label: `Search: ${rawParams.search}` }
      : null,
    rawParams.genre_id
      ? { key: 'genre_id', label: `Genre #${rawParams.genre_id}` }
      : null,
    rawParams.director_id
      ? { key: 'director_id', label: `Director #${rawParams.director_id}` }
      : null,
    rawParams.actor_id
      ? { key: 'actor_id', label: `Actor #${rawParams.actor_id}` }
      : null,
    rawParams.year ? { key: 'year', label: `Year ${rawParams.year}` } : null,
    rawParams.year_min
      ? { key: 'year_min', label: `From ${rawParams.year_min}` }
      : null,
    rawParams.year_max
      ? { key: 'year_max', label: `Until ${rawParams.year_max}` }
      : null,
    rawParams.sort ? { key: 'sort', label: `Sort ${rawParams.sort}` } : null,
  ].filter((value): value is { key: string; label: string } => Boolean(value));

  const setFilterPatch = (
    patch: Record<string, string | number | undefined | null>,
  ) => {
    setSearchParams(writeSearchParams(searchParams, patch));
  };

  return (
    <PageSection
      eyebrow="Catalog"
      title="Movies"
      description="A fast, filterable view across the whole collection, with enough detail to scan and narrow without losing momentum."
    >
      <MovieFilterBar
        actors={actorsQuery.data?.items ?? []}
        directors={directorsQuery.data?.items ?? []}
        genres={genresQuery.data?.items ?? []}
        onChange={(patch) => setFilterPatch(patch)}
        value={rawParams}
      />
      <ActiveFilters
        filters={activeFilters}
        onClear={(key) => setFilterPatch({ [key]: undefined, page: 1 })}
        onClearAll={() => setSearchParams(new URLSearchParams())}
      />
      {moviesQuery.isLoading ? (
        <Spinner className="py-20" label="Loading movies" />
      ) : null}
      {moviesQuery.isError ? (
        <ErrorState message="Movies could not be loaded right now. Please try again." />
      ) : null}
      {!moviesQuery.isLoading &&
      !moviesQuery.isError &&
      moviesQuery.data?.items.length === 0 ? (
        <div className="mt-6">
          <EmptyState
            title="No movies matched"
            message="Try relaxing one or two filters to widen the catalog."
          />
        </div>
      ) : null}
      {moviesQuery.data?.items.length ? (
        <>
          <div className="mt-6">
            <MovieGrid movies={moviesQuery.data.items} />
          </div>
          <Pagination
            onPageChange={(nextPage) => setFilterPatch({ page: nextPage })}
            page={params.page ?? 1}
            totalPages={moviesQuery.data.meta?.pagination?.total_pages ?? 1}
          />
        </>
      ) : null}
    </PageSection>
  );
}
