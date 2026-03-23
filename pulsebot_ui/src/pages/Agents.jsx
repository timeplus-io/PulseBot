import React, { useEffect, useState } from 'react';
import { useProtonQuery } from '../hooks/useProtonQuery';
import PageHeader from '../components/PageHeader';
import DataTable from '../components/DataTable';

function statusBadge(status, type = 'agent') {
  const s = (status || '').toLowerCase();
  if (type === 'project') {
    if (s === 'active') return 'bg-tertiary/10 text-tertiary';
    if (s === 'completed') return 'bg-secondary/10 text-secondary';
    if (s === 'paused') return 'bg-[#fff3cd] text-[#856404]';
    if (s === 'failed') return 'bg-obs-error/10 text-obs-error';
  } else {
    if (s === 'active' || s === 'working' || s === 'done') return 'bg-tertiary/10 text-tertiary';
    if (s === 'idle' || s === 'inactive') return 'bg-secondary/10 text-secondary';
    if (s === 'failed') return 'bg-obs-error/10 text-obs-error';
  }
  return 'bg-secondary/10 text-secondary';
}

function DetailField({ label, value }) {
  if (value == null || value === '') return null;
  const display = Array.isArray(value)
    ? value.join(', ') || '—'
    : String(value);
  return (
    <div className="min-w-0">
      <dt className="text-[10px] font-bold uppercase tracking-wider text-secondary mb-0.5">{label}</dt>
      <dd className="text-xs text-on-surface break-words">{display || '—'}</dd>
    </div>
  );
}

// ── Topology diagram ──────────────────────────────────────────────────────────

const NODE_W = 152;
const NODE_H = 56;
const COL_GAP = 180;
const ROW_GAP = 110;
const PAD = 48;

function nodeColor(status, isManager) {
  if (isManager) return { fill: '#fdf2f8', stroke: '#ad1a6c', text: '#ad1a6c' };
  const s = (status || '').toLowerCase();
  if (s === 'active' || s === 'working') return { fill: '#f0fdf4', stroke: '#4ade80', text: '#166534' };
  if (s === 'done') return { fill: '#eff6ff', stroke: '#60a5fa', text: '#1e40af' };
  if (s === 'failed') return { fill: '#fef2f2', stroke: '#f87171', text: '#991b1b' };
  return { fill: '#f8fafc', stroke: '#cbd5e1', text: '#475569' };
}

function buildLayout(agents) {
  const allIds = new Set(agents.map(a => a.agent_id));

  // Identify manager agent (agent_id starts with 'manager_')
  const managerId = agents.find(a => a.agent_id.startsWith('manager_'))?.agent_id;
  const workers = agents.filter(a => a.agent_id !== managerId);
  const workerIds = new Set(workers.map(w => w.agent_id));

  // Build worker→worker / worker→manager edges from target_agents
  const edges = [];
  agents.forEach(a => {
    const targets = Array.isArray(a.target_agents) ? a.target_agents : [];
    targets.forEach(t => { if (allIds.has(t)) edges.push({ from: a.agent_id, to: t, dispatch: false }); });
  });

  // Dispatch edges: manager → root workers (workers with no incoming from other workers)
  if (managerId) {
    const hasIncomingFromWorker = new Set(
      edges.filter(e => workerIds.has(e.to) && workerIds.has(e.from)).map(e => e.to)
    );
    workers
      .filter(w => !hasIncomingFromWorker.has(w.agent_id))
      .forEach(w => edges.push({ from: managerId, to: w.agent_id, dispatch: true }));
  }

  // Assign depth rows: manager = 0, workers via BFS on target_agents
  const depth = {};
  if (managerId) depth[managerId] = 0;

  const workerInDeg = {};
  workers.forEach(w => { workerInDeg[w.agent_id] = 0; });
  edges.forEach(e => {
    if (workerIds.has(e.to) && workerIds.has(e.from)) {
      workerInDeg[e.to] = (workerInDeg[e.to] || 0) + 1;
    }
  });

  const roots = workers.filter(w => !workerInDeg[w.agent_id]);
  roots.forEach(w => { depth[w.agent_id] = 1; });

  const bfs = roots.map(w => w.agent_id);
  while (bfs.length) {
    const cur = bfs.shift();
    const agent = agents.find(a => a.agent_id === cur);
    const targets = Array.isArray(agent?.target_agents) ? agent.target_agents : [];
    targets.forEach(t => {
      if (workerIds.has(t)) {
        depth[t] = Math.max(depth[t] ?? 1, (depth[cur] ?? 1) + 1);
        bfs.push(t);
      }
    });
  }
  workers.forEach(w => { if (depth[w.agent_id] == null) depth[w.agent_id] = 1; });

  // Group by depth row, assign columns (centered)
  const rowGroups = {};
  agents.forEach(a => {
    const r = depth[a.agent_id] ?? 0;
    if (!rowGroups[r]) rowGroups[r] = [];
    rowGroups[r].push(a.agent_id);
  });

  const maxCols = Math.max(...Object.values(rowGroups).map(g => g.length));
  const maxDepth = Math.max(...Object.values(depth));
  const svgW = PAD * 2 + Math.max(1, maxCols) * COL_GAP;
  const svgH = PAD * 2 + (maxDepth + 1) * ROW_GAP;
  const centerX = svgW / 2;

  const pos = {};
  Object.entries(rowGroups).forEach(([r, ids]) => {
    ids.forEach((id, i) => {
      pos[id] = {
        x: centerX + (i - (ids.length - 1) / 2) * COL_GAP - NODE_W / 2,
        y: PAD + Number(r) * ROW_GAP,
      };
    });
  });

  return { pos, edges, svgW, svgH, managerId };
}

