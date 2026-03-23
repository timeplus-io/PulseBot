import React, { useEffect } from 'react';
import { useProtonQuery } from '../hooks/useProtonQuery';
import PageHeader from '../components/PageHeader';
import MetricCard from '../components/MetricCard';

export default function Dashboard() {
  const { data: eventStats, loading: eventsLoading, query: queryEvents } = useProtonQuery();
  const { data: llmStats, loading: llmLoading, query: queryLlm } = useProtonQuery();
  const { data: toolStats, loading: toolLoading, query: queryTools } = useProtonQuery();

  const load = () => {
    queryEvents(`SELECT count() as total, count_if(severity='error') as errors FROM table(pulsebot.events)`);
    queryLlm(`SELECT count() as total, round(avg(latency_ms)) as avg_latency FROM table(pulsebot.llm_logs)`);
    queryTools(`SELECT count() as total, count_if(status='success') as success FROM table(pulsebot.tool_logs)`);
  };

  useEffect(() => { load(); }, []);

  const isLoading = eventsLoading || llmLoading || toolLoading;
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
            icon={<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-5 h-5 text-primary"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.75" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>}
            subtitle={ev.errors > 0 ? `${ev.errors} error events` : 'No errors'}
            subtitleColor={ev.errors > 0 ? 'text-obs-error' : 'text-tertiary'}
          />
          <MetricCard
            label="LLM Calls"
            value={llm.total != null ? Number(llm.total).toLocaleString() : '—'}
            icon={<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-5 h-5 text-primary"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.75" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.346.346a.5.5 0 01-.16.113l-.342.15a.5.5 0 01-.195.04H9.5a.5.5 0 01-.195-.04l-.342-.15a.5.5 0 01-.16-.113l-.346-.346z" /></svg>}
            subtitle={llm.avg_latency ? `Avg latency: ${llm.avg_latency}ms` : undefined}
          />
          <MetricCard
            label="Tool Calls"
            value={tool.total != null ? Number(tool.total).toLocaleString() : '—'}
            icon={<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-5 h-5 text-primary"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.75" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.75" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>}
            subtitle={successRate !== null ? `${successRate}% success rate` : undefined}
            subtitleColor={successRate !== null && successRate < 80 ? 'text-obs-error' : 'text-tertiary'}
          />
          <MetricCard
            label="Active Agents"
            value="—"
            icon={<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-5 h-5 text-primary"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.75" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" /></svg>}
            subtitle="Steady state"
          />
        </section>

      </div>
    </div>
  );
}
