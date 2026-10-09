const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

if (!API_BASE_URL) {
  throw new Error("VITE_API_BASE_URL is not configured");
}

export interface HealthResponse {
  status: string;
  database: string;
  redis: string;
}

export async function checkBackendHealth(): Promise<HealthResponse> {
  const response = await fetch(
    `${API_BASE_URL}/api/health/`,
    {
      method: "GET",
      headers: {
        Accept: "application/json",
      },
    },
  );

  if (!response.ok) {
    throw new Error(
      `Backend health check failed with status ${response.status}`,
    );
  }

  return response.json();
}