import React, { useEffect } from 'react';
import { useProtonQuery } from '../hooks/useProtonQuery';
import PageHeader from '../components/PageHeader';

function statusBadge(status) {
  if (status === 'success') return 'bg-[#87fd6f]/40 text-[#035300]';
  if (status === 'error') return 'bg-obs-error text-white';
  return 'bg-error-container text-on-error-container';
}

export default function ToolLogs() {
  const { data: metrics, loading: metricsLoading, query: queryMetrics } = useProtonQuery();
  const { data, loading, error, query } = useProtonQuery();

  const load = () => {
    queryMetrics(`SELECT count() as total, round(avg(duration_ms)) as avg_latency, round(countIf(status='success') * 100.0 / count()) as success_rate FROM table(pulsebot.tool_logs)`);
    query(`SELECT id, timestamp, session_id, tool_name, skill_name, status, duration_ms, result_preview, error_message FROM table(pulsebot.tool_logs) ORDER BY timestamp DESC LIMIT 200`);
  };

  useEffect(() => { load(); }, []);

  const m = metrics[0] || {};

  return (
    <div className="flex flex-col h-full overflow-hidden">
      <PageHeader onRefresh={load} loading={loading || metricsLoading} />

      <main className="flex-1 overflow-y-auto">
        <div className="p-8 max-w-7xl mx-auto">
          {/* Page Header */}
          <div className="flex justify-between items-end mb-8">
            <div>
              <span className="text-[11px] font-semibold uppercase tracking-[0.05em] text-secondary">Monitoring</span>
              <h2 className="text-2xl font-bold text-on-surface">Tool Logs</h2>
            </div>
          </div>

          {/* Metric Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <div className="bg-surface-container-lowest p-5 rounded-lg shadow-[0_4px_20px_rgba(26,28,28,0.06)] border border-outline-variant/10">
              <p className="text-[11px] font-bold uppercase tracking-wider text-secondary mb-1">Total Tool Calls</p>
              <div className="flex items-baseline space-x-2">
                <span className="text-3xl font-bold text-on-surface">{m.total != null ? Number(m.total).toLocaleString() : '—'}</span>
              </div>
            </div>
            <div className="bg-surface-container-lowest p-5 rounded-lg shadow-[0_4px_20px_rgba(26,28,28,0.06)] border border-outline-variant/10">
              <p className="text-[11px] font-bold uppercase tracking-wider text-secondary mb-1">Avg Latency</p>
              <div className="flex items-baseline space-x-2">
                <span className="text-3xl font-bold text-on-surface">{m.avg_latency ? `${m.avg_latency}ms` : '—'}</span>
              </div>
            </div>
            <div className="bg-surface-container-lowest p-5 rounded-lg shadow-[0_4px_20px_rgba(26,28,28,0.06)] border border-outline-variant/10">
              <p className="text-[11px] font-bold uppercase tracking-wider text-secondary mb-1">Success Rate</p>
              <div className="flex items-baseline space-x-2">
                <span className="text-3xl font-bold text-on-surface">{m.success_rate != null ? `${m.success_rate}%` : '—'}</span>
                {m.success_rate != null && (
                  <span className={`text-xs font-medium ${m.success_rate >= 95 ? 'text-tertiary' : 'text-obs-error'}`}>
                    {m.success_rate >= 95 ? 'Stable' : 'Degraded'}
                  </span>
                )}
              </div>
            </div>
            <div className="bg-surface-container-lowest p-5 rounded-lg shadow-[0_4px_20px_rgba(26,28,28,0.06)] border border-outline-variant/10">
              <p className="text-[11px] font-bold uppercase tracking-wider text-secondary mb-1">Unique Tools</p>
              <div className="flex items-baseline space-x-2">
                <span className="text-3xl font-bold text-on-surface">
                  {data.length > 0 ? new Set(data.map(r => r.tool_name)).size : '—'}
                </span>
                <span className="text-xs font-medium text-secondary">Global</span>
              </div>
            </div>
          </div>

          {/* Tabular Log View */}
          <div className="bg-surface-container-lowest rounded-lg shadow-[0_4px_20px_rgba(26,28,28,0.06)] overflow-hidden">
            {error && (
              <div className="px-6 py-3 text-sm text-on-error-container bg-error-container">Error: {error}</div>
            )}
            <div className="overflow-x-auto">
              {loading ? (
                <div className="px-6 py-12 text-center text-sm text-secondary">Loading...</div>
              ) : data.length === 0 ? (
                <div className="px-6 py-12 text-center text-sm text-secondary">No tool call records found</div>
              ) : (
                <table className="w-full text-left border-collapse">
                  <thead>
                    <tr className="bg-surface-container-low border-none">
                      <th className="px-6 py-4 text-[11px] font-bold uppercase tracking-widest text-secondary">Timestamp</th>
                      <th className="px-6 py-4 text-[11px] font-bold uppercase tracking-widest text-secondary">Tool Name</th>
                      <th className="px-6 py-4 text-[11px] font-bold uppercase tracking-widest text-secondary">Skill</th>
                      <th className="px-6 py-4 text-[11px] font-bold uppercase tracking-widest text-secondary">Latency</th>
                      <th className="px-6 py-4 text-[11px] font-bold uppercase tracking-widest text-secondary">Status</th>
                      <th className="px-6 py-4 text-[11px] font-bold uppercase tracking-widest text-secondary">Result</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-transparent">
                    {data.map((row, i) => (
                      <tr
                        key={row.id || i}
                        className={`hover:bg-surface-container transition-colors group ${i % 2 === 1 ? 'bg-surface-container-low' : ''}`}
                      >
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className="text-xs font-mono text-secondary">
                            {row.timestamp ? new Date(row.timestamp).toLocaleString() : '—'}
                          </span>
                        </td>
                        <td className="px-6 py-4">
                          <code className="text-sm font-semibold text-primary px-2 py-0.5 bg-primary-fixed/30 rounded">
                            {row.tool_name}
                          </code>
                        </td>
                        <td className="px-6 py-4 text-sm font-medium text-secondary">{row.skill_name || '—'}</td>
                        <td className="px-6 py-4 text-sm font-mono text-on-surface">
                          {row.duration_ms != null ? `${row.duration_ms}ms` : '—'}
                        </td>
                        <td className="px-6 py-4">
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider ${statusBadge(row.status)}`}>
                            {row.status}
                          </span>
                        </td>
                        <td className="px-6 py-4 text-xs text-secondary max-w-xs">
                          {row.status !== 'success' && row.error_message ? (
                            <span className="text-obs-error font-mono truncate block" title={row.error_message}>
                              {row.error_message}
                            </span>
                          ) : row.result_preview ? (
                            <span className="font-mono truncate block text-secondary" title={row.result_preview}>
                              {row.result_preview}
                            </span>
                          ) : '—'}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
            <div className="px-6 py-4 bg-surface-container-low flex justify-between items-center border-none">
              <span className="text-xs text-secondary font-medium">
                Showing {data.length} tool executions
              </span>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
