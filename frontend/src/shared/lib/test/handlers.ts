import { http, HttpResponse } from 'msw';

const movieList = [
  {
    id: 1,
    title: 'Arrival',
    release_year: 2016,
    poster_url: null,
    average_rating: 4.4,
    genres: [{ id: 1, name: 'Sci-Fi', slug: 'sci-fi' }],
    director: { id: 1, name: 'Denis Villeneuve', birth_year: 1967 },
  },
];

const movieDetail = {
  ...movieList[0],
  synopsis:
    'A linguist is recruited to interpret the language of visitors from another world.',
  runtime_minutes: 116,
  actors: [{ id: 8, name: 'Amy Adams', birth_year: 1974 }],
  reviews: [
    {
      id: 1,
      movie_id: 1,
      author_name: 'Alex',
      rating: 5,
      comment: 'Quiet, emotional, and surprisingly tense.',
      created_at: '2024-04-01T12:00:00Z',
    },
  ],
};

function envelope<T>(
  data: T,
  pagination?: {
    page: number;
    page_size: number;
    total: number;
    total_pages: number;
  },
) {
  return {
    success: true,
    data,
    error: null,
    meta: {
      request_id: 'test-request-id',
      pagination: pagination ?? null,
    },
  };
}

export const handlers = [
  http.get('http://localhost:8000/api/v1/movies', () =>
    HttpResponse.json(
      envelope(movieList, { page: 1, page_size: 12, total: 1, total_pages: 1 }),
    ),
  ),
  http.get('http://localhost:8000/api/v1/movies/1', () =>
    HttpResponse.json(envelope(movieDetail)),
  ),
  http.get('http://localhost:8000/api/v1/genres', () =>
    HttpResponse.json(envelope([{ id: 1, name: 'Sci-Fi', slug: 'sci-fi' }])),
  ),
  http.get('http://localhost:8000/api/v1/directors', () =>
    HttpResponse.json(
      envelope([{ id: 1, name: 'Denis Villeneuve', birth_year: 1967 }], {
        page: 1,
        page_size: 100,
        total: 1,
        total_pages: 1,
      }),
    ),
  ),
  http.get('http://localhost:8000/api/v1/actors', () =>
    HttpResponse.json(
      envelope([{ id: 8, name: 'Amy Adams', birth_year: 1974 }], {
        page: 1,
        page_size: 100,
        total: 1,
        total_pages: 1,
      }),
    ),
  ),
  http.get('http://localhost:8000/api/v1/actors/:actorId', () =>
    HttpResponse.json(
      envelope({ id: 8, name: 'Amy Adams', birth_year: 1974, bio: 'Bio' }),
    ),
  ),
  http.get('http://localhost:8000/api/v1/actors/:actorId/movies', () =>
    HttpResponse.json(
      envelope(movieList, { page: 1, page_size: 20, total: 1, total_pages: 1 }),
    ),
  ),
  http.get('http://localhost:8000/api/v1/directors/:directorId', () =>
    HttpResponse.json(
      envelope({
        id: 1,
        name: 'Denis Villeneuve',
        birth_year: 1967,
        bio: 'Bio',
      }),
    ),
  ),
  http.get('http://localhost:8000/api/v1/directors/:directorId/movies', () =>
    HttpResponse.json(
      envelope(movieList, { page: 1, page_size: 20, total: 1, total_pages: 1 }),
    ),
  ),
  http.get('http://localhost:8000/api/v1/genres/:genreId', () =>
    HttpResponse.json(envelope({ id: 1, name: 'Sci-Fi', slug: 'sci-fi' })),
  ),
  http.get('http://localhost:8000/api/v1/genres/:genreId/movies', () =>
    HttpResponse.json(
      envelope(movieList, { page: 1, page_size: 20, total: 1, total_pages: 1 }),
    ),
  ),
];
