import React, { useEffect } from 'react';
import { useProtonQuery } from '../hooks/useProtonQuery';
import PageHeader from '../components/PageHeader';
import MetricCard from '../components/MetricCard';

function hourKey(d) {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}-${d.getHours()}`;
}

// Expand sparse query results into a full 24-slot array (one per hour).
// Hours with no data get value=0 so the chart always shows 24 bars.
function fill24Hours(queryData, valueKey) {
  const lookup = {};
  for (const row of queryData) {
    const d = new Date(row.hour);
    if (!isNaN(d.getTime())) {
      lookup[hourKey(d)] = Number(row[valueKey]) || 0;
    }
  }
  const now = new Date();
  now.setMinutes(0, 0, 0);
  const slots = [];
  for (let i = 23; i >= 0; i--) {
    const d = new Date(now.getTime() - i * 3600 * 1000);
    slots.push({
      label: `${String(d.getHours()).padStart(2, '0')}:00`,
      value: lookup[hourKey(d)] || 0,
    });
  }
  return slots;
}

function formatCount(v) {
  const n = Number(v) || 0;
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(1)}K`;
  return String(n);
}

// data: [{label: 'HH:00', value: number}] — always 24 slots, pre-filled by fill24Hours()
function ColumnChart({ data, loading, color = 'primary' }) {
  if (loading) {
    return (
      <div className="h-28 flex items-center justify-center">
        <p className="text-xs text-secondary">Loading…</p>
      </div>
    );
  }

  const values = (data || []).map(d => d.value);
  const max = Math.max(...values, 1);
  const barColor = color === 'primary' ? 'bg-primary/70 group-hover/col:bg-primary' : 'bg-tertiary/70 group-hover/col:bg-tertiary';
  // x-axis labels every 6 hours: indices 0, 6, 12, 18, 23
  const labelIdxs = new Set([0, 6, 12, 18, 23]);

  return (
    <div>
      <div className="h-28 flex items-end gap-0.5">
        {(data || []).map((d, i) => {
          const pct = (d.value / max) * 100;
          return (
            <div
              key={i}
              className="group/col flex-1 flex flex-col justify-end relative cursor-default rounded-[2px] hover:bg-surface-container transition-colors"
              style={{ height: '100%' }}
            >
              {/* Tooltip — positioned above the chart column */}
              <div
                className="absolute left-1/2 -translate-x-1/2 hidden group-hover/col:flex flex-col items-center z-20 pointer-events-none"
                style={{ bottom: 'calc(100% + 6px)' }}
              >
                <div className="bg-[#1a1c1c] text-[#f1f0f0] rounded-[3px] px-2 py-1 whitespace-nowrap text-center shadow-md">
                  <div className="text-[8px] text-[#94a3b8] leading-tight">{d.label}</div>
                  <div className="text-[10px] font-bold leading-tight">{formatCount(d.value)}</div>
                </div>
                {/* caret */}
                <div className="w-0 h-0"
                  style={{
                    borderLeft: '4px solid transparent',
                    borderRight: '4px solid transparent',
                    borderTop: '4px solid #1a1c1c',
                  }}
                />
              </div>

              {/* Bar */}
              <div
                className={`w-full rounded-t-[2px] transition-colors ${pct > 0 ? barColor : ''}`}
                style={{ height: `${pct}%` }}
              />
            </div>
          );
        })}
      </div>
      <div className="flex mt-1.5 relative h-4">
        {(data || []).map((d, i) => {
          if (!labelIdxs.has(i)) return null;
          const pct = (i / 23) * 100;
          return (
            <span
              key={i}
              className="absolute text-[9px] font-bold text-secondary tracking-wider transform -translate-x-1/2"
              style={{ left: `${pct}%` }}
            >
              {d.label}
            </span>
          );
        })}
      </div>
    </div>
  );
}

function ModelBarChart({ data, loading }) {
  if (loading) {
    return (
      <div className="h-28 flex items-center justify-center">
        <p className="text-xs text-secondary">Loading…</p>
      </div>
    );
  }
  if (!data || data.length === 0) {
    return (
      <div className="py-8 flex items-center justify-center">
        <p className="text-xs text-secondary">No data</p>
      </div>
    );
  }

  const maxCalls = Math.max(...data.map(d => Number(d.calls) || 0), 1);

  return (
    <div className="space-y-3">
      {data.map((row, i) => {
        const calls = Number(row.calls) || 0;
        const pct = (calls / maxCalls) * 100;
        return (
          <div key={i} className="flex items-center gap-3">
            <span
              className="text-[10px] font-mono text-secondary truncate shrink-0"
              style={{ width: '11rem' }}
              title={row.model || 'unknown'}
            >
              {row.model || 'unknown'}
            </span>
            <div className="flex-1 h-3.5 bg-surface-container rounded-[2px] overflow-hidden">
              <div
                className="h-full bg-primary/75 hover:bg-primary transition-colors rounded-[2px]"
                style={{ width: `${pct}%` }}
                title={`${calls.toLocaleString()} calls`}
              />
            </div>
            <span className="text-[10px] font-bold text-secondary w-10 text-right shrink-0">
              {formatCount(calls)}
            </span>
          </div>
        );
      })}
    </div>
  );
}

