import React, { useEffect, useState } from 'react';
import { useProtonQuery } from '../hooks/useProtonQuery';

const SEVERITIES = ['all', 'error', 'warn', 'info', 'debug'];

function severityStyle(sev) {
  const map = {
    error: 'bg-error-container text-on-error-container',
    warn: 'bg-[#fff3cd] text-[#856404]',
    info: 'bg-secondary-container text-on-secondary-fixed',
    debug: 'bg-surface-container text-on-surface-variant',
  };
  return map[sev] || map.info;
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

export default function Events() {
  const [severityFilter, setSeverityFilter] = useState('all');
  const { data, loading, error, query } = useProtonQuery();

  const load = () => {
    const where = severityFilter !== 'all' ? `WHERE severity = '${severityFilter}'` : '';
    query(`SELECT id, timestamp, event_type, source, severity, payload, tags FROM table(pulsebot.events) ${where} ORDER BY timestamp DESC LIMIT 200`);
  };

  useEffect(() => { load(); }, [severityFilter]);

  return (
    <div className="flex flex-col h-full overflow-hidden">
      {/* Header */}
      <header className="glass-header ambient-shadow border-b border-surface-container-high px-6 py-4 flex items-center gap-3 flex-shrink-0">
        <h1 className="text-base font-semibold text-on-surface">Events</h1>
        <div className="ml-auto flex items-center gap-3">
          <div className="flex items-center gap-1">
            {SEVERITIES.map((s) => (
              <button
                key={s}
                onClick={() => setSeverityFilter(s)}
                className={`px-3 py-1.5 text-xs font-medium rounded transition-colors capitalize ${
                  severityFilter === s
                    ? 'bg-primary text-on-primary'
                    : 'text-on-surface-variant bg-surface-container hover:bg-surface-container-high'
                }`}
              >
                {s}
              </button>
            ))}
          </div>
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
              <div className="px-5 py-12 text-center text-sm text-on-surface-variant">No events found</div>
            ) : (
              <table className="w-full text-sm">
                <thead>
                  <tr className="bg-surface-container border-b border-surface-container-high">
                    <th className="text-left px-5 py-3 text-xs font-semibold text-on-surface-variant uppercase tracking-wide whitespace-nowrap">Time</th>
                    <th className="text-left px-5 py-3 text-xs font-semibold text-on-surface-variant uppercase tracking-wide whitespace-nowrap">Type</th>
                    <th className="text-left px-5 py-3 text-xs font-semibold text-on-surface-variant uppercase tracking-wide whitespace-nowrap">Source</th>
                    <th className="text-left px-5 py-3 text-xs font-semibold text-on-surface-variant uppercase tracking-wide whitespace-nowrap">Severity</th>
                    <th className="text-left px-5 py-3 text-xs font-semibold text-on-surface-variant uppercase tracking-wide">Payload</th>
                    <th className="text-left px-5 py-3 text-xs font-semibold text-on-surface-variant uppercase tracking-wide">Tags</th>
                  </tr>
                </thead>
                <tbody>
                  {data.map((row, i) => (
                    <tr key={row.id || i} className="border-b border-surface-container last:border-0 hover:bg-surface-container-low transition-colors">
                      <td className="px-5 py-3 text-xs text-on-surface-variant whitespace-nowrap font-mono">
                        {row.timestamp ? new Date(row.timestamp).toLocaleString() : '—'}
                      </td>
                      <td className="px-5 py-3 font-mono text-xs text-on-surface whitespace-nowrap">{row.event_type}</td>
                      <td className="px-5 py-3 text-xs text-on-surface whitespace-nowrap">{row.source}</td>
                      <td className="px-5 py-3 whitespace-nowrap">
                        <span className={`inline-flex px-2 py-0.5 rounded text-xs font-medium ${severityStyle(row.severity)}`}>
                          {row.severity}
                        </span>
                      </td>
                      <td className="px-5 py-3 text-xs text-on-surface-variant max-w-xs">
                        <div className="font-mono truncate">
                          {typeof row.payload === 'object' ? JSON.stringify(row.payload) : String(row.payload || '')}
                        </div>
                      </td>
                      <td className="px-5 py-3 text-xs text-on-surface-variant max-w-[120px] truncate font-mono">
                        {Array.isArray(row.tags) ? row.tags.join(', ') : String(row.tags || '')}
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
