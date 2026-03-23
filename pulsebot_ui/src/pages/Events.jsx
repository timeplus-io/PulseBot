import React, { useEffect } from 'react';
import { useProtonQuery } from '../hooks/useProtonQuery';

function severityBadge(sev) {
  const map = {
    error: 'bg-obs-error/10 text-obs-error',
    warn: 'bg-[#fff3cd] text-[#856404]',
    warning: 'bg-[#fff3cd] text-[#856404]',
    info: 'bg-tertiary/10 text-tertiary',
    debug: 'bg-secondary/10 text-secondary',
  };
  return map[sev] || 'bg-secondary/10 text-secondary';
}

function initials(str) {
  if (!str) return '??';
  return str.split(/[_\-\s]/).slice(0, 2).map(w => w[0]?.toUpperCase() || '').join('');
}

function sourceColor(source) {
  const colors = [
    'bg-primary-fixed text-on-primary-fixed-variant',
    'bg-secondary-container text-on-secondary-fixed-variant',
    'bg-error-container text-on-error-container',
    'bg-[#e8f5e9] text-[#2e7d32]',
  ];
  const hash = (source || '').split('').reduce((a, c) => a + c.charCodeAt(0), 0);
  return colors[hash % colors.length];
}

export default function Events() {
  const { data: stats, loading: statsLoading, query: queryStats } = useProtonQuery();
  const { data, loading, error, query } = useProtonQuery();

  const load = () => {
    queryStats(`SELECT count() as total, countIf(severity='error') as errors FROM table(pulsebot.events)`);
    query(`SELECT id, timestamp, event_type, source, severity, payload FROM table(pulsebot.events) ORDER BY timestamp DESC LIMIT 200`);
  };

  useEffect(() => { load(); }, []);

  const st = stats[0] || {};

  return (
    <div className="flex flex-col h-full overflow-hidden">
      {/* TopAppBar */}
      <header className="glass-header ambient-shadow sticky top-0 z-50 flex justify-between items-center w-full px-6 py-3 flex-shrink-0">
        <div className="flex items-center gap-4">
          <span className="text-xl font-bold tracking-tight text-primary">Events Monitor</span>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={load}
            disabled={loading || statsLoading}
            className="px-4 py-2 primary-gradient text-on-primary text-sm font-medium rounded-lg ambient-shadow flex items-center gap-2 active:scale-95 transition-transform disabled:opacity-50"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`}>
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Refresh
          </button>
        </div>
      </header>

      <div className="flex-1 overflow-y-auto p-8 max-w-7xl mx-auto w-full space-y-8">
        {/* Headline */}
        <div className="flex items-end justify-between">
          <div>
            <p className="text-[11px] font-semibold uppercase tracking-[0.05em] text-secondary mb-1">Monitoring Suite</p>
            <h2 className="text-2xl font-bold text-on-surface">Events Monitor</h2>
          </div>
        </div>

        {/* Stats Bento Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-surface-container-lowest p-6 rounded-lg ambient-shadow border border-outline-variant/10 flex flex-col justify-between h-32">
            <div className="flex justify-between items-start">
              <span className="text-[11px] font-semibold uppercase tracking-[0.05em] text-secondary">Total Events</span>
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-5 h-5 text-tertiary">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.75" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <div className="flex items-baseline gap-2">
              <span className="text-3xl font-bold text-on-surface">{st.total ?? '—'}</span>
            </div>
          </div>
          <div className="bg-surface-container-lowest p-6 rounded-lg ambient-shadow border border-outline-variant/10 flex flex-col justify-between h-32">
            <div className="flex justify-between items-start">
              <span className="text-[11px] font-semibold uppercase tracking-[0.05em] text-secondary">Event Sources</span>
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-5 h-5 text-primary">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.75" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
              </svg>
            </div>
            <div className="flex items-baseline gap-2">
              <span className="text-3xl font-bold text-on-surface">{data.length > 0 ? new Set(data.map(r => r.source)).size : '—'}</span>
              <span className="text-primary text-[11px] font-bold">sources</span>
            </div>
          </div>
          <div className="bg-surface-container-lowest p-6 rounded-lg ambient-shadow border border-outline-variant/10 flex flex-col justify-between h-32">
            <div className="flex justify-between items-start">
              <span className="text-[11px] font-semibold uppercase tracking-[0.05em] text-secondary">Critical Errors</span>
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-5 h-5 text-obs-error">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.75" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
            <div className="flex items-baseline gap-2">
              <span className="text-3xl font-bold text-on-surface">{st.errors ?? '—'}</span>
              <span className={`text-[11px] font-bold ${st.errors > 0 ? 'text-obs-error' : 'text-tertiary'}`}>
                {st.errors > 0 ? 'Active' : 'None'}
              </span>
            </div>
          </div>
        </div>

        {/* Event Log Table */}
        <div className="bg-surface-container-lowest rounded-lg ambient-shadow overflow-hidden border border-outline-variant/10">
          <div className="px-6 py-4 border-b border-outline-variant/10 flex justify-between items-center">
            <h3 className="text-sm font-semibold text-on-surface uppercase tracking-wider">Event Log</h3>
            <div className="flex gap-4">
              <div className="flex items-center gap-2 text-[11px] text-secondary font-medium">
                <span className="w-2 h-2 rounded-full bg-tertiary"></span> System
              </div>
              <div className="flex items-center gap-2 text-[11px] text-secondary font-medium">
                <span className="w-2 h-2 rounded-full bg-primary"></span> Agent
              </div>
            </div>
          </div>
          {error && (
            <div className="px-6 py-3 text-sm text-on-error-container bg-error-container">Error: {error}</div>
          )}
          <div className="overflow-x-auto">
            {loading ? (
              <div className="px-6 py-12 text-center text-sm text-secondary">Loading...</div>
            ) : data.length === 0 ? (
              <div className="px-6 py-12 text-center text-sm text-secondary">No events found</div>
            ) : (
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-surface-container-low">
                    <th className="px-6 py-3 text-[11px] font-bold text-secondary uppercase tracking-widest">Timestamp</th>
                    <th className="px-6 py-3 text-[11px] font-bold text-secondary uppercase tracking-widest">Source</th>
                    <th className="px-6 py-3 text-[11px] font-bold text-secondary uppercase tracking-widest">Event Type</th>
                    <th className="px-6 py-3 text-[11px] font-bold text-secondary uppercase tracking-widest">Status</th>
                    <th className="px-6 py-3 text-[11px] font-bold text-secondary uppercase tracking-widest">Payload</th>
                  </tr>
                </thead>
                <tbody className="text-sm">
                  {data.map((row, i) => (
                    <tr
                      key={row.id || i}
                      className={`hover:bg-surface transition-colors ${i % 2 === 1 ? 'bg-surface-container-low/30' : ''}`}
                    >
                      <td className="px-6 py-4 font-medium text-secondary tabular-nums text-xs whitespace-nowrap">
                        {row.timestamp ? new Date(row.timestamp).toLocaleString() : '—'}
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-2">
                          <div className={`w-6 h-6 rounded flex items-center justify-center text-[10px] font-bold ${sourceColor(row.source)}`}>
                            {initials(row.source)}
                          </div>
                          <span className="font-semibold text-on-surface text-xs">{row.source}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4 text-on-surface/80 text-xs font-mono">{row.event_type}</td>
                      <td className="px-6 py-4">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${severityBadge(row.severity)}`}>
                          {row.severity}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-xs text-secondary max-w-xs truncate font-mono">
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
