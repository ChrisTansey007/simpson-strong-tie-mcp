import { useQuery } from '@tanstack/react-query';

interface HealthResponse {
  status: string;
  version: string;
}

interface ReadinessResponse {
  status: string;
  database_connected: boolean;
}

export default function App() {
  const { data: health, isLoading: healthLoading, isError: healthError } = useQuery<HealthResponse>({
    queryKey: ['health'],
    queryFn: async () => {
      const res = await fetch('/api/health');
      if (!res.ok) throw new Error('API request failed');
      return res.json();
    },
    refetchInterval: 5000,
  });

  const { data: ready } = useQuery<ReadinessResponse>({
    queryKey: ['ready'],
    queryFn: async () => {
      const res = await fetch('/api/ready');
      if (!res.ok) return { status: 'offline', database_connected: false };
      return res.json();
    },
    refetchInterval: 5000,
  });

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-8">
      <header className="max-w-6xl mx-auto flex items-center justify-between pb-8 border-b border-slate-800">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold tracking-tight text-amber-500">Simpson Strong-Tie Expert MCP</h1>
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/20">
              Admin & Human Verification
            </span>
          </div>
          <p className="text-slate-400 text-sm mt-1">
            System status monitoring and engineering claim verification gate
          </p>
        </div>

        <div className="flex items-center gap-2">
          <div className={`w-3 h-3 rounded-full ${health?.status === 'ok' ? 'bg-emerald-500 shadow-emerald-500/50 shadow-lg' : 'bg-rose-500'}`} />
          <span className="text-xs font-mono uppercase tracking-wider text-slate-300">
            {healthLoading ? 'CONNECTING...' : healthError ? 'DISCONNECTED' : 'SYSTEM ONLINE'}
          </span>
        </div>
      </header>

      <main className="max-w-6xl mx-auto mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
          <div className="text-xs uppercase tracking-wider font-semibold text-slate-400">Admin API Status</div>
          <div className="text-3xl font-bold mt-2 text-slate-100">
            {healthLoading ? '...' : healthError ? 'Offline' : 'Healthy'}
          </div>
          <p className="text-xs text-slate-500 mt-2 font-mono">Version: {health?.version || '0.1.0'}</p>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
          <div className="text-xs uppercase tracking-wider font-semibold text-slate-400">PostgreSQL + pgvector</div>
          <div className="text-3xl font-bold mt-2 text-slate-100">
            {ready?.database_connected ? (
              <span className="text-emerald-400">Connected</span>
            ) : (
              <span className="text-amber-400">Standby / Unreachable</span>
            )}
          </div>
          <p className="text-xs text-slate-500 mt-2 font-mono">Extension: vector & pg_trgm</p>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
          <div className="text-xs uppercase tracking-wider font-semibold text-slate-400">MCP Server Foundation</div>
          <div className="text-3xl font-bold mt-2 text-emerald-400">Ready</div>
          <p className="text-xs text-slate-500 mt-2 font-mono">SDK Constraint: mcp &gt;= 1.27, &lt; 2</p>
        </div>
      </main>
    </div>
  );
}
