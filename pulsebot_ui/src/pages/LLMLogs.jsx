import React, { useEffect } from 'react';
import { useProtonQuery } from '../hooks/useProtonQuery';

function statusStyle(status) {
  if (status === 'success') return 'bg-on-tertiary-container text-tertiary';
  if (status === 'error') return 'bg-error-container text-on-error-container';
  return 'bg-surface-container text-on-surface-variant';
}

function RefreshButton({ onClick, loading }) {
  return (
    <button
      onClick={onClick}
      disabled={loading}
      className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-on-surface-variant bg-surface-container hover:bg-surface-container-high rounded transition-colors disabled:opacity-50"
    >
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`}>
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
      </svg>
      Refresh
    </button>
  );
}

function LatencyBar({ ms, max }) {
  if (!ms || !max) return null;
  const pct = Math.min((ms / max) * 100, 100);
  const color = ms > 5000 ? 'bg-obs-error' : ms > 2000 ? 'bg-[#ffc107]' : 'bg-tertiary';
  return (
    <div className="flex items-center gap-2">
      <div className="w-16 h-1.5 bg-surface-container rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${pct}%` }} />
      </div>
      <span className="text-xs font-mono text-on-surface-variant">{ms}ms</span>
    </div>
  );
}

export default function LLMLogs() {
  const { data, loading, error, query } = useProtonQuery();

  const load = () => {
    query(`SELECT id, timestamp, session_id, model, provider, input_tokens, output_tokens, total_tokens, latency_ms, status, error_message FROM table(pulsebot.llm_logs) ORDER BY timestamp DESC LIMIT 200`);
  };

  useEffect(() => { load(); }, []);

  const maxLatency = data.length > 0 ? Math.max(...data.map(r => r.latency_ms || 0)) : 1;

  return (
    <div className="flex flex-col h-full overflow-hidden">
      {/* Header */}
      <header className="glass-header ambient-shadow border-b border-surface-container-high px-6 py-4 flex items-center gap-3 flex-shrink-0">
        <h1 className="text-base font-semibold text-on-surface">LLM Calls</h1>
        {data.length > 0 && (
          <span className="text-xs text-on-surface-variant bg-surface-container px-2 py-1 rounded">
            {data.length} records
          </span>
        )}
        <div className="ml-auto">
          <RefreshButton onClick={load} loading={loading} />
        </div>
      </header>

      {/* Table */}
      <div className="flex-1 overflow-auto p-6">
        <div className="bg-surface-container-lowest rounded-lg ambient-shadow">
          {error && (
            <div className="px-5 py-4 text-sm text-on-error-container bg-error-container rounded-t-lg">
              Error: {error}
            </div>
          )}
          <div className="overflow-x-auto">
            {loading ? (
              <div className="px-5 py-12 text-center text-sm text-on-surface-variant">Loading...</div>
            ) : data.length === 0 ? (
              <div className="px-5 py-12 text-center text-sm text-on-surface-variant">No LLM call records found</div>
            ) : (
              <table className="w-full text-sm">
                <thead>
                  <tr className="bg-surface-container border-b border-surface-container-high">
                    <th className="text-left px-5 py-3 text-xs font-semibold text-on-surface-variant uppercase tracking-wide whitespace-nowrap">Time</th>
                    <th className="text-left px-5 py-3 text-xs font-semibold text-on-surface-variant uppercase tracking-wide whitespace-nowrap">Model</th>
                    <th className="text-left px-5 py-3 text-xs font-semibold text-on-surface-variant uppercase tracking-wide whitespace-nowrap">Provider</th>
                    <th className="text-left px-5 py-3 text-xs font-semibold text-on-surface-variant uppercase tracking-wide whitespace-nowrap">Tokens (in/out)</th>
                    <th className="text-left px-5 py-3 text-xs font-semibold text-on-surface-variant uppercase tracking-wide whitespace-nowrap">Latency</th>
                    <th className="text-left px-5 py-3 text-xs font-semibold text-on-surface-variant uppercase tracking-wide whitespace-nowrap">Status</th>
                    <th className="text-left px-5 py-3 text-xs font-semibold text-on-surface-variant uppercase tracking-wide whitespace-nowrap">Session</th>
                  </tr>
                </thead>
                <tbody>
                  {data.map((row, i) => (
                    <tr key={row.id || i} className="border-b border-surface-container last:border-0 hover:bg-surface-container-low transition-colors">
                      <td className="px-5 py-3 text-xs text-on-surface-variant whitespace-nowrap font-mono">
                        {row.timestamp ? new Date(row.timestamp).toLocaleString() : '—'}
                      </td>
                      <td className="px-5 py-3 text-xs text-on-surface font-mono whitespace-nowrap">{row.model}</td>
                      <td className="px-5 py-3 text-xs text-on-surface capitalize whitespace-nowrap">{row.provider}</td>
                      <td className="px-5 py-3 text-xs text-on-surface-variant font-mono whitespace-nowrap">
                        {row.input_tokens ?? '?'} / {row.output_tokens ?? '?'}
                        {row.total_tokens && <span className="ml-1 text-on-surface">({row.total_tokens})</span>}
                      </td>
                      <td className="px-5 py-3 whitespace-nowrap">
                        <LatencyBar ms={row.latency_ms} max={maxLatency} />
                      </td>
                      <td className="px-5 py-3 whitespace-nowrap">
                        <span className={`inline-flex px-2 py-0.5 rounded text-xs font-medium ${statusStyle(row.status)}`}>
                          {row.status}
                        </span>
                        {row.error_message && (
                          <div className="text-xs text-obs-error mt-0.5 max-w-[200px] truncate" title={row.error_message}>
                            {row.error_message}
                          </div>
                        )}
                      </td>
                      <td className="px-5 py-3 text-xs text-on-surface-variant font-mono max-w-[120px] truncate">
                        {row.session_id}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
