import React, { useEffect } from 'react';
import { useProtonQuery } from '../hooks/useProtonQuery';
import PageHeader from '../components/PageHeader';

function agentStatusBadge(status) {
  const map = {
    active: 'bg-tertiary/10 text-tertiary',
    working: 'bg-tertiary/10 text-tertiary',
    done: 'bg-tertiary/10 text-tertiary',
    idle: 'bg-secondary/10 text-secondary',
    inactive: 'bg-secondary/10 text-secondary',
    failed: 'bg-obs-error/10 text-obs-error',
  };
  return map[(status || '').toLowerCase()] || 'bg-secondary/10 text-secondary';
}

function projectStatusBadge(status) {
  const map = {
    active: 'bg-tertiary/10 text-tertiary',
    completed: 'bg-secondary/10 text-secondary',
    paused: 'bg-[#fff3cd] text-[#856404]',
    failed: 'bg-obs-error/10 text-obs-error',
  };
  return map[(status || '').toLowerCase()] || 'bg-secondary/10 text-secondary';
}

function borderColor(status) {
  const s = (status || '').toLowerCase();
  if (s === 'active' || s === 'working' || s === 'done') return 'border-primary';
  return 'border-secondary';
}

export default function Agents() {
  const { data: projects, loading: projLoading, error: projError, query: queryProjects } = useProtonQuery();
  const { data: agents, loading: agentsLoading, error: agentsError, query: queryAgents } = useProtonQuery();

  const load = () => {
    queryProjects(`SELECT project_id, timestamp, name, description, status, created_by, session_id FROM table(pulsebot.kanban_projects) ORDER BY timestamp DESC LIMIT 50`);
    queryAgents(`SELECT agent_id, timestamp, project_id, name, role, task_description, status, skills FROM table(pulsebot.kanban_agents) ORDER BY timestamp DESC LIMIT 200`);
  };

  useEffect(() => { load(); }, []);

  const isLoading = projLoading || agentsLoading;
  const agentsByProject = agents.reduce((acc, agent) => {
    const pid = agent.project_id || 'unassigned';
    if (!acc[pid]) acc[pid] = [];
    acc[pid].push(agent);
    return acc;
  }, {});

  return (
    <div className="flex flex-col h-full overflow-hidden">
      <PageHeader onRefresh={load} loading={isLoading} />

      <div className="flex-1 overflow-y-auto p-8 max-w-[1400px] w-full mx-auto space-y-8">
        {(projError || agentsError) && (
          <div className="px-4 py-3 text-sm text-on-error-container bg-error-container rounded-lg">
            {projError || agentsError}
          </div>
        )}

        {isLoading ? (
          <div className="text-center py-16 text-sm text-secondary">Loading...</div>
        ) : projects.length === 0 && agents.length === 0 ? (
          <div className="text-center py-16">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-12 h-12 mx-auto mb-3 text-outline opacity-50">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <p className="text-sm text-secondary">No agents or projects found</p>
          </div>
        ) : (
          <>
            {/* Agent Cards Grid */}
            {agents.length > 0 && (
              <section>
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-lg font-bold text-on-surface flex items-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-5 h-5 text-primary">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.75" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
                    </svg>
                    Active Intelligence Units
                  </h2>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                  {agents.map((agent) => (
                    <div
                      key={agent.agent_id}
                      className={`bg-surface-container-lowest rounded-lg p-5 shadow-[0_4px_20px_rgba(26,28,28,0.06)] border-l-2 ${borderColor(agent.status)} group hover:-translate-y-0.5 transition-transform duration-200`}
                    >
                      <div className="flex justify-between items-start mb-4">
                        <div>
                          <h4 className="font-bold text-on-surface group-hover:text-primary transition-colors">
                            {agent.name || agent.role || 'Unnamed Agent'}
                          </h4>
                          {agent.role && agent.name && (
                            <p className="text-[11px] text-secondary font-medium mt-0.5">{agent.role}</p>
                          )}
                          {agent.project_id && (
                            <p className="text-[11px] text-secondary font-medium mt-0.5">
                              Project: <span className="text-on-surface">{agent.project_id.slice(0, 8)}</span>
                            </p>
                          )}
                        </div>
                        <span className={`px-2 py-0.5 rounded text-[9px] font-bold uppercase tracking-wider ${agentStatusBadge(agent.status)}`}>
                          {agent.status || 'unknown'}
                        </span>
                      </div>
                      {agent.task_description && (
                        <p className="text-xs text-secondary mb-3 line-clamp-2">{agent.task_description}</p>
                      )}
                      <div className="flex items-center justify-between text-[10px] text-secondary border-t border-surface-container pt-4">
                        <span className="font-mono">{agent.agent_id?.slice(0, 12)}</span>
                        {agent.skills && (
                          <div className="flex flex-wrap gap-1">
                            {(Array.isArray(agent.skills) ? agent.skills : String(agent.skills).split(',')).slice(0, 2).map((s, si) => (
                              <span key={si} className="px-1.5 py-0.5 bg-secondary-container text-on-secondary-fixed-variant rounded text-[9px] font-bold">
                                {String(s).trim()}
                              </span>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </section>
            )}

            {/* Projects with grouped agents */}
            {projects.length > 0 && (
              <section className="bg-surface-container-low rounded-lg p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="uppercase tracking-[0.05em] text-[11px] font-semibold text-secondary">Projects</h3>
                </div>
                <div className="space-y-0.5">
                  {projects.map((project) => {
                    const projectAgents = agentsByProject[project.project_id] || [];
                    return (
                      <div key={project.project_id} className="flex items-center justify-between py-2 px-4 hover:bg-surface-container-high transition-colors rounded">
                        <div className="flex items-center gap-4">
                          <div className={`w-6 h-6 rounded flex items-center justify-center text-white`}
                            style={{ background: '#ad1a6c' }}>
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-3.5 h-3.5">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                            </svg>
                          </div>
                          <span className="text-xs font-medium text-on-surface">{project.name || project.project_id}</span>
                          {project.description && (
                            <span className="text-xs text-secondary hidden lg:block">{project.description}</span>
                          )}
                        </div>
                        <div className="flex items-center gap-3">
                          <span className="text-[10px] font-mono text-secondary">{projectAgents.length} agents</span>
                          <span className={`text-[10px] font-bold uppercase tracking-tighter ${projectStatusBadge(project.status).split(' ')[1]}`}>
                            {project.status}
                          </span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </section>
            )}
          </>
        )}
      </div>
    </div>
  );
}
