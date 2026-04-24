const fallbackApiBaseUrl = '/api/v1';

export function getApiBaseUrl() {
  const raw = import.meta.env.VITE_API_BASE_URL as string | undefined;
  const value = raw?.trim() ?? '';

  if (value) {
    return value.replace(/\/+$/, '');
  }

  if (import.meta.env.MODE === 'test') {
    return 'http://localhost:8000/api/v1';
  }

  return fallbackApiBaseUrl;
}
