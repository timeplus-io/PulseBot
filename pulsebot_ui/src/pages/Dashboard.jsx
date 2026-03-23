import React, { useEffect } from 'react';
import { useProtonQuery } from '../hooks/useProtonQuery';
import PageHeader from '../components/PageHeader';

function MetricCard({ label, value, icon, trend, trendColor = 'text-tertiary' }) {
  return (
    <div className="bg-surface-container-lowest p-6 rounded-lg ambient-shadow border border-outline-variant/10">
      <div className="flex justify-between items-start mb-4">
        <span className="text-secondary text-[10px] font-bold uppercase tracking-widest">{label}</span>
        <span className="text-primary text-xl">{icon}</span>
      </div>
      <div className="text-3xl font-bold text-on-surface">{value ?? '—'}</div>
      {trend && (
        <div className={`mt-2 text-[10px] font-semibold flex items-center gap-1 ${trendColor}`}>
          {trend}
        </div>
      )}
    </div>
  );
}

function statusBadge(status) {
  if (status === 'success') return 'bg-tertiary/10 text-tertiary';
  if (status === 'error') return 'bg-obs-error/10 text-obs-error';
  return 'bg-secondary/10 text-secondary';
}

export default function Dashboard() {
  const { data: eventStats, loading: eventsLoading, query: queryEvents } = useProtonQuery();
  const { data: llmStats, loading: llmLoading, query: queryLlm } = useProtonQuery();
  const { data: toolStats, loading: toolLoading, query: queryTools } = useProtonQuery();
  const { data: recentTools, loading: recentLoading, query: queryRecent } = useProtonQuery();

  const load = () => {
    queryEvents(`SELECT count() as total, countIf(severity='error') as errors FROM table(pulsebot.events)`);
    queryLlm(`SELECT count() as total, round(avg(latency_ms)) as avg_latency FROM table(pulsebot.llm_logs)`);
    queryTools(`SELECT count() as total, countIf(status='success') as success FROM table(pulsebot.tool_logs)`);
    queryRecent(`SELECT timestamp, tool_name, skill_name, duration_ms, status FROM table(pulsebot.tool_logs) ORDER BY timestamp DESC LIMIT 10`);
  };

  useEffect(() => { load(); }, []);

  const isLoading = eventsLoading || llmLoading || toolLoading || recentLoading;
  const ev = eventStats[0] || {};
  const llm = llmStats[0] || {};
  const tool = toolStats[0] || {};
  const successRate = tool.total > 0 ? Math.round((tool.success / tool.total) * 100) : null;

  return (
    <div className="flex flex-col h-full overflow-hidden">
      <PageHeader onRefresh={load} loading={isLoading} />

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-6 lg:p-10 space-y-8">
        {/* Page Header */}
        <section className="flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div>
            <h2 className="text-2xl font-bold tracking-tight text-on-surface">System Observability</h2>
            <p className="text-secondary text-sm">Real-time performance metrics for PulseBot clusters.</p>
          </div>
        </section>

        {/* Metric Cards Bento Grid */}
        <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <MetricCard
            label="Total Events"
            value={ev.total != null ? Number(ev.total).toLocaleString() : '—'}
            icon={
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-5 h-5">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.75" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            }
            trend={ev.errors > 0 ? `${ev.errors} error events` : 'No errors'}
            trendColor={ev.errors > 0 ? 'text-obs-error' : 'text-tertiary'}
          />
          <MetricCard
            label="LLM Calls"
            value={llm.total != null ? Number(llm.total).toLocaleString() : '—'}
            icon={
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-5 h-5">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.75" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.346.346a.5.5 0 01-.16.113l-.342.15a.5.5 0 01-.195.04H9.5a.5.5 0 01-.195-.04l-.342-.15a.5.5 0 01-.16-.113l-.346-.346z" />
              </svg>
            }
            trend={llm.avg_latency ? `Avg latency: ${llm.avg_latency}ms` : undefined}
            trendColor="text-secondary"
          />
          <MetricCard
            label="Tool Calls"
            value={tool.total != null ? Number(tool.total).toLocaleString() : '—'}
            icon={
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-5 h-5">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.75" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.75" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            }
            trend={successRate !== null ? `${successRate}% success rate` : undefined}
            trendColor={successRate !== null && successRate < 80 ? 'text-obs-error' : 'text-tertiary'}
          />
          <MetricCard
            label="Active Agents"
            value="—"
            icon={
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-5 h-5">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.75" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            }
            trend="Steady state"
            trendColor="text-secondary"
          />
        </section>

        {/* Recent Tool Executions Table */}
        <section className="bg-surface-container-lowest rounded-lg ambient-shadow border border-outline-variant/10 overflow-hidden">
          <div className="px-6 py-4 flex items-center justify-between border-b border-outline-variant/10">
            <h3 className="text-sm font-bold uppercase tracking-widest text-secondary">Recent Tool Executions</h3>
          </div>
          <div className="overflow-x-auto">
            {recentLoading ? (
              <div className="px-6 py-10 text-center text-sm text-secondary">Loading...</div>
            ) : recentTools.length === 0 ? (
              <div className="px-6 py-10 text-center text-sm text-secondary">No tool executions found</div>
            ) : (
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-surface-container-low/50">
                    <th className="px-6 py-3 text-[10px] font-bold uppercase tracking-widest text-secondary">Timestamp</th>
                    <th className="px-6 py-3 text-[10px] font-bold uppercase tracking-widest text-secondary">Tool Name</th>
                    <th className="px-6 py-3 text-[10px] font-bold uppercase tracking-widest text-secondary">Skill</th>
                    <th className="px-6 py-3 text-[10px] font-bold uppercase tracking-widest text-secondary">Latency</th>
                    <th className="px-6 py-3 text-[10px] font-bold uppercase tracking-widest text-secondary text-right">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-outline-variant/10">
                  {recentTools.map((row, i) => (
                    <tr key={i} className="hover:bg-surface-container-low transition-colors">
                      <td className="px-6 py-4 text-xs font-medium text-secondary tabular-nums whitespace-nowrap">
                        {row.timestamp ? new Date(row.timestamp).toLocaleString() : '—'}
                      </td>
                      <td className="px-6 py-4 text-xs font-bold text-on-surface">
                        <div className="flex items-center gap-2">
                          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-4 h-4 text-primary shrink-0">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.75" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.75" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                          </svg>
                          {row.tool_name}
                        </div>
                      </td>
                      <td className="px-6 py-4 text-xs font-medium text-secondary">{row.skill_name || '—'}</td>
                      <td className="px-6 py-4 text-xs font-medium text-secondary">
                        {row.duration_ms != null ? `${row.duration_ms}ms` : '—'}
                      </td>
                      <td className="px-6 py-4 text-right">
                        <span className={`inline-flex px-2 py-0.5 rounded text-[10px] font-bold uppercase ${statusBadge(row.status)}`}>
                          {row.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </section>
      </div>
    </div>
  );
}