function TopologyDiagram({ agents, onSelectAgent }) {
  if (agents.length === 0) {
    return <p className="text-xs text-secondary p-6">No agents in this project.</p>;
  }

  const { pos, edges, svgW, svgH, managerId } = buildLayout(agents);

  return (
    <div className="overflow-auto">
      <svg width={svgW} height={svgH} xmlns="http://www.w3.org/2000/svg">
        <defs>
          <marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">
            <path d="M0,0 L0,6 L8,3 z" fill="#94a3b8" />
          </marker>
          <marker id="arrow-dispatch" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">
            <path d="M0,0 L0,6 L8,3 z" fill="#ad1a6c" />
          </marker>
        </defs>

        {/* Edges */}
        {edges.map((e, i) => {
          const from = pos[e.from];
          const to = pos[e.to];
          if (!from || !to) return null;
          // Top-to-bottom: exit bottom-center of source, enter top-center of target
          const x1 = from.x + NODE_W / 2;
          const y1 = from.y + NODE_H;
          const x2 = to.x + NODE_W / 2;
          const y2 = to.y;
          const cy = (y1 + y2) / 2;
          return (
            <path
              key={i}
              d={`M${x1},${y1} C${x1},${cy} ${x2},${cy} ${x2},${y2}`}
              fill="none"
              stroke={e.dispatch ? '#ad1a6c' : '#94a3b8'}
              strokeWidth="1.5"
              strokeDasharray={e.dispatch ? '5,3' : undefined}
              markerEnd={e.dispatch ? 'url(#arrow-dispatch)' : 'url(#arrow)'}
            />
          );
        })}

        {/* Nodes */}
        {agents.map(a => {
          const p = pos[a.agent_id];
          if (!p) return null;
          const isManager = a.agent_id === managerId;
          const { fill, stroke, text } = nodeColor(a.status, isManager);
          const label = a.name || a.role || a.agent_id.slice(0, 10);
          const sublabel = a.role && a.name ? a.role : (a.status || '');
          return (
            <g
              key={a.agent_id}
              transform={`translate(${p.x},${p.y})`}
              style={{ cursor: 'pointer' }}
              onClick={() => onSelectAgent(a.agent_id)}
            >
              <rect width={NODE_W} height={NODE_H} rx="8" fill={fill} stroke={stroke} strokeWidth={isManager ? 2 : 1.5} />
              <text
                x={NODE_W / 2}
                y={NODE_H / 2 - 6}
                textAnchor="middle"
                fontSize="11"
                fontWeight="700"
                fill={text}
                fontFamily="inherit"
              >
                {label.length > 18 ? label.slice(0, 16) + '…' : label}
              </text>
              <text
                x={NODE_W / 2}
                y={NODE_H / 2 + 10}
                textAnchor="middle"
                fontSize="9"
                fill={isManager ? '#ad1a6c' : '#94a3b8'}
                fontFamily="inherit"
              >
                {sublabel.length > 22 ? sublabel.slice(0, 20) + '…' : sublabel}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}

// ── Project detail ─────────────────────────────────────────────────────────────

function ProjectDetail({ project, agents, onSelectAgent }) {
  return (
    <div className="p-8 space-y-6">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-[11px] font-semibold uppercase tracking-[0.05em] text-secondary mb-1">Project</p>
          <h2 className="text-xl font-bold text-on-surface">{project.name || project.project_id}</h2>
          {project.description && <p className="text-sm text-secondary mt-1">{project.description}</p>}
        </div>
        <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider shrink-0 ${statusBadge(project.status, 'project')}`}>
          {project.status || 'unknown'}
        </span>
      </div>

      <dl className="grid grid-cols-2 gap-x-6 gap-y-4 bg-surface-container-low rounded-lg p-5">
        <DetailField label="Project ID" value={project.project_id} />
        <DetailField label="Created By" value={project.created_by} />
        <DetailField label="Session ID" value={project.session_id} />
        <DetailField label="Last Updated" value={project.timestamp ? new Date(project.timestamp).toLocaleString() : null} />
      </dl>

      <div>
        <h3 className="text-[11px] font-bold uppercase tracking-widest text-secondary mb-4">
          Agent Topology ({agents.length})
        </h3>
        <div className="bg-surface-container-low rounded-lg border border-outline-variant/10 overflow-hidden">
          <TopologyDiagram agents={agents} onSelectAgent={onSelectAgent} />
        </div>
        <p className="text-[10px] text-secondary mt-2">Click a node to view agent details.</p>
      </div>
    </div>
  );
}

const KANBAN_COLUMNS = [
  {
    header: 'Time',
    render: row => (
      <span className="text-xs font-medium text-secondary whitespace-nowrap">
        {row.timestamp ? new Date(row.timestamp).toLocaleString() : '—'}
      </span>
    ),
  },
  {
    header: 'Dir',
    render: (row, agentId) => {
      const sent = row.sender_id === agentId;
      return (
        <span className={`px-1.5 py-0.5 rounded text-[9px] font-bold uppercase tracking-wider ${sent ? 'bg-primary-fixed text-on-primary-fixed-variant' : 'bg-secondary/10 text-secondary'}`}>
          {sent ? 'Out' : 'In'}
        </span>
      );
    },
  },
  {
    header: 'Type',
    render: row => (
      <span className="text-[10px] font-mono text-on-surface">{row.msg_type || '—'}</span>
    ),
  },
  {
    header: 'From',
    cellClassName: 'max-w-[120px]',
    render: row => (
      <span className="text-xs font-mono text-secondary truncate block" title={row.sender_id}>
        {row.sender_id || '—'}
      </span>
    ),
  },
  {
    header: 'To',
    cellClassName: 'max-w-[120px]',
    render: row => (
      <span className="text-xs font-mono text-secondary truncate block" title={row.target_id}>
        {row.target_id || '—'}
      </span>
    ),
  },
  {
    header: 'Content',
    cellClassName: 'max-w-xs',
    render: row => (
      <span className="text-xs text-on-surface truncate block" title={row.content}>
        {row.content || '—'}
      </span>
    ),
  },
];

function AgentDetail({ agent }) {
  const skills = Array.isArray(agent.skills)
    ? agent.skills
    : String(agent.skills || '').split(',').map(s => s.trim()).filter(Boolean);

  const { data: kanban, loading: kanbanLoading, error: kanbanError, query: queryKanban } = useProtonQuery();

  useEffect(() => {
    queryKanban(
      `SELECT msg_id, timestamp, project_id, sender_id, target_id, msg_type, content, priority, metadata ` +
      `FROM table(pulsebot.kanban) ` +
      `WHERE sender_id = '${agent.agent_id}' OR target_id = '${agent.agent_id}' ` +
      `ORDER BY timestamp DESC LIMIT 200`
    );
  }, [agent.agent_id]);

  // Bind agent_id into column renderers that need it
  const columns = KANBAN_COLUMNS.map(col => ({
    ...col,
    render: row => col.render(row, agent.agent_id),
  }));

  return (
    <div className="p-8 space-y-6">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-[11px] font-semibold uppercase tracking-[0.05em] text-secondary mb-1">Agent</p>
          <h2 className="text-xl font-bold text-on-surface">{agent.name || agent.role || agent.agent_id}</h2>
          {agent.role && agent.name && <p className="text-sm text-secondary mt-1">{agent.role}</p>}
        </div>
        <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider shrink-0 ${statusBadge(agent.status)}`}>
          {agent.status || 'unknown'}
        </span>
      </div>

      {agent.task_description && (
        <div className="bg-surface-container-low rounded-lg p-5">
          <p className="text-[10px] font-bold uppercase tracking-wider text-secondary mb-2">Task</p>
          <p className="text-sm text-on-surface leading-relaxed">{agent.task_description}</p>
        </div>
      )}

      <dl className="grid grid-cols-2 gap-x-6 gap-y-4 bg-surface-container-low rounded-lg p-5">
        <DetailField label="Agent ID" value={agent.agent_id} />
        <DetailField label="Project ID" value={agent.project_id} />
        <DetailField label="Last Updated" value={agent.timestamp ? new Date(agent.timestamp).toLocaleString() : null} />
      </dl>

      {skills.length > 0 && (
        <div>
          <p className="text-[10px] font-bold uppercase tracking-wider text-secondary mb-2">Skills</p>
          <div className="flex flex-wrap gap-1.5">
            {skills.map((s, i) => (
              <span key={i} className="px-2 py-0.5 bg-secondary-container text-on-secondary-fixed-variant rounded text-[10px] font-bold">
                {s}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Kanban message log */}
      <div>
        <p className="text-[11px] font-bold uppercase tracking-widest text-secondary mb-3">Kanban Messages</p>
        <div className="bg-surface-container-lowest rounded-lg border border-outline-variant/10 overflow-hidden">
          <DataTable
            data={kanban}
            columns={columns}
            loading={kanbanLoading}
            error={kanbanError}
            emptyMessage="No kanban messages for this agent"
            pageSize={10}
          />
        </div>
      </div>
    </div>
  );
}

export default function Agents() {
  const { data: projects, loading: projLoading, error: projError, query: queryProjects } = useProtonQuery();
  const { data: agents, loading: agentsLoading, error: agentsError, query: queryAgents } = useProtonQuery();
  const [expandedProjects, setExpandedProjects] = useState(new Set());
  const [selected, setSelected] = useState(null); // { type: 'project'|'agent', id: string }

  const load = () => {
    queryProjects(`SELECT project_id, name, description, status, created_by, session_id, timestamp FROM table(pulsebot.kanban_projects) ORDER BY timestamp DESC LIMIT 1 BY project_id LIMIT 50`);
    queryAgents(`SELECT agent_id, project_id, name, role, task_description, status, skills, target_agents, timestamp FROM table(pulsebot.kanban_agents) ORDER BY timestamp DESC LIMIT 1 BY agent_id, project_id LIMIT 200`);
  };

  useEffect(() => { load(); }, []);

  const isLoading = projLoading || agentsLoading;

  const agentsByProject = agents.reduce((acc, agent) => {
    const pid = agent.project_id || 'unassigned';
    if (!acc[pid]) acc[pid] = [];
    acc[pid].push(agent);
    return acc;
  }, {});

  const toggleProject = (pid) => {
    setExpandedProjects(prev => {
      const next = new Set(prev);
      next.has(pid) ? next.delete(pid) : next.add(pid);
      return next;
    });
  };

  const selectedProject = selected?.type === 'project'
    ? projects.find(p => p.project_id === selected.id)
    : null;
  const selectedAgent = selected?.type === 'agent'
    ? agents.find(a => a.agent_id === selected.id)
    : null;

  return (
    <div className="flex flex-col h-full overflow-hidden">
      <PageHeader onRefresh={load} loading={isLoading} />

      {(projError || agentsError) && (
        <div className="px-6 py-2 text-sm text-on-error-container bg-error-container">
          {projError || agentsError}
        </div>
      )}

      <div className="flex-1 flex overflow-hidden">
        {/* Left tree panel */}
        <aside className="w-72 flex-shrink-0 border-r border-outline-variant/10 overflow-y-auto bg-surface">
          <div className="px-4 py-4">
            <p className="text-[11px] font-bold uppercase tracking-widest text-secondary">Projects & Agents</p>
          </div>

          {isLoading ? (
            <p className="px-4 py-8 text-sm text-secondary text-center">Loading...</p>
          ) : projects.length === 0 && agents.length === 0 ? (
            <p className="px-4 py-8 text-sm text-secondary text-center">No projects found</p>
          ) : (
            <ul className="pb-4">
              {projects.map(project => {
                const projectAgents = agentsByProject[project.project_id] || [];
                const isExpanded = expandedProjects.has(project.project_id);
                const isSelected = selected?.type === 'project' && selected.id === project.project_id;
                return (
                  <li key={project.project_id}>
                    {/* Project row */}
                    <div
                      className={`flex items-center gap-1.5 px-3 py-2 cursor-pointer transition-colors ${isSelected ? 'bg-surface-container-high text-primary' : 'text-on-surface hover:bg-surface-container-high'}`}
                      onClick={() => {
                        setSelected({ type: 'project', id: project.project_id });
                        if (projectAgents.length > 0 && !isExpanded) toggleProject(project.project_id);
                      }}
                    >
                      {/* Chevron */}
                      <button
                        onClick={e => { e.stopPropagation(); toggleProject(project.project_id); }}
                        className="w-4 h-4 flex items-center justify-center shrink-0 text-secondary"
                      >
                        {projectAgents.length > 0 ? (
                          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className={`w-3 h-3 transition-transform ${isExpanded ? 'rotate-90' : ''}`}>
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7" />
                          </svg>
                        ) : <span className="w-3" />}
                      </button>
                      {/* Project icon */}
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-4 h-4 shrink-0 text-primary">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.75" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                      </svg>
                      <span className="text-xs font-semibold truncate flex-1">{project.name || project.project_id}</span>
                      <span className={`px-1.5 py-0.5 rounded text-[8px] font-bold uppercase shrink-0 ${statusBadge(project.status, 'project')}`}>
                        {project.status || '?'}
                      </span>
                    </div>

                    {/* Agent children */}
                    {isExpanded && projectAgents.map(agent => {
                      const isAgentSelected = selected?.type === 'agent' && selected.id === agent.agent_id;
                      return (
                        <div
                          key={agent.agent_id}
                          onClick={() => setSelected({ type: 'agent', id: agent.agent_id })}
                          className={`flex items-center gap-1.5 pl-9 pr-3 py-1.5 cursor-pointer transition-colors ${isAgentSelected ? 'bg-surface-container-high text-primary' : 'text-secondary hover:bg-surface-container-high hover:text-on-surface'}`}
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-3.5 h-3.5 shrink-0">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.75" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                          </svg>
                          <span className="text-xs truncate flex-1">{agent.name || agent.role || agent.agent_id}</span>
                          <span className={`w-1.5 h-1.5 rounded-full shrink-0 ${(agent.status || '').toLowerCase() === 'failed' ? 'bg-obs-error' : (agent.status || '').toLowerCase() === 'active' || (agent.status || '').toLowerCase() === 'working' ? 'bg-tertiary' : 'bg-secondary/40'}`} />
                        </div>
                      );
                    })}
                  </li>
                );
              })}

              {/* Unassigned agents */}
              {(agentsByProject['unassigned'] || []).map(agent => {
                const isAgentSelected = selected?.type === 'agent' && selected.id === agent.agent_id;
                return (
                  <div
                    key={agent.agent_id}
                    onClick={() => setSelected({ type: 'agent', id: agent.agent_id })}
                    className={`flex items-center gap-1.5 px-3 py-2 cursor-pointer transition-colors ${isAgentSelected ? 'bg-surface-container-high text-primary' : 'text-secondary hover:bg-surface-container-high hover:text-on-surface'}`}
                  >
                    <span className="w-4 shrink-0" />
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-3.5 h-3.5 shrink-0">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.75" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                    <span className="text-xs truncate flex-1">{agent.name || agent.role || agent.agent_id}</span>
                  </div>
                );
              })}
            </ul>
          )}
        </aside>

        {/* Right detail panel */}
        <main className="flex-1 overflow-y-auto">
          {selectedProject ? (
            <ProjectDetail
              project={selectedProject}
              agents={agentsByProject[selectedProject.project_id] || []}
              onSelectAgent={id => setSelected({ type: 'agent', id })}
            />
          ) : selectedAgent ? (
            <AgentDetail agent={selectedAgent} />
          ) : (
            <div className="flex flex-col items-center justify-center h-full text-center gap-3 text-secondary">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-10 h-10 opacity-30">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5" />
              </svg>
              <p className="text-sm">Select a project or agent to view details</p>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
