import React, { useEffect } from 'react';
import { useProtonQuery } from '../hooks/useProtonQuery';
import PageHeader from '../components/PageHeader';
import DataTable from '../components/DataTable';
import MetricCard from '../components/MetricCard';
import Card from '../components/Card';

function statusBadge(status) {
  if (status === 'success') return 'bg-[#87fd6f]/40 text-[#035300]';
  if (status === 'error') return 'bg-obs-error text-white';
  return 'bg-error-container text-on-error-container';
}

const COLUMNS = [
  {
    header: 'Timestamp',
    render: row => (
      <span className="text-xs font-mono text-secondary whitespace-nowrap">
        {row.timestamp ? new Date(row.timestamp).toLocaleString() : '—'}
      </span>
    ),
  },
  {
    header: 'Caller',
    render: row => (
      <span className="text-xs font-mono text-secondary">
        {row.caller || 'main'}
      </span>
    ),
  },
  {
    header: 'Tool Name',
    render: row => (
      <code className="text-sm font-semibold text-primary px-2 py-0.5 bg-primary-fixed/30 rounded">
        {row.tool_name}
      </code>
    ),
  },
  {
    header: 'Skill',
    render: row => <span className="text-sm font-medium text-secondary">{row.skill_name || '—'}</span>,
  },
  {
    header: 'Latency',
    render: row => (
      <span className="text-sm font-mono text-on-surface">
        {row.duration_ms != null ? `${row.duration_ms}ms` : '—'}
      </span>
    ),
  },
  {
    header: 'Status',
    render: row => (
      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider ${statusBadge(row.status)}`}>
        {row.status}
      </span>
    ),
  },
];

export default function ToolLogs() {
  const { data: metrics, loading: metricsLoading, query: queryMetrics } = useProtonQuery();
  const { data, loading, error, query } = useProtonQuery();

  const load = () => {
    queryMetrics(`SELECT count() as total, round(avg(duration_ms)) as avg_latency, round(count_if(status='success') * 100.0 / count()) as success_rate FROM table(pulsebot.tool_logs)`);
    query(`SELECT id, timestamp, session_id, caller, llm_request_id, tool_name, skill_name, arguments, status, duration_ms, result_preview, error_message FROM table(pulsebot.tool_logs) ORDER BY timestamp DESC LIMIT 200`);
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
            <MetricCard
              label="Total Tool Calls"
              value={m.total != null ? Number(m.total).toLocaleString() : '—'}
            />
            <MetricCard
              label="Avg Latency"
              value={m.avg_latency ? `${m.avg_latency}ms` : '—'}
            />
            <MetricCard
              label="Success Rate"
              value={m.success_rate != null ? `${m.success_rate}%` : '—'}
              tag={m.success_rate != null ? (m.success_rate >= 95 ? 'Stable' : 'Degraded') : undefined}
              tagColor={m.success_rate >= 95 ? 'text-tertiary' : 'text-obs-error'}
            />
            <MetricCard
              label="Unique Tools"
              value={data.length > 0 ? new Set(data.map(r => r.tool_name)).size : '—'}
              tag="Global"
            />
          </div>

          {/* Tabular Log View */}
          <Card>
            <DataTable
              data={data}
              columns={COLUMNS}
              loading={loading}
              error={error}
              emptyMessage="No tool call records found"
            />
          </Card>
        </div>
      </main>
    </div>
  );
}
