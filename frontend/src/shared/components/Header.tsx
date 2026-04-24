import { Link, NavLink } from 'react-router-dom';

const navigation = [
  { to: '/movies', label: 'Movies' },
  { to: '/actors', label: 'Actors' },
  { to: '/directors', label: 'Directors' },
  { to: '/genres', label: 'Genres' },
  { to: '/favorites', label: 'Favorites' },
];

export function Header() {
  return (
    <header className="panel mb-8 rounded-[2rem] px-5 py-5 sm:px-7">
      <div className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <p className="text-sm uppercase tracking-[0.35em] text-[color:var(--accent)]">
            L7 Informatics
          </p>
          <h1 className="mt-2 text-4xl font-semibold tracking-tight text-[color:var(--text)]">
            <Link className="ring-focus rounded-md hover:text-amber-800" to="/">
              Movie Explorer
            </Link>
          </h1>
          <p className="mt-2 max-w-2xl text-sm text-[color:var(--muted)] sm:text-base">
            Browse a curated cinema catalog, trace casts and directors, and keep
            your shortlist close at hand.
          </p>
        </div>
        <nav aria-label="Primary" className="flex flex-wrap gap-2">
          {navigation.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                [
                  'ring-focus rounded-full border px-4 py-2 text-sm transition',
                  isActive
                    ? 'border-amber-700 bg-amber-700 text-amber-50'
                    : 'border-[color:var(--border)] bg-white/50 text-[color:var(--text)] hover:-translate-y-0.5 hover:border-amber-700/40 hover:bg-white',
                ].join(' ')
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
      </div>
    </header>
  );
}
