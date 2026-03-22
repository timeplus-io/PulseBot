import React, { useEffect } from 'react';
import { useProtonQuery } from '../hooks/useProtonQuery';

function StatCard({ label, value, sub, color = 'primary' }) {
  const colors = {
    primary: 'bg-primary-fixed text-on-primary-fixed',
    secondary: 'bg-secondary-container text-on-secondary-fixed',
    tertiary: 'bg-on-tertiary-container text-tertiary',
    error: 'bg-error-container text-on-error-container',
  };
  return (
    <div className={`rounded-lg p-5 flex flex-col gap-1 ambient-shadow ${colors[color] || colors.primary}`}>
      <span className="text-xs font-medium uppercase tracking-wide opacity-70">{label}</span>
      <span className="text-3xl font-bold">{value ?? '—'}</span>
      {sub && <span className="text-xs opacity-60">{sub}</span>}
    </div>
  );
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

export default function Dashboard() {
  const { data: eventStats, loading: eventsLoading, query: queryEvents } = useProtonQuery();
  const { data: llmStats, loading: llmLoading, query: queryLlm } = useProtonQuery();
  const { data: toolStats, loading: toolLoading, query: queryTools } = useProtonQuery();
  const { data: recentEvents, loading: recentLoading, query: queryRecent } = useProtonQuery();

  const load = () => {
    queryEvents(`SELECT count() as total, countIf(severity='error') as errors FROM table(pulsebot.events)`);
    queryLlm(`SELECT count() as total, sum(total_tokens) as tokens, round(avg(latency_ms)) as avg_latency FROM table(pulsebot.llm_logs)`);
    queryTools(`SELECT count() as total, countIf(status='success') as success FROM table(pulsebot.tool_logs)`);
    queryRecent(`SELECT timestamp, event_type, source, severity, payload FROM table(pulsebot.events) ORDER BY timestamp DESC LIMIT 10`);
  };

  useEffect(() => { load(); }, []);

  const isLoading = eventsLoading || llmLoading || toolLoading || recentLoading;

  const ev = eventStats[0] || {};
  const llm = llmStats[0] || {};
  const tool = toolStats[0] || {};

  const successRate = tool.total > 0 ? Math.round((tool.success / tool.total) * 100) : null;

  function severityBadge(sev) {
    const map = {
      error: 'bg-error-container text-on-error-container',
      warn: 'bg-[#fff3cd] text-[#856404]',
      info: 'bg-secondary-container text-on-secondary-fixed',
      debug: 'bg-surface-container text-on-surface-variant',
    };
    return map[sev] || map.info;
  }

  return (
    <div className="flex flex-col h-full overflow-hidden">
      {/* Header */}
      <header className="glass-header ambient-shadow border-b border-surface-container-high px-6 py-4 flex items-center gap-3 flex-shrink-0">
        <h1 className="text-base font-semibold text-on-surface">Dashboard</h1>
        <div className="ml-auto">
          <RefreshButton onClick={load} loading={isLoading} />
        </div>
      </header>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-6">
        {/* Stat Cards */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <StatCard
            label="Total Events"
            value={ev.total}
            sub={ev.errors > 0 ? `${ev.errors} errors` : 'No errors'}
            color={ev.errors > 0 ? 'error' : 'secondary'}
          />
          <StatCard
            label="LLM Calls"
            value={llm.total}
            sub={llm.avg_latency ? `${llm.avg_latency}ms avg latency` : undefined}
            color="primary"
          />
          <StatCard
            label="Total Tokens"
            value={llm.tokens ? Number(llm.tokens).toLocaleString() : undefined}
            sub="across all LLM calls"
            color="secondary"
          />
          <StatCard
            label="Tool Calls"
            value={tool.total}
            sub={successRate !== null ? `${successRate}% success rate` : undefined}
            color={successRate !== null && successRate < 80 ? 'error' : 'tertiary'}
          />
        </div>

        {/* Recent Events */}
        <div className="bg-surface-container-lowest rounded-lg ambient-shadow">
          <div className="px-5 py-4 border-b border-surface-container-high flex items-center">
            <h2 className="text-sm font-semibold text-on-surface">Recent Events</h2>
          </div>
          <div className="overflow-x-auto">
            {recentLoading ? (
              <div className="px-5 py-8 text-center text-sm text-on-surface-variant">Loading...</div>
            ) : recentEvents.length === 0 ? (
              <div className="px-5 py-8 text-center text-sm text-on-surface-variant">No events found</div>
            ) : (
              <table className="w-full text-sm">
                <thead>
                  <tr className="bg-surface-container border-b border-surface-container-high">
                    <th className="text-left px-5 py-3 text-xs font-semibold text-on-surface-variant uppercase tracking-wide">Time</th>
                    <th className="text-left px-5 py-3 text-xs font-semibold text-on-surface-variant uppercase tracking-wide">Type</th>
                    <th className="text-left px-5 py-3 text-xs font-semibold text-on-surface-variant uppercase tracking-wide">Source</th>
                    <th className="text-left px-5 py-3 text-xs font-semibold text-on-surface-variant uppercase tracking-wide">Severity</th>
                    <th className="text-left px-5 py-3 text-xs font-semibold text-on-surface-variant uppercase tracking-wide">Payload</th>
                  </tr>
                </thead>
                <tbody>
                  {recentEvents.map((row, i) => (
                    <tr key={i} className="border-b border-surface-container last:border-0 hover:bg-surface-container-low transition-colors">
                      <td className="px-5 py-3 text-xs text-on-surface-variant whitespace-nowrap font-mono">
                        {row.timestamp ? new Date(row.timestamp).toLocaleTimeString() : '—'}
                      </td>
                      <td className="px-5 py-3 font-mono text-xs text-on-surface">{row.event_type}</td>
                      <td className="px-5 py-3 text-xs text-on-surface">{row.source}</td>
                      <td className="px-5 py-3">
                        <span className={`inline-flex px-2 py-0.5 rounded text-xs font-medium ${severityBadge(row.severity)}`}>
                          {row.severity}
                        </span>
                      </td>
                      <td className="px-5 py-3 text-xs text-on-surface-variant max-w-xs truncate font-mono">
                        {typeof row.payload === 'object' ? JSON.stringify(row.payload) : String(row.payload || '')}
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
