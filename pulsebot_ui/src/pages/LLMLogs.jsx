import React, { useEffect } from 'react';
import { useProtonQuery } from '../hooks/useProtonQuery';
import PageHeader from '../components/PageHeader';

function modelColor(model) {
  if (!model) return 'bg-secondary-container text-on-secondary-fixed-variant';
  const m = model.toLowerCase();
  if (m.includes('claude')) return 'bg-primary-fixed text-on-primary-fixed-variant';
  if (m.includes('gpt') || m.includes('openai')) return 'bg-secondary-container text-on-secondary-fixed-variant';
  if (m.includes('gemini')) return 'bg-[#e8f5e9] text-[#2e7d32]';
  if (m.includes('llama') || m.includes('qwen') || m.includes('deepseek')) return 'bg-[#e8f5e9] text-[#2e7d32]';
  return 'bg-secondary-container text-on-secondary-fixed-variant';
}

export default function LLMLogs() {
  const { data: summaryData, loading: summaryLoading, query: querySummary } = useProtonQuery();
  const { data, loading, error, query } = useProtonQuery();

  const load = () => {
    querySummary(`SELECT round(avg(latency_ms)) as avg_latency, round(count_if(status='success') * 100.0 / count()) as success_rate, sum(total_tokens) as total_tokens FROM table(pulsebot.llm_logs)`);
    query(`SELECT id, timestamp, session_id, model, provider, input_tokens, output_tokens, total_tokens, latency_ms, status, error_message FROM table(pulsebot.llm_logs) ORDER BY timestamp DESC LIMIT 200`);
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

          {/* Bento Summary Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Avg Latency */}
            <div className="bg-surface-container-lowest p-6 rounded-lg shadow-[0_4px_20px_rgba(26,28,28,0.06)] border-l-4 border-primary">
              <div className="flex justify-between items-start mb-4">
                <span className="uppercase tracking-[0.05em] text-[11px] font-semibold text-secondary">Avg Latency</span>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-5 h-5 text-primary">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.75" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="flex items-baseline gap-2">
                <span className="text-3xl font-bold text-on-surface">{s.avg_latency ? `${s.avg_latency}ms` : '—'}</span>
              </div>
              <p className="text-[10px] text-secondary mt-2">across all LLM calls</p>
            </div>
            {/* Success Rate */}
            <div className="bg-surface-container-lowest p-6 rounded-lg shadow-[0_4px_20px_rgba(26,28,28,0.06)] border-l-4 border-tertiary">
              <div className="flex justify-between items-start mb-4">
                <span className="uppercase tracking-[0.05em] text-[11px] font-semibold text-secondary">Success Rate</span>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-5 h-5 text-tertiary">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.75" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="flex items-baseline gap-2">
                <span className="text-3xl font-bold text-on-surface">{s.success_rate != null ? `${s.success_rate}%` : '—'}</span>
              </div>
              <p className="text-[10px] text-secondary mt-2">across all agents</p>
            </div>
            {/* Token Burn */}
            <div className="bg-surface-container-lowest p-6 rounded-lg shadow-[0_4px_20px_rgba(26,28,28,0.06)] border-l-4 border-primary-container">
              <div className="flex justify-between items-start mb-4">
                <span className="uppercase tracking-[0.05em] text-[11px] font-semibold text-secondary">Token Burn</span>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-5 h-5 text-primary-container">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.75" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
                </svg>
              </div>
              <div className="flex items-baseline gap-2">
                <span className="text-3xl font-bold text-on-surface">
                  {s.total_tokens ? (s.total_tokens >= 1000000 ? `${(s.total_tokens / 1000000).toFixed(1)}M` : Number(s.total_tokens).toLocaleString()) : '—'}
                </span>
              </div>
              <p className="text-[10px] text-secondary mt-2">total tokens consumed</p>
            </div>
          </div>

          {/* Trace History Table */}
          <section className="bg-surface-container-lowest rounded-lg shadow-[0_4px_20px_rgba(26,28,28,0.06)] overflow-hidden">
            <div className="px-6 py-4 border-b border-surface-container-low flex justify-between items-center">
              <h3 className="text-sm font-bold text-on-surface">Trace History</h3>
              {data.length > 0 && (
                <span className="text-xs text-secondary">{data.length} records</span>
              )}
            </div>
            {error && (
              <div className="px-6 py-3 text-sm text-on-error-container bg-error-container">Error: {error}</div>
            )}
            <div className="overflow-x-auto">
              {loading ? (
                <div className="px-6 py-12 text-center text-sm text-secondary">Loading...</div>
              ) : data.length === 0 ? (
                <div className="px-6 py-12 text-center text-sm text-secondary">No LLM call records found</div>
              ) : (
                <table className="w-full text-left border-collapse">
                  <thead>
                    <tr className="bg-surface-container-low">
                      <th className="px-6 py-3 uppercase tracking-[0.05em] text-[11px] font-semibold text-secondary">Timestamp</th>
                      <th className="px-6 py-3 uppercase tracking-[0.05em] text-[11px] font-semibold text-secondary">Session</th>
                      <th className="px-6 py-3 uppercase tracking-[0.05em] text-[11px] font-semibold text-secondary">Model</th>
                      <th className="px-6 py-3 uppercase tracking-[0.05em] text-[11px] font-semibold text-secondary">Status</th>
                      <th className="px-6 py-3 uppercase tracking-[0.05em] text-[11px] font-semibold text-secondary">Tokens</th>
                      <th className="px-6 py-3 uppercase tracking-[0.05em] text-[11px] font-semibold text-secondary text-right">Latency</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-surface-container-low">
                    {data.map((row, i) => {
                      const isSuccess = row.status === 'success';
                      return (
                        <tr key={row.id || i} className="hover:bg-surface-container transition-colors group">
                          <td className="px-6 py-4 text-xs font-medium text-secondary whitespace-nowrap">
                            {row.timestamp ? new Date(row.timestamp).toLocaleString() : '—'}
                          </td>
                          <td className="px-6 py-4 text-xs font-mono text-secondary max-w-[120px] truncate">
                            {row.session_id}
                          </td>
                          <td className="px-6 py-4">
                            <span className={`px-2 py-1 rounded text-[10px] font-bold uppercase ${modelColor(row.model)}`}>
                              {row.model}
                            </span>
                          </td>
                          <td className="px-6 py-4">
                            <div className={`flex items-center gap-1.5 ${isSuccess ? 'text-tertiary' : 'text-obs-error'}`}>
                              <span className={`w-1.5 h-1.5 rounded-full ${isSuccess ? 'bg-tertiary' : 'bg-obs-error'}`}></span>
                              <span className="text-xs font-medium capitalize">{row.status}</span>
                            </div>
                            {row.error_message && (
                              <div className="text-[10px] text-obs-error mt-0.5 max-w-[200px] truncate" title={row.error_message}>
                                {row.error_message}
                              </div>
                            )}
                          </td>
                          <td className="px-6 py-4 text-xs font-mono text-secondary whitespace-nowrap">
                            {row.input_tokens ?? '?'} / {row.output_tokens ?? '?'}
                            {row.total_tokens ? <span className="text-on-surface ml-1">({row.total_tokens})</span> : null}
                          </td>
                          <td className="px-6 py-4 text-sm font-mono text-on-surface text-right whitespace-nowrap">
                            {row.latency_ms != null ? `${row.latency_ms}ms` : '—'}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              )}
            </div>
          </section>
        </div>
      </main>
    </div>
  );
}
