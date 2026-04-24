import { Link } from 'react-router-dom';

import type { ActorRead } from '../../../shared/types';

type ActorListProps = {
  actors: ActorRead[];
};

export function ActorList({ actors }: ActorListProps) {
  return (
    <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
      {actors.map((actor) => (
        <Link
          key={actor.id}
          className="panel rounded-[1.5rem] p-5 transition hover:-translate-y-1"
          to={`/actors/${actor.id}`}
        >
          <p className="text-xs uppercase tracking-[0.25em] text-[color:var(--accent)]">
            Actor
          </p>
          <h3 className="mt-2 text-xl font-semibold">{actor.name}</h3>
          <p className="mt-2 text-sm text-[color:var(--muted)]">
            {actor.birth_year
              ? `Born ${actor.birth_year}`
              : 'Birth year unavailable'}
          </p>
        </Link>
      ))}
    </div>
  );
}
