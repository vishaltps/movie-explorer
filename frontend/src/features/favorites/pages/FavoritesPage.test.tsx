import { describe, expect, it, beforeEach } from 'vitest';
import { screen } from '@testing-library/react';

import FavoritesPage from './FavoritesPage';
import { favoritesStorageKey } from '../../../shared/lib/localStorage';
import { renderWithProviders } from '../../../shared/lib/test/render';

describe('FavoritesPage', () => {
  beforeEach(() => {
    window.localStorage.clear();
  });

  it('shows empty state when no favorites exist', () => {
    renderWithProviders(<FavoritesPage />, { route: '/favorites' });
    expect(screen.getByText(/No favorites yet/i)).toBeInTheDocument();
  });

  it('renders stored favorites', () => {
    window.localStorage.setItem(
      favoritesStorageKey,
      JSON.stringify([
        {
          id: 5,
          title: 'Past Lives',
          release_year: 2023,
          poster_url: null,
          average_rating: 4.2,
        },
      ]),
    );

    renderWithProviders(<FavoritesPage />, { route: '/favorites' });
    expect(screen.getByText('Past Lives')).toBeInTheDocument();
  });
});
