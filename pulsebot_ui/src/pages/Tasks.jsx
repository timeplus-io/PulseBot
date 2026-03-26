import React, { useEffect, useState } from 'react';
import { useProtonQuery } from '../hooks/useProtonQuery';
import PageHeader from '../components/PageHeader';
import DataTable from '../components/DataTable';

function statusBadge(status) {
  const s = (status || '').toLowerCase();
  if (s === 'active') return 'bg-tertiary/10 text-tertiary';
  if (s === 'paused') return 'bg-[#fff3cd] text-[#856404]';
  if (s === 'deleted') return 'bg-obs-error/10 text-obs-error';
  return 'bg-secondary/10 text-secondary';
}

function statusDot(status) {
  const s = (status || '').toLowerCase();
  if (s === 'active') return 'bg-tertiary';
  if (s === 'paused') return 'bg-[#f6ad55]';
  if (s === 'deleted') return 'bg-obs-error';
  return 'bg-secondary/40';
}

const TRIGGER_COLUMNS = [
  {
    header: 'Triggered At',
    render: row => (
      <span className="text-xs text-secondary whitespace-nowrap">
        {row.triggered_at ? new Date(row.triggered_at).toLocaleString() : '—'}
      </span>
    ),
  },
  {
    header: 'Trigger ID',
    render: row => (
      <span className="text-[10px] font-mono text-secondary truncate block max-w-[140px]" title={row.trigger_id}>
        {row.trigger_id || '—'}
      </span>
    ),
  },
  {
    header: 'Execution ID',
    render: row => (
      <span className="text-[10px] font-mono text-secondary truncate block max-w-[140px]" title={row.execution_id}>
        {row.execution_id || '—'}
      </span>
    ),
  },
  {
    header: 'Prompt',
    render: row => (
      <span className="text-xs text-on-surface truncate block max-w-[280px]" title={row.prompt}>
        {row.prompt || '—'}
      </span>
    ),
  },
];

