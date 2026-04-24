import { Link, useParams } from 'react-router-dom';

import { EmptyState } from '../../../shared/components/EmptyState';
import { ErrorState } from '../../../shared/components/ErrorState';
import { MovieGrid } from '../../movies/components/MovieGrid';
import { PageSection } from '../../../shared/components/PageSection';
import { Spinner } from '../../../shared/components/Spinner';
import { useDocumentTitle } from '../../../shared/hooks/useDocumentTitle';
import { useActor, useActorMovies } from '../hooks';

export default function ActorDetailPage() {
  const { actorId } = useParams();
  const id = Number(actorId);
  const actorQuery = useActor(id);
  const moviesQuery = useActorMovies(id);

  useDocumentTitle(actorQuery.data?.item.name ?? 'Actor');

  if (actorQuery.isLoading) {
    return <Spinner className="py-24" label="Loading actor" />;
  }

  if (actorQuery.isError || !actorQuery.data) {
    return <ErrorState message="The actor details could not be loaded." />;
  }

  return (
    <>
      <PageSection
        eyebrow="Performer"
        title={actorQuery.data.item.name}
        description={
          actorQuery.data.item.bio ??
          `${actorQuery.data.item.name} does not yet have a biography in this catalog.`
        }
        actions={
          <Link
            className="rounded-full border border-[color:var(--border)] bg-white px-4 py-2 text-sm"
            to="/actors"
          >
            Back to actors
          </Link>
        }
      >
        <p className="text-sm text-[color:var(--muted)]">
          {actorQuery.data.item.birth_year
            ? `Born ${actorQuery.data.item.birth_year}`
            : 'Birth year unavailable'}
        </p>
      </PageSection>
      <PageSection
        title="Filmography"
        description="Movies featuring this actor."
      >
        {moviesQuery.isLoading ? (
          <Spinner className="py-16" label="Loading filmography" />
        ) : null}
        {moviesQuery.isError ? (
          <ErrorState message="Filmography could not be loaded." />
        ) : null}
        {!moviesQuery.isLoading &&
        !moviesQuery.isError &&
        moviesQuery.data?.items.length === 0 ? (
          <EmptyState
            title="No movies listed"
            message="This actor has no linked movies in the seed data."
          />
        ) : null}
        {moviesQuery.data?.items.length ? (
          <MovieGrid movies={moviesQuery.data.items} />
        ) : null}
      </PageSection>
    </>
  );
}
