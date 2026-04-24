import { getApiBaseUrl } from './env';
import type { Envelope, ErrorPayload } from '../types';

export class ApiError extends Error {
  status: number;
  code: string;
  details?: Record<string, unknown> | null;
  requestId?: string | null;

  constructor(
    message: string,
    options: {
      status: number;
      code?: string;
      details?: Record<string, unknown> | null;
      requestId?: string | null;
    },
  ) {
    super(message);
    this.name = 'ApiError';
    this.status = options.status;
    this.code = options.code ?? 'unknown_error';
    this.details = options.details;
    this.requestId = options.requestId;
  }
}

function normalizeParams(params?: Record<string, string | number | undefined>) {
  const searchParams = new URLSearchParams();

  if (!params) {
    return '';
  }

  for (const [key, value] of Object.entries(params)) {
    if (value == null || value === '') {
      continue;
    }

    searchParams.set(key, String(value));
  }

  const serialized = searchParams.toString();
  return serialized ? `?${serialized}` : '';
}

async function parseEnvelope<T>(response: Response): Promise<Envelope<T>> {
  const payload = (await response.json()) as Envelope<T>;

  if (!response.ok || payload.success === false) {
    const error = payload.error as ErrorPayload | undefined;
    throw new ApiError(error?.message ?? 'Request failed', {
      status: response.status,
      code: error?.code,
      details: error?.details ?? null,
      requestId:
        payload.meta?.request_id ?? response.headers.get('x-request-id'),
    });
  }

  return payload;
}

export async function apiGet<T>(
  path: string,
  params?: Record<string, string | number | undefined>,
): Promise<{ data: T; meta: Envelope<T>['meta'] }> {
  const response = await fetch(
    `${getApiBaseUrl()}${path}${normalizeParams(params)}`,
    {
      headers: {
        Accept: 'application/json',
      },
    },
  );

  const payload = await parseEnvelope<T>(response);

  return {
    data: payload.data as T,
    meta: payload.meta,
  };
}
