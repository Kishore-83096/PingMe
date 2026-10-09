import { useState } from "react";

import {
  checkBackendHealth,
  type HealthResponse,
} from "./services/api/health";

function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleHealthCheck() {
    setLoading(true);
    setHealth(null);
    setError(null);

    try {
      const result = await checkBackendHealth();
      setHealth(result);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to connect to PingMe backend",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-950 px-6 text-white">
      <div className="w-full max-w-2xl rounded-3xl border border-slate-800 bg-slate-900 p-8 shadow-2xl">
        
        <div className="mb-8">
          <p className="mb-2 text-sm font-medium uppercase tracking-[0.25em] text-blue-400">
            PingMe
          </p>

          <h1 className="text-4xl font-bold tracking-tight">
            Backend Connection
          </h1>

          <p className="mt-3 text-slate-400">
            Testing the local React frontend against the PingMe Nginx API.
          </p>
        </div>

        <div className="rounded-2xl border border-slate-800 bg-slate-950 p-5">
          <p className="mb-3 text-sm text-slate-400">
            API Endpoint
          </p>

          <code className="break-all text-sm text-blue-300">
            {import.meta.env.VITE_API_BASE_URL}/api/health/
          </code>
        </div>

        <button
          type="button"
          onClick={handleHealthCheck}
          disabled={loading}
          className="mt-6 w-full rounded-xl bg-blue-600 px-5 py-3 font-semibold transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading ? "Checking connection..." : "Check Backend Connection"}
        </button>

        {health && (
          <div className="mt-6 rounded-2xl border border-emerald-800 bg-emerald-950/40 p-5">
            <div className="mb-4 flex items-center gap-3">
              <div className="h-3 w-3 rounded-full bg-emerald-400" />

              <h2 className="font-semibold text-emerald-300">
                Backend Connected
              </h2>
            </div>

            <div className="space-y-2 text-sm">
              <p>
                <span className="text-slate-400">Status:</span>{" "}
                {health.status}
              </p>

              <p>
                <span className="text-slate-400">PostgreSQL:</span>{" "}
                {health.database}
              </p>

              <p>
                <span className="text-slate-400">Redis/Valkey:</span>{" "}
                {health.redis}
              </p>
            </div>
          </div>
        )}

        {error && (
          <div className="mt-6 rounded-2xl border border-red-800 bg-red-950/40 p-5">
            <h2 className="mb-2 font-semibold text-red-300">
              Connection Failed
            </h2>

            <p className="break-words text-sm text-red-200">
              {error}
            </p>
          </div>
        )}
      </div>
    </main>
  );
}

export default App;