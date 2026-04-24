import type { ChangeEvent } from 'react';

import type { ActorRead, DirectorRead, GenreRead } from '../../../shared/types';

import type { MovieListParams } from '../types';

type MovieFilterBarProps = {
  value: MovieListParams;
  genres: GenreRead[];
  directors: DirectorRead[];
  actors: ActorRead[];
  onChange: (patch: Partial<MovieListParams>) => void;
};

function parseNumber(value: string) {
  if (!value) {
    return undefined;
  }

  const parsed = Number.parseInt(value, 10);
  return Number.isNaN(parsed) ? undefined : parsed;
}

export function MovieFilterBar({
  value,
  genres,
  directors,
  actors,
  onChange,
}: MovieFilterBarProps) {
  const handleSelectChange =
    (key: keyof MovieListParams) => (event: ChangeEvent<HTMLSelectElement>) => {
      onChange({ [key]: parseNumber(event.target.value), page: 1 });
    };

  const handleInputChange =
    (key: keyof MovieListParams) => (event: ChangeEvent<HTMLInputElement>) => {
      onChange({ [key]: event.target.value, page: 1 });
    };

  return (
    <div className="panel rounded-[1.75rem] p-5">
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <label className="text-sm">
          <span className="mb-2 block font-medium">Search title</span>
          <input
            className="ring-focus w-full rounded-2xl border border-[color:var(--border)] bg-white px-4 py-3"
            onChange={handleInputChange('search')}
            placeholder="Search movies..."
            value={value.search ?? ''}
          />
        </label>
        <label className="text-sm">
          <span className="mb-2 block font-medium">Genre</span>
          <select
            className="ring-focus w-full rounded-2xl border border-[color:var(--border)] bg-white px-4 py-3"
            onChange={handleSelectChange('genre_id')}
            value={value.genre_id ?? ''}
          >
            <option value="">All genres</option>
            {genres.map((genre) => (
              <option key={genre.id} value={genre.id}>
                {genre.name}
              </option>
            ))}
          </select>
        </label>
        <label className="text-sm">
          <span className="mb-2 block font-medium">Director</span>
          <select
            className="ring-focus w-full rounded-2xl border border-[color:var(--border)] bg-white px-4 py-3"
            onChange={handleSelectChange('director_id')}
            value={value.director_id ?? ''}
          >
            <option value="">All directors</option>
            {directors.map((director) => (
              <option key={director.id} value={director.id}>
                {director.name}
              </option>
            ))}
          </select>
        </label>
        <label className="text-sm">
          <span className="mb-2 block font-medium">Actor</span>
          <select
            className="ring-focus w-full rounded-2xl border border-[color:var(--border)] bg-white px-4 py-3"
            onChange={handleSelectChange('actor_id')}
            value={value.actor_id ?? ''}
          >
            <option value="">All actors</option>
            {actors.map((actor) => (
              <option key={actor.id} value={actor.id}>
                {actor.name}
              </option>
            ))}
          </select>
        </label>
        <label className="text-sm">
          <span className="mb-2 block font-medium">Exact year</span>
          <input
            className="ring-focus w-full rounded-2xl border border-[color:var(--border)] bg-white px-4 py-3"
            inputMode="numeric"
            onChange={(event) =>
              onChange({ year: parseNumber(event.target.value), page: 1 })
            }
            placeholder="e.g. 2019"
            value={value.year ?? ''}
          />
        </label>
        <label className="text-sm">
          <span className="mb-2 block font-medium">Year from</span>
          <input
            className="ring-focus w-full rounded-2xl border border-[color:var(--border)] bg-white px-4 py-3"
            inputMode="numeric"
            onChange={(event) =>
              onChange({ year_min: parseNumber(event.target.value), page: 1 })
            }
            placeholder="1980"
            value={value.year_min ?? ''}
          />
        </label>
        <label className="text-sm">
          <span className="mb-2 block font-medium">Year to</span>
          <input
            className="ring-focus w-full rounded-2xl border border-[color:var(--border)] bg-white px-4 py-3"
            inputMode="numeric"
            onChange={(event) =>
              onChange({ year_max: parseNumber(event.target.value), page: 1 })
            }
            placeholder="2024"
            value={value.year_max ?? ''}
          />
        </label>
        <label className="text-sm">
          <span className="mb-2 block font-medium">Sort</span>
          <select
            className="ring-focus w-full rounded-2xl border border-[color:var(--border)] bg-white px-4 py-3"
            onChange={(event) =>
              onChange({ sort: event.target.value || undefined, page: 1 })
            }
            value={value.sort ?? ''}
          >
            <option value="">Featured</option>
            <option value="title">Title A-Z</option>
            <option value="-title">Title Z-A</option>
            <option value="-release_year">Newest first</option>
            <option value="release_year">Oldest first</option>
            <option value="-average_rating">Top rated</option>
            <option value="average_rating">Lowest rated</option>
          </select>
        </label>
      </div>
    </div>
  );
}
