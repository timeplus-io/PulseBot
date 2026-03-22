import React, { useEffect } from 'react';
import { useProtonQuery } from '../hooks/useProtonQuery';

function RefreshButton({ onClick, loading }) {
  return (
    <button
      onClick={onClick}
      disabled={loading}
      className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-on-surface-variant bg-surface-container hover:bg-surface-container-high rounded transition-colors disabled:opacity-50"
    >
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`}>
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
      </svg>
      Refresh
    </button>
  );
}

function projectStatusStyle(status) {
  const map = {
    active: 'bg-on-tertiary-container text-tertiary',
    completed: 'bg-secondary-container text-on-secondary-fixed',
    paused: 'bg-[#fff3cd] text-[#856404]',
    failed: 'bg-error-container text-on-error-container',
  };
  return map[status] || 'bg-surface-container text-on-surface-variant';
}

function agentStatusStyle(status) {
  const map = {
    idle: 'bg-surface-container text-on-surface-variant',
    working: 'bg-primary-fixed text-on-primary-fixed',
    done: 'bg-on-tertiary-container text-tertiary',
    failed: 'bg-error-container text-on-error-container',
  };
  return map[status] || 'bg-surface-container text-on-surface-variant';
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

  // Group agents by project_id
  const agentsByProject = agents.reduce((acc, agent) => {
    const pid = agent.project_id || 'unassigned';
    if (!acc[pid]) acc[pid] = [];
    acc[pid].push(agent);
    return acc;
  }, {});

  return (
    <div className="flex flex-col h-full overflow-hidden">
      {/* Header */}
      <header className="glass-header ambient-shadow border-b border-surface-container-high px-6 py-4 flex items-center gap-3 flex-shrink-0">
        <h1 className="text-base font-semibold text-on-surface">Agents & Projects</h1>
        <div className="ml-auto">
          <RefreshButton onClick={load} loading={isLoading} />
        </div>
      </header>

      {/* Content */}
      <div className="flex-1 overflow-auto p-6">
        {(projError || agentsError) && (
          <div className="mb-4 px-4 py-3 text-sm text-on-error-container bg-error-container rounded-lg">
            {projError || agentsError}
          </div>
        )}

        {isLoading ? (
          <div className="text-center py-12 text-sm text-on-surface-variant">Loading...</div>
        ) : projects.length === 0 ? (
          <div className="text-center py-16 text-sm text-on-surface-variant">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-12 h-12 mx-auto mb-3 text-outline opacity-50">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <p>No projects found</p>
          </div>
        ) : (
          <div className="flex flex-col gap-6">
            {projects.map((project) => {
              const projectAgents = agentsByProject[project.project_id] || [];
              return (
                <div key={project.project_id} className="bg-surface-container-lowest rounded-lg ambient-shadow">
                  {/* Project Header */}
                  <div className="px-5 py-4 border-b border-surface-container-high flex items-start gap-3">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 flex-wrap">
                        <h2 className="text-sm font-semibold text-on-surface">{project.name || 'Unnamed Project'}</h2>
                        <span className={`inline-flex px-2 py-0.5 rounded text-xs font-medium ${projectStatusStyle(project.status)}`}>
                          {project.status}
                        </span>
                      </div>
                      {project.description && (
                        <p className="text-xs text-on-surface-variant mt-0.5">{project.description}</p>
                      )}
                    </div>
                    <div className="text-xs text-on-surface-variant text-right shrink-0">
                      <div className="font-mono">{project.project_id?.slice(0, 8)}</div>
                      <div>{project.timestamp ? new Date(project.timestamp).toLocaleString() : ''}</div>
                    </div>
                  </div>

                  {/* Agents Grid */}
                  {projectAgents.length === 0 ? (
                    <div className="px-5 py-4 text-xs text-on-surface-variant">No agents assigned</div>
                  ) : (
                    <div className="p-4 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                      {projectAgents.map((agent) => (
                        <div key={agent.agent_id} className="bg-surface-container rounded p-3 flex flex-col gap-1.5">
                          <div className="flex items-center gap-2">
                            <span className="text-xs font-semibold text-on-surface">{agent.name || agent.role}</span>
                            <span className={`ml-auto inline-flex px-2 py-0.5 rounded text-xs font-medium ${agentStatusStyle(agent.status)}`}>
                              {agent.status}
                            </span>
                          </div>
                          {agent.role && agent.name && (
                            <div className="text-xs text-on-surface-variant">{agent.role}</div>
                          )}
                          {agent.task_description && (
                            <div className="text-xs text-on-surface-variant line-clamp-2">{agent.task_description}</div>
                          )}
                          {agent.skills && (
                            <div className="flex flex-wrap gap-1 mt-0.5">
                              {(Array.isArray(agent.skills) ? agent.skills : String(agent.skills).split(',')).map((skill, si) => (
                                <span key={si} className="px-1.5 py-0.5 bg-secondary-container text-on-secondary-fixed rounded text-[10px] font-medium">
                                  {String(skill).trim()}
                                </span>
                              ))}
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
