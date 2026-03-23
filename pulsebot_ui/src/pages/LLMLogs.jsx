import React, { useEffect } from 'react';
import { useProtonQuery } from '../hooks/useProtonQuery';
import PageHeader from '../components/PageHeader';
import DataTable from '../components/DataTable';
import MetricCard from '../components/MetricCard';
import Card from '../components/Card';

function modelColor(model) {
  if (!model) return 'bg-secondary-container text-on-secondary-fixed-variant';
  const m = model.toLowerCase();
  if (m.includes('claude')) return 'bg-primary-fixed text-on-primary-fixed-variant';
  if (m.includes('gpt') || m.includes('openai')) return 'bg-secondary-container text-on-secondary-fixed-variant';
  if (m.includes('gemini')) return 'bg-[#e8f5e9] text-[#2e7d32]';
  if (m.includes('llama') || m.includes('qwen') || m.includes('deepseek')) return 'bg-[#e8f5e9] text-[#2e7d32]';
  return 'bg-secondary-container text-on-secondary-fixed-variant';
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
    header: 'Caller',
    render: row => (
      <span className="text-xs font-mono text-secondary">
        {row.caller || 'main'}
      </span>
    ),
  },
  {
    header: 'Model',
    render: row => (
      <span className={`px-2 py-1 rounded text-[10px] font-bold uppercase ${modelColor(row.model)}`}>
        {row.model}
      </span>
    ),
  },
  {
    header: 'Status',
    render: row => {
      const isSuccess = row.status === 'success';
      return (
        <div>
          <div className={`flex items-center gap-1.5 ${isSuccess ? 'text-tertiary' : 'text-obs-error'}`}>
            <span className={`w-1.5 h-1.5 rounded-full ${isSuccess ? 'bg-tertiary' : 'bg-obs-error'}`} />
            <span className="text-xs font-medium capitalize">{row.status}</span>
          </div>
          {row.error_message && (
            <div className="text-[10px] text-obs-error mt-0.5 max-w-[200px] truncate" title={row.error_message}>
              {row.error_message}
            </div>
          )}
        </div>
      );
    },
  },
  {
    header: 'Tokens',
    render: row => (
      <span className="text-xs font-mono text-secondary whitespace-nowrap">
        {row.input_tokens ?? '?'} / {row.output_tokens ?? '?'}
        {row.total_tokens ? <span className="text-on-surface ml-1">({row.total_tokens})</span> : null}
      </span>
    ),
  },
  {
    header: 'Latency',
    headerClassName: 'text-right',
    cellClassName: 'text-right',
    render: row => (
      <span className="text-sm font-mono text-on-surface whitespace-nowrap">
        {row.latency_ms != null ? `${row.latency_ms}ms` : '—'}
      </span>
    ),
  },
];

export default function LLMLogs() {
  const { data: summaryData, loading: summaryLoading, query: querySummary } = useProtonQuery();
  const { data, loading, error, query } = useProtonQuery();

  const load = () => {
    querySummary(`SELECT round(avg(latency_ms)) as avg_latency, round(count_if(status='success') * 100.0 / count()) as success_rate, sum(total_tokens) as total_tokens FROM table(pulsebot.llm_logs)`);
    query(`SELECT id, timestamp, session_id, caller, model, provider, input_tokens, output_tokens, total_tokens, estimated_cost_usd, latency_ms, time_to_first_token_ms, system_prompt_hash, system_prompt_preview, user_message_preview, assistant_response_preview, full_response_content, messages_count, tools_called, tool_call_count, status, error_message FROM table(pulsebot.llm_logs) ORDER BY timestamp DESC LIMIT 200`);
  };

  useEffect(() => { load(); }, []);

  const s = summaryData[0] || {};

  return (
    <div className="flex flex-col h-full overflow-hidden">
      <PageHeader onRefresh={load} loading={loading || summaryLoading} />

      <main className="flex-1 p-8 overflow-y-auto">
        <div className="max-w-7xl mx-auto space-y-8">
          {/* Header */}
          <div className="flex flex-col gap-1">
            <h2 className="text-2xl font-bold tracking-tight text-on-surface">LLM Execution Logs</h2>
            <p className="text-secondary text-sm">Performance monitoring and trace analysis for active agents.</p>
          </div>

          {/* Summary Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <MetricCard
              label="Avg Latency"
              value={s.avg_latency ? `${s.avg_latency}ms` : '—'}
              subtitle="across all LLM calls"
              icon={<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-5 h-5 text-primary"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.75" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>}
            />
            <MetricCard
              label="Success Rate"
              value={s.success_rate != null ? `${s.success_rate}%` : '—'}
              subtitle="across all agents"
              icon={<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-5 h-5 text-tertiary"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.75" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>}
            />
            <MetricCard
              label="Token Burn"
              value={s.total_tokens ? (s.total_tokens >= 1000000 ? `${(s.total_tokens / 1000000).toFixed(1)}M` : Number(s.total_tokens).toLocaleString()) : '—'}
              subtitle="total tokens consumed"
              icon={<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-5 h-5 text-secondary"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.75" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" /></svg>}
            />
          </div>

          {/* Trace History Table */}
          <Card>
            <div className="px-6 py-4 border-b border-outline-variant/10">
              <h3 className="text-sm font-bold text-on-surface">Trace History</h3>
            </div>
            <DataTable
              data={data}
              columns={COLUMNS}
              loading={loading}
              error={error}
              emptyMessage="No LLM call records found"
            />
          </Card>
        </div>
      </main>
    </div>
  );
}
