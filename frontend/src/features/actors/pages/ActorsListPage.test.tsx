import { afterAll, afterEach, beforeAll, describe, expect, it } from 'vitest';
import { screen, waitFor } from '@testing-library/react';

import ActorsListPage from './ActorsListPage';
import { handlers } from '../../../shared/lib/test/handlers';
import { renderWithProviders } from '../../../shared/lib/test/render';
import { server } from '../../../shared/lib/test/server';

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

server.use(...handlers);

describe('ActorsListPage', () => {
  it('renders actor results from the API', async () => {
    renderWithProviders(<ActorsListPage />, { route: '/actors' });

    await waitFor(() => {
      expect(screen.getByText('Amy Adams')).toBeInTheDocument();
    });
  });
});