export default function Dashboard() {
  const { data: eventStats, loading: eventsLoading, query: queryEvents } = useProtonQuery();
  const { data: llmStats, loading: llmLoading, query: queryLlm } = useProtonQuery();
  const { data: toolStats, loading: toolLoading, query: queryTools } = useProtonQuery();
  const { data: agentStats, loading: agentsLoading, query: queryAgents } = useProtonQuery();
  const { data: llmOverTime, loading: llmTimeLoading, query: queryLlmTime } = useProtonQuery();
  const { data: tokensOverTime, loading: tokensTimeLoading, query: queryTokensTime } = useProtonQuery();
  const { data: toolsOverTime, loading: toolsTimeLoading, query: queryToolsTime } = useProtonQuery();
  const { data: modelBreakdown, loading: modelsLoading, query: queryModels } = useProtonQuery();

  const load = () => {
    queryEvents(`SELECT count() as total, count_if(severity='error') as errors FROM table(pulsebot.events)`);
    queryLlm(`SELECT count() as total, round(avg(latency_ms)) as avg_latency FROM table(pulsebot.llm_logs)`);
    queryTools(`SELECT count() as total, count_if(status='success') as success FROM table(pulsebot.tool_logs)`);
    queryAgents(`SELECT count() as active FROM (SELECT agent_id, status FROM table(pulsebot.kanban_agents) ORDER BY timestamp DESC LIMIT 1 BY agent_id) WHERE status = 'running'`);
    queryLlmTime(`SELECT to_start_of_hour(timestamp) as hour, count() as calls FROM table(pulsebot.llm_logs) WHERE timestamp >= now() - interval 24 hour GROUP BY hour ORDER BY hour`);
    queryTokensTime(`SELECT to_start_of_hour(timestamp) as hour, sum(total_tokens) as tokens FROM table(pulsebot.llm_logs) WHERE timestamp >= now() - interval 24 hour GROUP BY hour ORDER BY hour`);
    queryToolsTime(`SELECT to_start_of_hour(timestamp) as hour, count() as calls FROM table(pulsebot.tool_logs) WHERE timestamp >= now() - interval 24 hour GROUP BY hour ORDER BY hour`);
    queryModels(`SELECT model, count() as calls FROM table(pulsebot.llm_logs) GROUP BY model ORDER BY calls DESC LIMIT 8`);
  };

  useEffect(() => { load(); }, []);

  const isLoading = eventsLoading || llmLoading || toolLoading || agentsLoading;
  const ev = eventStats[0] || {};
  const llm = llmStats[0] || {};
  const tool = toolStats[0] || {};
  const agents = agentStats[0] || {};
  const successRate = tool.total > 0 ? Math.round((tool.success / tool.total) * 100) : null;

  const cardStyle = { boxShadow: '0 4px 20px rgba(26,28,28,0.06)' };

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
            value={agents.active != null ? Number(agents.active).toLocaleString() : '—'}
            icon={<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-5 h-5 text-primary"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.75" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" /></svg>}
            subtitle={agents.active > 0 ? 'Agents running' : 'No active agents'}
            subtitleColor={agents.active > 0 ? 'text-tertiary' : 'text-secondary'}
          />
        </section>

        {/* Time Series Charts */}
        <section className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* LLM Calls Over Time */}
          <div className="bg-surface-container-lowest rounded-lg border border-outline-variant/10 p-5" style={cardStyle}>
            <div className="flex items-center gap-2 mb-4">
              <span className="w-2 h-2 rounded-full bg-primary shrink-0" />
              <p className="text-[10px] font-bold uppercase tracking-widest text-secondary">LLM Calls · Last 24h</p>
            </div>
            <ColumnChart
              data={fill24Hours(llmOverTime, 'calls')}
              loading={llmTimeLoading}
            />
          </div>

          {/* LLM Tokens Over Time */}
          <div className="bg-surface-container-lowest rounded-lg border border-outline-variant/10 p-5" style={cardStyle}>
            <div className="flex items-center gap-2 mb-4">
              <span className="w-2 h-2 rounded-full bg-primary shrink-0" />
              <p className="text-[10px] font-bold uppercase tracking-widest text-secondary">Tokens Consumed · Last 24h</p>
            </div>
            <ColumnChart
              data={fill24Hours(tokensOverTime, 'tokens')}
              loading={tokensTimeLoading}
            />
          </div>

          {/* Tool Calls Over Time */}
          <div className="bg-surface-container-lowest rounded-lg border border-outline-variant/10 p-5" style={cardStyle}>
            <div className="flex items-center gap-2 mb-4">
              <span className="w-2 h-2 rounded-full bg-tertiary shrink-0" />
              <p className="text-[10px] font-bold uppercase tracking-widest text-secondary">Tool Calls · Last 24h</p>
            </div>
            <ColumnChart
              data={fill24Hours(toolsOverTime, 'calls')}
              loading={toolsTimeLoading}
              color="tertiary"
            />
          </div>
        </section>

        {/* Model Breakdown */}
        <section className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <div className="bg-surface-container-lowest rounded-lg border border-outline-variant/10 p-5" style={cardStyle}>
            <p className="text-[10px] font-bold uppercase tracking-widest text-secondary mb-5">LLM Calls by Model</p>
            <ModelBarChart data={modelBreakdown} loading={modelsLoading} />
          </div>
        </section>

      </div>
    </div>
  );
}
