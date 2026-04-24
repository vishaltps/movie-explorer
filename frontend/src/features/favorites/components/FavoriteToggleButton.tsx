import { useFavorites } from '../hooks';
import type { MovieRead } from '../../../shared/types';

type FavoriteToggleButtonProps = {
  movie: Pick<
    MovieRead,
    'id' | 'title' | 'release_year' | 'poster_url' | 'average_rating'
  >;
};

export function FavoriteToggleButton({ movie }: FavoriteToggleButtonProps) {
  const { isFavorite, toggleFavorite } = useFavorites();
  const active = isFavorite(movie.id);

  return (
    <button
      aria-label={
        active
          ? `Remove ${movie.title} from favorites`
          : `Save ${movie.title} to favorites`
      }
      className={[
        'ring-focus rounded-full border px-3 py-2 text-xs font-semibold shadow-sm transition',
        active
          ? 'border-amber-700 bg-amber-700 text-white'
          : 'border-white/70 bg-white/85 text-slate-900 hover:bg-white',
      ].join(' ')}
      onClick={() => toggleFavorite(movie)}
      type="button"
    >
      {active ? 'Saved' : 'Save'}
    </button>
  );
}
