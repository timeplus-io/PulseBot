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

export default function ToolLogs() {
  const { data, loading, error, query } = useProtonQuery();

  const load = () => {
    query(`SELECT id, timestamp, session_id, tool_name, skill_name, status, duration_ms, result_preview, error_message FROM table(pulsebot.tool_logs) ORDER BY timestamp DESC LIMIT 200`);
  };

  useEffect(() => { load(); }, []);

  return (
    <div className="flex flex-col h-full overflow-hidden">
      {/* Header */}
      <header className="glass-header ambient-shadow border-b border-surface-container-high px-6 py-4 flex items-center gap-3 flex-shrink-0">
        <h1 className="text-base font-semibold text-on-surface">Tool Logs</h1>
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
              <div className="px-5 py-12 text-center text-sm text-on-surface-variant">No tool call records found</div>
            ) : (
              <table className="w-full text-sm">
                <thead>
                  <tr className="bg-surface-container border-b border-surface-container-high">
                    <th className="text-left px-5 py-3 text-xs font-semibold text-on-surface-variant uppercase tracking-wide whitespace-nowrap">Time</th>
                    <th className="text-left px-5 py-3 text-xs font-semibold text-on-surface-variant uppercase tracking-wide whitespace-nowrap">Tool</th>
                    <th className="text-left px-5 py-3 text-xs font-semibold text-on-surface-variant uppercase tracking-wide whitespace-nowrap">Skill</th>
                    <th className="text-left px-5 py-3 text-xs font-semibold text-on-surface-variant uppercase tracking-wide whitespace-nowrap">Duration</th>
                    <th className="text-left px-5 py-3 text-xs font-semibold text-on-surface-variant uppercase tracking-wide whitespace-nowrap">Status</th>
                    <th className="text-left px-5 py-3 text-xs font-semibold text-on-surface-variant uppercase tracking-wide">Result</th>
                  </tr>
                </thead>
                <tbody>
                  {data.map((row, i) => (
                    <tr key={row.id || i} className="border-b border-surface-container last:border-0 hover:bg-surface-container-low transition-colors">
                      <td className="px-5 py-3 text-xs text-on-surface-variant whitespace-nowrap font-mono">
                        {row.timestamp ? new Date(row.timestamp).toLocaleString() : '—'}
                      </td>
                      <td className="px-5 py-3 font-mono text-xs text-on-surface font-medium whitespace-nowrap">
                        {row.tool_name}
                      </td>
                      <td className="px-5 py-3 text-xs text-on-surface-variant whitespace-nowrap">{row.skill_name}</td>
                      <td className="px-5 py-3 text-xs text-on-surface-variant font-mono whitespace-nowrap">
                        {row.duration_ms != null ? `${row.duration_ms}ms` : '—'}
                      </td>
                      <td className="px-5 py-3 whitespace-nowrap">
                        <span className={`inline-flex px-2 py-0.5 rounded text-xs font-medium ${statusStyle(row.status)}`}>
                          {row.status}
                        </span>
                      </td>
                      <td className="px-5 py-3 text-xs text-on-surface-variant max-w-xs">
                        {row.status !== 'success' && row.error_message ? (
                          <div className="text-obs-error font-mono truncate" title={row.error_message}>
                            {row.error_message}
                          </div>
                        ) : row.result_preview ? (
                          <div className="font-mono truncate text-on-surface-variant" title={row.result_preview}>
                            {row.result_preview}
                          </div>
                        ) : (
                          <span className="text-outline">—</span>
                        )}
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
