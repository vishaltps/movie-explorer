import { beforeAll, afterAll, afterEach, describe, expect, it } from 'vitest';
import { screen, waitFor } from '@testing-library/react';

import MoviesListPage from './MoviesListPage';
import { handlers } from '../../../shared/lib/test/handlers';
import { renderWithProviders } from '../../../shared/lib/test/render';
import { server } from '../../../shared/lib/test/server';

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

server.use(...handlers);

describe('MoviesListPage', () => {
  it('renders movies from the API', async () => {
    renderWithProviders(<MoviesListPage />, { route: '/movies' });

    await waitFor(() => {
      expect(screen.getByText('Arrival')).toBeInTheDocument();
    });

    expect(
      screen.getByText(/Directed by Denis Villeneuve/i),
    ).toBeInTheDocument();
  });
});
