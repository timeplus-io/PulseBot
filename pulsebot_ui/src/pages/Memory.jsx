import React, { useEffect } from 'react';
import { useProtonQuery } from '../hooks/useProtonQuery';
import PageHeader from '../components/PageHeader';
import DataTable from '../components/DataTable';
import MetricCard from '../components/MetricCard';
import Card from '../components/Card';

function memoryTypeBadge(type) {
  const map = {
    fact: 'bg-primary-fixed text-on-primary-fixed-variant',
    preference: 'bg-secondary-container text-on-secondary-fixed-variant',
    conversation_summary: 'bg-tertiary/10 text-tertiary',
    skill_learned: 'bg-[#e8f5e9] text-[#2e7d32]',
  };
  return map[type] || 'bg-secondary/10 text-secondary';
}

function categoryBadge(cat) {
  const map = {
    user_info: 'bg-primary-fixed text-on-primary-fixed-variant',
    project: 'bg-secondary-container text-on-secondary-fixed-variant',
    schedule: 'bg-[#fff3cd] text-[#856404]',
    general: 'bg-secondary/10 text-secondary',
  };
  return map[cat] || 'bg-secondary/10 text-secondary';
}

function ImportanceBar({ value }) {
  if (value == null) return <span className="text-secondary text-xs">—</span>;
  const pct = Math.round(value * 100);
  const color = pct >= 70 ? 'bg-tertiary' : pct >= 40 ? 'bg-primary' : 'bg-secondary/40';
  return (
    <div className="flex items-center gap-2 min-w-[80px]">
      <div className="flex-1 h-1.5 rounded-full bg-outline-variant/20 overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${pct}%` }} />
      </div>
      <span className="text-xs font-mono text-secondary tabular-nums w-8 text-right">{pct}%</span>
    </div>
  );
}

const COLUMNS = [
  {
    header: 'Timestamp',
    render: row => (
      <span className="text-xs font-medium text-secondary whitespace-nowrap">
        {row.timestamp ? new Date(row.timestamp).toLocaleString() : '—'}
      </span>
    ),
  },
  {
    header: 'Type',
    render: row => (
      <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${memoryTypeBadge(row.memory_type)}`}>
        {row.memory_type?.replace(/_/g, ' ') || '—'}
      </span>
    ),
  },
  {
    header: 'Category',
    render: row => (
      <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${categoryBadge(row.category)}`}>
        {row.category?.replace(/_/g, ' ') || '—'}
      </span>
    ),
  },
  {
    header: 'Content',
    cellClassName: 'max-w-sm',
    render: row => (
      <span
        className="text-xs text-on-surface block truncate"
        title={row.content}
      >
        {row.content || '—'}
      </span>
    ),
  },
  {
    header: 'Importance',
    render: row => <ImportanceBar value={row.importance} />,
  },
  {
    header: 'State',
    render: row => {
      const deleted = row.is_deleted === true || row.is_deleted === 'true' || row.is_deleted === 1;
      return (
        <span className={`inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${deleted ? 'bg-obs-error/10 text-obs-error' : 'bg-[#87fd6f]/40 text-[#035300]'}`}>
          <span className={`w-1.5 h-1.5 rounded-full ${deleted ? 'bg-obs-error' : 'bg-tertiary'}`} />
          {deleted ? 'Deleted' : 'Active'}
        </span>
      );
    },
  },
];

export default function Memory() {
  const { data: stats, loading: statsLoading, query: queryStats } = useProtonQuery();
  const { data, loading, error, query } = useProtonQuery();

  const load = () => {
    queryStats(`SELECT count() as total, count_if(is_deleted = false) as active, count_if(is_deleted = true) as deleted FROM table(pulsebot.memory)`);
    query(`SELECT id, timestamp, memory_type, category, content, source_session_id, importance, is_deleted FROM table(pulsebot.memory) ORDER BY timestamp DESC LIMIT 500`);
  };

  useEffect(() => { load(); }, []);

  const s = stats[0] || {};
  const uniqueTypes = data.length > 0 ? new Set(data.filter(r => !r.is_deleted).map(r => r.memory_type)).size : '—';

  return (
    <div className="flex flex-col h-full overflow-hidden">
      <PageHeader onRefresh={load} loading={loading || statsLoading} />

      <div className="flex-1 overflow-y-auto p-8 max-w-7xl mx-auto w-full space-y-8">
        {/* Header */}
        <div className="flex flex-col gap-1">
          <span className="text-[11px] font-semibold uppercase tracking-[0.05em] text-secondary">Monitoring</span>
          <h2 className="text-2xl font-bold text-on-surface">Memory</h2>
          <p className="text-secondary text-sm">Agent knowledge base — facts, preferences, and learned context.</p>
        </div>

        {/* Metric Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <MetricCard
            label="Total Memories"
            value={s.total != null ? Number(s.total).toLocaleString() : '—'}
            icon={<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-5 h-5 text-primary"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.75" d="M9 3H5a2 2 0 00-2 2v4m6-6h10a2 2 0 012 2v4M9 3v18m0 0h10a2 2 0 002-2v-4M9 21H5a2 2 0 01-2-2v-4m0 0h18" /></svg>}
          />
          <MetricCard
            label="Active"
            value={s.active != null ? Number(s.active).toLocaleString() : '—'}
            tag={s.total > 0 && s.active != null ? `${Math.round((s.active / s.total) * 100)}%` : undefined}
            tagColor="text-tertiary"
            icon={<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-5 h-5 text-tertiary"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.75" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>}
          />
          <MetricCard
            label="Deleted"
            value={s.deleted != null ? Number(s.deleted).toLocaleString() : '—'}
            tag={s.deleted > 0 ? 'Soft-deleted' : undefined}
            tagColor="text-obs-error"
            icon={<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-5 h-5 text-secondary"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.75" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>}
          />
          <MetricCard
            label="Memory Types"
            value={uniqueTypes}
            tag="distinct"
            icon={<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-5 h-5 text-primary"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.75" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" /></svg>}
          />
        </div>

        {/* Memory Table */}
        <Card>
          <div className="px-6 py-4 border-b border-outline-variant/10">
            <h3 className="text-sm font-bold text-on-surface">Memory Records</h3>
          </div>
          <DataTable
            data={data}
            columns={COLUMNS}
            loading={loading}
            error={error}
            emptyMessage="No memory records found"
          />
        </Card>
      </div>
    </div>
  );
}
