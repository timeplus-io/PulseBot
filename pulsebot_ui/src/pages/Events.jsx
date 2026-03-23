import React, { useEffect } from 'react';
import { useProtonQuery } from '../hooks/useProtonQuery';
import PageHeader from '../components/PageHeader';
import DataTable from '../components/DataTable';
import MetricCard from '../components/MetricCard';
import Card from '../components/Card';

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

const COLUMNS = [
  {
    header: 'Timestamp',
    render: row => (
      <span className="text-xs font-medium text-secondary tabular-nums whitespace-nowrap">
        {row.timestamp ? new Date(row.timestamp).toLocaleString() : '—'}
      </span>
    ),
  },
  {
    header: 'Source',
    render: row => (
      <div className="flex items-center gap-2">
        <div className={`w-6 h-6 rounded flex items-center justify-center text-[10px] font-bold ${sourceColor(row.source)}`}>
          {initials(row.source)}
        </div>
        <span className="font-semibold text-on-surface text-xs">{row.source}</span>
      </div>
    ),
  },
  {
    header: 'Event Type',
    render: row => <span className="text-xs text-on-surface/80 font-mono">{row.event_type}</span>,
  },
  {
    header: 'Status',
    render: row => (
      <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${severityBadge(row.severity)}`}>
        {row.severity}
      </span>
    ),
  },
  {
    header: 'Payload',
    cellClassName: 'max-w-xs',
    render: row => (
      <span className="text-xs text-secondary truncate block font-mono">
        {typeof row.payload === 'object' ? JSON.stringify(row.payload) : String(row.payload || '')}
      </span>
    ),
  },
];

export default function Events() {
  const { data: stats, loading: statsLoading, query: queryStats } = useProtonQuery();
  const { data, loading, error, query } = useProtonQuery();

  const load = () => {
    queryStats(`SELECT count() as total, count_if(severity='error') as errors FROM table(pulsebot.events)`);
    query(`SELECT id, timestamp, event_type, source, severity, payload, tags FROM table(pulsebot.events) ORDER BY timestamp DESC LIMIT 200`);
  };

  useEffect(() => { load(); }, []);

  const st = stats[0] || {};

  return (
    <div className="flex flex-col h-full overflow-hidden">
      <PageHeader onRefresh={load} loading={loading || statsLoading} />

      <div className="flex-1 overflow-y-auto p-8 max-w-7xl mx-auto w-full space-y-8">
        {/* Headline */}
        <div className="flex items-end justify-between">
          <div>
            <p className="text-[11px] font-semibold uppercase tracking-[0.05em] text-secondary mb-1">Monitoring Suite</p>
            <h2 className="text-2xl font-bold text-on-surface">Events Monitor</h2>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <MetricCard
            label="Total Events"
            value={st.total ?? '—'}
            icon={<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-5 h-5 text-tertiary"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.75" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>}
          />
          <MetricCard
            label="Event Sources"
            value={data.length > 0 ? new Set(data.map(r => r.source)).size : '—'}
            tag="sources"
            tagColor="text-primary"
            icon={<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-5 h-5 text-primary"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.75" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" /></svg>}
          />
          <MetricCard
            label="Critical Errors"
            value={st.errors ?? '—'}
            tag={st.errors > 0 ? 'Active' : 'None'}
            tagColor={st.errors > 0 ? 'text-obs-error' : 'text-tertiary'}
            icon={<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-5 h-5 text-obs-error"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.75" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>}
          />
        </div>

        {/* Event Log Table */}
        <Card>
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
          <DataTable
            data={data}
            columns={COLUMNS}
            loading={loading}
            error={error}
            emptyMessage="No events found"
          />
        </Card>
      </div>
    </div>
  );
}