function TaskDetail({ task, refreshKey }) {
  const { data: triggers, loading: triggersLoading, error: triggersError, query: queryTriggers } = useProtonQuery();
  const { data: taskDef, loading: defLoading, error: defError, query: queryDef } = useProtonQuery();

  useEffect(() => {
    const safeName = task.task_name.replace(/'/g, "\\'");
    queryTriggers(
      `SELECT trigger_id, task_name, prompt, execution_id, triggered_at ` +
      `FROM table(pulsebot.task_triggers) ` +
      `WHERE task_name = '${safeName}' ` +
      `ORDER BY triggered_at DESC LIMIT 50`
    );
    queryDef(`SHOW CREATE TASK \`${task.task_name}\``);
  }, [task.task_id, refreshKey]);

  // Extract DDL: Proton returns a row whose first value is the statement
  const ddl = taskDef.length > 0
    ? (taskDef[0].statement || taskDef[0].create_query || Object.values(taskDef[0])[0] || '')
    : '';

  return (
    <div className="p-8 space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-[11px] font-semibold uppercase tracking-[0.05em] text-secondary mb-1">Task</p>
          <h2 className="text-xl font-bold text-on-surface">{task.task_name}</h2>
        </div>
        <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider shrink-0 ${statusBadge(task.status)}`}>
          {task.status || 'unknown'}
        </span>
      </div>

      {/* Metadata grid */}
      <dl className="grid grid-cols-2 gap-x-6 gap-y-4 bg-surface-container-low rounded-lg p-5">
        <div className="min-w-0 col-span-2">
          <dt className="text-[10px] font-bold uppercase tracking-wider text-secondary mb-0.5">Task ID</dt>
          <dd className="text-xs font-mono text-on-surface break-all">{task.task_id || '—'}</dd>
        </div>
        <div className="min-w-0">
          <dt className="text-[10px] font-bold uppercase tracking-wider text-secondary mb-0.5">Type</dt>
          <dd className="text-xs text-on-surface capitalize">{task.task_type || '—'}</dd>
        </div>
        <div className="min-w-0">
          <dt className="text-[10px] font-bold uppercase tracking-wider text-secondary mb-0.5">Schedule</dt>
          <dd className="text-xs font-mono text-on-surface">{task.schedule || '—'}</dd>
        </div>
        <div className="min-w-0">
          <dt className="text-[10px] font-bold uppercase tracking-wider text-secondary mb-0.5">Created</dt>
          <dd className="text-xs text-on-surface">
            {task.created_at ? new Date(task.created_at).toLocaleString() : '—'}
          </dd>
        </div>
        <div className="min-w-0">
          <dt className="text-[10px] font-bold uppercase tracking-wider text-secondary mb-0.5">Created By</dt>
          <dd className="text-xs text-on-surface">{task.created_by || '—'}</dd>
        </div>
      </dl>

      {/* Prompt */}
      {task.prompt && (
        <div className="bg-surface-container-low rounded-lg p-5">
          <p className="text-[10px] font-bold uppercase tracking-wider text-secondary mb-2">Prompt</p>
          <p className="text-sm text-on-surface leading-relaxed whitespace-pre-wrap">{task.prompt}</p>
        </div>
      )}

      {/* Timeplus Task Definition */}
      <div>
        <p className="text-[11px] font-bold uppercase tracking-widest text-secondary mb-3">Timeplus Task Definition</p>
        <div className="bg-[#1a1c1c] rounded-lg p-4 overflow-x-auto">
          {defLoading ? (
            <p className="text-xs text-[#94a3b8]">Loading...</p>
          ) : defError ? (
            <p className="text-xs text-[#f87171]">{defError}</p>
          ) : ddl ? (
            <pre className="text-xs font-mono text-[#e2e8f0] whitespace-pre-wrap">{ddl}</pre>
          ) : (
            <p className="text-xs text-[#94a3b8]">No definition found</p>
          )}
        </div>
      </div>

      {/* Trigger History */}
      <div>
        <p className="text-[11px] font-bold uppercase tracking-widest text-secondary mb-3">
          Trigger History
        </p>
        <div className="bg-surface-container-lowest rounded-lg border border-outline-variant/10 overflow-hidden">
          <DataTable
            data={triggers}
            columns={TRIGGER_COLUMNS}
            loading={triggersLoading}
            error={triggersError}
            emptyMessage="No triggers recorded for this task"
            pageSize={10}
          />
        </div>
      </div>
    </div>
  );
}

export default function Tasks() {
  const { data: tasks, loading, error, query: queryTasks } = useProtonQuery();
  const [selected, setSelected] = useState(null);
  const [expandedGroups, setExpandedGroups] = useState(new Set(['interval', 'cron']));
  const [refreshKey, setRefreshKey] = useState(0);

  const load = () => {
    queryTasks(
      `SELECT task_id, task_name, task_type, prompt, schedule, status, created_at, created_by ` +
      `FROM (SELECT task_id, task_name, task_type, prompt, schedule, status, created_at, created_by ` +
      `FROM table(pulsebot.tasks) ORDER BY created_at DESC LIMIT 1 BY task_id) ` +
      `WHERE status != 'deleted'`
    );
    setRefreshKey(k => k + 1);
  };

  useEffect(() => { load(); }, []);

  // Group tasks by type; keep interval and cron first
  const grouped = tasks.reduce((acc, task) => {
    const type = task.task_type || 'other';
    if (!acc[type]) acc[type] = [];
    acc[type].push(task);
    return acc;
  }, {});

  const groupOrder = ['interval', 'cron', 'other'];
  const sortedGroups = [...new Set([...groupOrder, ...Object.keys(grouped)])].filter(g => grouped[g]);

  const toggleGroup = (g) => {
    setExpandedGroups(prev => {
      const next = new Set(prev);
      next.has(g) ? next.delete(g) : next.add(g);
      return next;
    });
  };

  const selectedTask = selected ? tasks.find(t => t.task_id === selected) : null;

  return (
    <div className="flex flex-col h-full overflow-hidden">
      <PageHeader onRefresh={load} loading={loading} />

      {error && (
        <div className="px-6 py-2 text-sm text-on-error-container bg-error-container">
          {error}
        </div>
      )}

      <div className="flex-1 flex overflow-hidden">
        {/* Left tree panel */}
        <aside className="w-72 flex-shrink-0 border-r border-outline-variant/10 overflow-y-auto bg-surface">
          <div className="px-4 py-4">
            <p className="text-[11px] font-bold uppercase tracking-widest text-secondary">Scheduled Tasks</p>
          </div>

          {loading ? (
            <p className="px-4 py-8 text-sm text-secondary text-center">Loading...</p>
          ) : tasks.length === 0 ? (
            <p className="px-4 py-8 text-sm text-secondary text-center">No tasks found</p>
          ) : (
            <ul className="pb-4">
              {sortedGroups.map(group => {
                const groupTasks = grouped[group] || [];
                const isExpanded = expandedGroups.has(group);
                return (
                  <li key={group}>
                    {/* Group header */}
                    <div
                      className="flex items-center gap-2 px-3 py-2 cursor-pointer text-secondary hover:bg-surface-container-high transition-colors"
                      onClick={() => toggleGroup(group)}
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        className={`w-3 h-3 shrink-0 transition-transform ${isExpanded ? 'rotate-90' : ''}`}
                      >
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7" />
                      </svg>
                      <span className="text-[10px] font-bold uppercase tracking-widest capitalize">{group}</span>
                      <span className="ml-auto text-[10px] text-secondary/60">{groupTasks.length}</span>
                    </div>

                    {/* Task rows */}
                    {isExpanded && groupTasks.map(task => {
                      const isSelected = selected === task.task_id;
                      return (
                        <div
                          key={task.task_id}
                          onClick={() => setSelected(task.task_id)}
                          className={`flex items-center gap-2 pl-8 pr-3 py-2 cursor-pointer transition-colors ${
                            isSelected
                              ? 'bg-surface-container-high text-primary'
                              : 'text-on-surface hover:bg-surface-container-high'
                          }`}
                        >
                          {/* Clock icon */}
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                            className="w-3.5 h-3.5 shrink-0 text-secondary"
                          >
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.75" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                          <span className="text-xs truncate flex-1">{task.task_name}</span>
                          <span className={`w-1.5 h-1.5 rounded-full shrink-0 ${statusDot(task.status)}`} />
                        </div>
                      );
                    })}
                  </li>
                );
              })}
            </ul>
          )}
        </aside>

        {/* Right detail panel */}
        <main className="flex-1 overflow-y-auto">
          {selectedTask ? (
            <TaskDetail task={selectedTask} refreshKey={refreshKey} />
          ) : (
            <div className="flex flex-col items-center justify-center h-full text-center gap-3 text-secondary">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                className="w-10 h-10 opacity-30"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p className="text-sm">Select a task to view details</p>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
