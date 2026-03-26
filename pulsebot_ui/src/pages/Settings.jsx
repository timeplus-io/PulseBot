import React, { useState, useEffect, useCallback } from 'react';
import PageHeader from '../components/PageHeader';

// ── Primitive form components ────────────────────────────────────────────────

function Label({ children, htmlFor }) {
  return (
    <label htmlFor={htmlFor} className="text-xs text-[#3A3741]">{children}</label>
  );
}

function Field({ label, hint, children }) {
  return (
    <div className="flex flex-col gap-1.5">
      {label && <Label>{label}</Label>}
      {children}
      {hint && <p className="text-[11px] text-secondary">{hint}</p>}
    </div>
  );
}

function TextInput({ id, value, onChange, placeholder, type = 'text', disabled }) {
  return (
    <input
      id={id}
      type={type}
      value={value ?? ''}
      onChange={e => onChange(e.target.value)}
      placeholder={placeholder}
      disabled={disabled}
      className="h-10 px-3 rounded text-sm bg-white text-[#120F1A] border border-[#B5B4B8]
        focus:outline-none focus:border-[#3A3741] placeholder:text-[#B5B4B8]
        disabled:bg-[#ECECED] disabled:text-[#7D7B82] disabled:cursor-not-allowed transition-colors"
    />
  );
}

function NumberInput({ id, value, onChange, min, max, disabled }) {
  return (
    <input
      id={id}
      type="number"
      value={value ?? ''}
      onChange={e => onChange(Number(e.target.value))}
      min={min}
      max={max}
      disabled={disabled}
      className="h-10 px-3 rounded text-sm bg-white text-[#120F1A] border border-[#B5B4B8]
        focus:outline-none focus:border-[#3A3741]
        disabled:bg-[#ECECED] disabled:text-[#7D7B82] disabled:cursor-not-allowed transition-colors w-36"
    />
  );
}

function SelectInput({ id, value, onChange, options, disabled }) {
  return (
    <select
      id={id}
      value={value ?? ''}
      onChange={e => onChange(e.target.value)}
      disabled={disabled}
      className="h-10 px-3 rounded text-sm bg-white text-[#120F1A] border border-[#B5B4B8]
        focus:outline-none focus:border-[#3A3741]
        disabled:bg-[#ECECED] disabled:text-[#7D7B82] disabled:cursor-not-allowed transition-colors"
    >
      {options.map(o => (
        <option key={o.value} value={o.value}>{o.label}</option>
      ))}
    </select>
  );
}

function Toggle({ checked, onChange, disabled }) {
  return (
    <button
      role="switch"
      aria-checked={checked}
      disabled={disabled}
      onClick={() => !disabled && onChange(!checked)}
      className={`relative w-9 h-5 rounded-full transition-colors flex-shrink-0
        ${disabled
          ? (checked ? 'bg-[#B83280]' : 'bg-[#7D7B82]')
          : (checked ? 'bg-[#D53F8C]' : 'bg-[#B5B4B8]')
        } ${disabled ? 'cursor-not-allowed' : 'cursor-pointer'}`}
    >
      <span className={`absolute top-[3px] w-[14px] h-[14px] rounded-full transition-transform
        ${disabled ? 'bg-[#B5B4B8]' : 'bg-white'}
        ${checked ? 'translate-x-[19px] left-0' : 'left-[3px]'}`}
      />
    </button>
  );
}

function ToggleRow({ label, hint, checked, onChange, disabled }) {
  return (
    <div className="flex items-start justify-between gap-4 py-3 border-b border-[#DAD9DB]/40 last:border-b-0">
      <div className="flex flex-col gap-0.5 flex-1">
        <span className="text-sm text-[#120F1A]">{label}</span>
        {hint && <span className="text-[11px] text-secondary">{hint}</span>}
      </div>
      <Toggle checked={!!checked} onChange={onChange} disabled={disabled} />
    </div>
  );
}

// API key field — shows masked placeholder when key is set server-side,
// clears to empty when the user clicks to edit a new value.
function ApiKeyField({ value, onChange, placeholder = 'Not configured' }) {
  const isServerMasked = value === '***';
  const [editing, setEditing] = useState(false);

  const handleFocus = () => {
    if (isServerMasked) {
      onChange('');
      setEditing(true);
    }
  };

  return (
    <div className="relative">
      <input
        type="password"
        value={isServerMasked && !editing ? '' : (value ?? '')}
        onFocus={handleFocus}
        onChange={e => { setEditing(true); onChange(e.target.value); }}
        placeholder={isServerMasked ? '••••••••  (configured — type to replace)' : placeholder}
        className="w-full h-10 px-3 rounded text-sm bg-white text-[#120F1A] border border-[#B5B4B8]
          focus:outline-none focus:border-[#3A3741] placeholder:text-[#B5B4B8] transition-colors"
      />
    </div>
  );
}

// ── Section card ─────────────────────────────────────────────────────────────

function SectionCard({ id, title, description, children, onSave, saving, saveError, saveOk }) {
  return (
    <section id={id} className="bg-white border border-[#DAD9DB]/60 rounded p-6 flex flex-col gap-5">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="text-sm font-semibold text-[#231F2B]">{title}</h2>
          {description && <p className="text-xs text-secondary mt-0.5">{description}</p>}
        </div>
        <div className="flex items-center gap-3 flex-shrink-0">
          {saveOk && (
            <span className="text-xs text-green-700 flex items-center gap-1">
              <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
              </svg>
              Saved
            </span>
          )}
          {saveError && (
            <span className="text-xs text-red-600 max-w-[200px] truncate" title={saveError}>{saveError}</span>
          )}
          <button
            onClick={onSave}
            disabled={saving}
            className="h-8 px-4 bg-[#D53F8C] hover:bg-[#B83280] text-white text-sm font-semibold rounded
              disabled:bg-[#DAD9DB] disabled:text-[#7D7B82] disabled:cursor-not-allowed transition-colors flex items-center gap-2"
          >
            {saving && (
              <svg className="w-3.5 h-3.5 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
              </svg>
            )}
            Save
          </button>
        </div>
      </div>
      <div className="flex flex-col gap-4">
        {children}
      </div>
    </section>
  );
}

// ── Provider sub-section ─────────────────────────────────────────────────────

function ProviderSection({ name, label, config, onChange }) {
  const hasBaseUrl = ['openai', 'openrouter'].includes(name);
  const isOllama = name === 'ollama';
  const hasTimeout = ['gemini', 'ollama', 'nvidia'].includes(name);
  const hasThinking = name === 'nvidia';

  return (
    <div className="flex flex-col gap-3 py-4 border-b border-[#DAD9DB]/40 last:border-b-0">
      <h3 className="text-xs font-semibold text-[#3A3741] uppercase tracking-wider">{label}</h3>
      <div className="grid grid-cols-2 gap-4">
        {isOllama ? (
          <Field label="Host URL">
            <TextInput
              value={config?.host}
              onChange={v => onChange({ ...config, host: v })}
              placeholder="http://localhost:11434"
            />
          </Field>
        ) : (
          <Field label="API Key">
            <ApiKeyField
              value={config?.api_key}
              onChange={v => onChange({ ...config, api_key: v })}
            />
          </Field>
        )}
        <Field label="Default Model">
          <TextInput
            value={config?.default_model}
            onChange={v => onChange({ ...config, default_model: v })}
            placeholder="e.g. gpt-4o"
          />
        </Field>
        {hasBaseUrl && (
          <Field label="Base URL" hint="Override for OpenAI-compatible endpoints">
            <TextInput
              value={config?.base_url ?? ''}
              onChange={v => onChange({ ...config, base_url: v || null })}
              placeholder="https://api.openai.com/v1"
            />
          </Field>
        )}
        {hasTimeout && (
          <Field label="Timeout (seconds)">
            <NumberInput
              value={config?.timeout_seconds}
              onChange={v => onChange({ ...config, timeout_seconds: v })}
              min={10}
            />
          </Field>
        )}
      </div>
      {hasThinking && (
        <ToggleRow
          label="Enable Thinking"
          hint="Extended reasoning mode (supported models only)"
          checked={config?.enable_thinking}
          onChange={v => onChange({ ...config, enable_thinking: v })}
        />
      )}
    </div>
  );
}

// ── Sidebar nav ──────────────────────────────────────────────────────────────

const SECTIONS = [
  { id: 'timeplus',     label: 'Timeplus' },
  { id: 'agent',        label: 'Agent' },
  { id: 'providers',    label: 'Providers' },
  { id: 'channels',     label: 'Channels' },
  { id: 'skills',       label: 'Skills' },
  { id: 'memory',       label: 'Memory' },
  { id: 'multi-agent',  label: 'Multi-Agent' },
  { id: 'observability',label: 'Observability' },
  { id: 'logging',      label: 'Logging' },
];

// ── Main page ────────────────────────────────────────────────────────────────

export default function Settings() {
  const [config, setConfig] = useState(null);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState(null);
  const [saving, setSaving] = useState({});
  const [saveError, setSaveError] = useState({});
  const [saveOk, setSaveOk] = useState({});
  const [activeSection, setActiveSection] = useState('timeplus');

  const load = useCallback(async () => {
    setLoading(true);
    setLoadError(null);
    try {
      const res = await fetch('/config');
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      setConfig(await res.json());
    } catch (e) {
      setLoadError(e.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const save = useCallback(async (sectionKey, patch) => {
    setSaving(s => ({ ...s, [sectionKey]: true }));
    setSaveError(s => ({ ...s, [sectionKey]: null }));
    setSaveOk(s => ({ ...s, [sectionKey]: false }));
    try {
      const res = await fetch('/config', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(patch),
      });
      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.detail || `HTTP ${res.status}`);
      }
      const updated = await res.json();
      const warning = updated._warning;
      const { _warning, ...cleanConfig } = updated;
      setConfig(prev => ({ ...prev, ...cleanConfig }));
      if (warning) {
        setSaveError(s => ({ ...s, [sectionKey]: warning }));
      } else {
        setSaveOk(s => ({ ...s, [sectionKey]: true }));
        setTimeout(() => setSaveOk(s => ({ ...s, [sectionKey]: false })), 3000);
      }
    } catch (e) {
      setSaveError(s => ({ ...s, [sectionKey]: e.message }));
    } finally {
      setSaving(s => ({ ...s, [sectionKey]: false }));
    }
  }, []);

  const update = useCallback((path, value) => {
    setConfig(prev => {
      if (!prev) return prev;
      const next = { ...prev };
      if (path.length === 1) {
        next[path[0]] = value;
      } else if (path.length === 2) {
        next[path[0]] = { ...prev[path[0]], [path[1]]: value };
      } else if (path.length === 3) {
        next[path[0]] = {
          ...prev[path[0]],
          [path[1]]: { ...prev[path[0]]?.[path[1]], [path[2]]: value },
        };
      }
      return next;
    });
  }, []);

  const scrollTo = (id) => {
    setActiveSection(id);
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  if (loading) {
    return (
      <div className="flex-1 flex items-center justify-center text-sm text-secondary bg-[#F7F6F6]">
        Loading configuration…
      </div>
    );
  }

  if (loadError) {
    return (
      <div className="flex-1 flex items-center justify-center bg-[#F7F6F6]">
        <div className="text-sm text-red-600 bg-red-50 border border-red-200 rounded px-4 py-3">
          Failed to load configuration: {loadError}
        </div>
      </div>
    );
  }

  const c = config;

  return (
    <div className="flex-1 flex flex-col min-h-0 bg-[#F7F6F6] overflow-hidden">
      <PageHeader title="Settings" onRefresh={load} />

      {/* Restart notice */}
      <div className="flex items-center gap-2 px-6 py-2.5 bg-amber-50 border-b border-amber-200 text-xs text-amber-800">
        <svg className="w-3.5 h-3.5 flex-shrink-0 text-amber-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span>
          Configuration is saved to <code className="font-mono">config.yaml</code>. Most settings are read by the agent at startup —
          <strong className="font-semibold"> restart the agent container</strong> for changes to take effect.
        </span>
      </div>

      <div className="flex flex-1 min-h-0 gap-0">
        {/* Section nav */}
        <nav className="w-44 flex-shrink-0 flex flex-col gap-0.5 py-4 px-3 border-r border-[#DAD9DB]/40 bg-white">
          {SECTIONS.map(s => (
            <button
              key={s.id}
              onClick={() => scrollTo(s.id)}
              className={`text-left px-3 py-2 rounded text-xs font-semibold uppercase tracking-[0.05em] transition-colors
                ${activeSection === s.id
                  ? 'bg-[#E9E8E8] text-[#ad1a6c]'
                  : 'text-[#5d5c74] hover:bg-[#E9E8E8]'
                }`}
            >
              {s.label}
            </button>
          ))}
        </nav>

        {/* Scrollable content */}
        <div className="flex-1 overflow-y-auto px-6 py-6 flex flex-col gap-5">

          {/* ── Timeplus ── */}
          <SectionCard
            id="timeplus"
            title="Timeplus"
            description="Connection settings for the Timeplus/Proton streaming database."
            onSave={() => save('timeplus', { timeplus: c.timeplus })}
            saving={saving.timeplus}
            saveError={saveError.timeplus}
            saveOk={saveOk.timeplus}
          >
            <div className="grid grid-cols-2 gap-4">
              <Field label="Host">
                <TextInput
                  value={c.timeplus?.host}
                  onChange={v => update(['timeplus', 'host'], v)}
                  placeholder="localhost"
                />
              </Field>
              <Field label="Port">
                <NumberInput
                  value={c.timeplus?.port}
                  onChange={v => update(['timeplus', 'port'], v)}
                  min={1} max={65535}
                />
              </Field>
              <Field label="Username">
                <TextInput
                  value={c.timeplus?.username}
                  onChange={v => update(['timeplus', 'username'], v)}
                  placeholder="default"
                />
              </Field>
              <Field label="Password">
                <ApiKeyField
                  value={c.timeplus?.password}
                  onChange={v => update(['timeplus', 'password'], v)}
                  placeholder="No password"
                />
              </Field>
            </div>
          </SectionCard>

          {/* ── Agent ── */}
          <SectionCard
            id="agent"
            title="Agent"

            description="Core identity and LLM behaviour for the main agent."
            onSave={() => save('agent', { agent: c.agent })}
            saving={saving.agent}
            saveError={saveError.agent}
            saveOk={saveOk.agent}
          >
            <div className="grid grid-cols-2 gap-4">
              <Field label="Name">
                <TextInput value={c.agent?.name} onChange={v => update(['agent', 'name'], v)} />
              </Field>
              <Field label="Provider">
                <SelectInput
                  value={c.agent?.provider}
                  onChange={v => update(['agent', 'provider'], v)}
                  options={[
                    { value: 'anthropic', label: 'Anthropic' },
                    { value: 'openai', label: 'OpenAI' },
                    { value: 'openrouter', label: 'OpenRouter' },
                    { value: 'gemini', label: 'Google Gemini' },
                    { value: 'ollama', label: 'Ollama (local)' },
                    { value: 'nvidia', label: 'NVIDIA NIM' },
                  ]}
                />
              </Field>
              <Field label="Model" hint="Model ID for the chosen provider">
                <TextInput
                  value={c.agent?.model}
                  onChange={v => update(['agent', 'model'], v)}
                  placeholder="e.g. claude-sonnet-4-20250514"
                />
              </Field>
              <Field label="Temperature" hint="0.0 = deterministic · 1.0 = creative">
                <NumberInput
                  value={c.agent?.temperature}
                  onChange={v => update(['agent', 'temperature'], v)}
                  min={0} max={2}
                />
              </Field>
              <Field label="Max Output Tokens">
                <NumberInput
                  value={c.agent?.max_tokens}
                  onChange={v => update(['agent', 'max_tokens'], v)}
                  min={256}
                />
              </Field>
              <Field label="Max Iterations" hint="Max tool-call loops per user message">
                <NumberInput
                  value={c.agent?.max_iterations}
                  onChange={v => update(['agent', 'max_iterations'], v)}
                  min={1} max={50}
                />
              </Field>
            </div>
            <ToggleRow
              label="Verbose Tool Logging"
              hint="Log full tool arguments and results to console"
              checked={c.agent?.verbose_tools}
              onChange={v => update(['agent', 'verbose_tools'], v)}
            />
          </SectionCard>

          {/* ── Providers ── */}
          <SectionCard
            id="providers"
            title="Providers"

            description="API keys and default models for each LLM provider. Only configure the providers you use."
            onSave={() => save('providers', { providers: c.providers })}
            saving={saving.providers}
            saveError={saveError.providers}
            saveOk={saveOk.providers}
          >
            {[
              { name: 'anthropic',  label: 'Anthropic Claude' },
              { name: 'openai',     label: 'OpenAI' },
              { name: 'openrouter', label: 'OpenRouter' },
              { name: 'gemini',     label: 'Google Gemini' },
              { name: 'ollama',     label: 'Ollama (local)' },
              { name: 'nvidia',     label: 'NVIDIA NIM' },
            ].map(p => (
              <ProviderSection
                key={p.name}
                name={p.name}
                label={p.label}
                config={c.providers?.[p.name]}
                onChange={v => update(['providers', p.name], v)}
              />
            ))}
          </SectionCard>

          {/* ── Channels ── */}
          <SectionCard
            id="channels"
            title="Channels"

            description="Input channels. Web chat is always available via the API server."
            onSave={() => save('channels', { channels: c.channels })}
            saving={saving.channels}
            saveError={saveError.channels}
            saveOk={saveOk.channels}
          >
            <div className="flex flex-col">
              <h3 className="text-xs font-semibold text-[#3A3741] uppercase tracking-wider mb-3">Telegram</h3>
              <ToggleRow
                label="Enabled"
                checked={c.channels?.telegram?.enabled}
                onChange={v => update(['channels', 'telegram', 'enabled'], v)}
              />
              <div className="grid grid-cols-2 gap-4 mt-3">
                <Field label="Bot Token">
                  <ApiKeyField
                    value={c.channels?.telegram?.token}
                    onChange={v => update(['channels', 'telegram', 'token'], v)}
                    placeholder="Not configured"
                  />
                </Field>
              </div>
            </div>
          </SectionCard>

          {/* ── Skills ── */}
          <SectionCard
            id="skills"
            title="Skills"
            description="Built-in tools, custom skills, and ClawHub registry integration."
            onSave={() => save('skills', { skills: c.skills })}
            saving={saving.skills}
            saveError={saveError.skills}
            saveOk={saveOk.skills}
          >
            <Field label="Built-in Skills" hint="Comma-separated list of enabled built-ins (e.g. file_ops, shell, workspace)">
              <TextInput
                value={(c.skills?.builtin ?? []).join(', ')}
                onChange={v => update(['skills', 'builtin'], v.split(',').map(s => s.trim()).filter(Boolean))}
                placeholder="file_ops, shell"
              />
            </Field>
            <Field label="Disabled Skills" hint="Skills to suppress even if installed (comma-separated slugs)">
              <TextInput
                value={(c.skills?.disabled_skills ?? []).join(', ')}
                onChange={v => update(['skills', 'disabled_skills'], v.split(',').map(s => s.trim()).filter(Boolean))}
                placeholder=""
              />
            </Field>
            <Field label="Skill Directories" hint="Paths to scan for agentskills packages (comma-separated)">
              <TextInput
                value={(c.skills?.skill_dirs ?? []).join(', ')}
                onChange={v => update(['skills', 'skill_dirs'], v.split(',').map(s => s.trim()).filter(Boolean))}
                placeholder="./skills"
              />
            </Field>
            <div className="flex flex-col pt-2 border-t border-[#DAD9DB]/40">
              <h3 className="text-xs font-semibold text-[#3A3741] uppercase tracking-wider mb-3">ClawHub Registry</h3>
              <div className="grid grid-cols-2 gap-4">
                <Field label="Auth Token" hint="Bearer token for authenticated registry access">
                  <ApiKeyField
                    value={c.skills?.clawhub?.auth_token}
                    onChange={v => update(['skills', 'clawhub', 'auth_token'], v)}
                    placeholder="Not configured"
                  />
                </Field>
                <Field label="Install Directory" hint="Defaults to first skill directory">
                  <TextInput
                    value={c.skills?.clawhub?.install_dir ?? ''}
                    onChange={v => update(['skills', 'clawhub', 'install_dir'], v || null)}
                    placeholder="(auto)"
                  />
                </Field>
                <Field label="Site URL" hint="Override registry site (default: clawhub.ai)">
                  <TextInput
                    value={c.skills?.clawhub?.site_url}
                    onChange={v => update(['skills', 'clawhub', 'site_url'], v)}
                    placeholder="https://clawhub.ai"
                  />
                </Field>
              </div>
            </div>
          </SectionCard>

          {/* ── Memory ── */}
          <SectionCard
            id="memory"
            title="Memory"

            description="Vector-indexed long-term memory and embedding configuration."
            onSave={() => save('memory', { memory: c.memory })}
            saving={saving.memory}
            saveError={saveError.memory}
            saveOk={saveOk.memory}
          >
            <ToggleRow
              label="Enabled"
              hint="Enable vector memory for long-term recall across sessions"
              checked={c.memory?.enabled}
              onChange={v => update(['memory', 'enabled'], v)}
            />
            <div className="grid grid-cols-2 gap-4">
              <Field label="Similarity Threshold" hint="Cosine similarity floor for duplicate suppression (0.0–1.0)">
                <NumberInput
                  value={c.memory?.similarity_threshold}
                  onChange={v => update(['memory', 'similarity_threshold'], v)}
                  min={0} max={1}
                />
              </Field>
              <Field label="Embedding Provider">
                <SelectInput
                  value={c.memory?.embedding_provider}
                  onChange={v => update(['memory', 'embedding_provider'], v)}
                  options={[
                    { value: 'local', label: 'Local (sentence-transformers)' },
                    { value: 'openai', label: 'OpenAI' },
                    { value: 'ollama', label: 'Ollama' },
                  ]}
                />
              </Field>
              <Field label="Embedding Model" hint="e.g. all-MiniLM-L6-v2 · text-embedding-3-small">
                <TextInput
                  value={c.memory?.embedding_model}
                  onChange={v => update(['memory', 'embedding_model'], v)}
                />
              </Field>
              <Field label="Embedding Timeout (seconds)">
                <NumberInput
                  value={c.memory?.embedding_timeout_seconds}
                  onChange={v => update(['memory', 'embedding_timeout_seconds'], v)}
                  min={5}
                />
              </Field>
            </div>
          </SectionCard>

          {/* ── Multi-Agent ── */}
          <SectionCard
            id="multi-agent"
            title="Multi-Agent"

            description="Resource limits for parallel and pipeline sub-agent projects."
            onSave={() => save('multi_agent', { multi_agent: c.multi_agent })}
            saving={saving.multi_agent}
            saveError={saveError.multi_agent}
            saveOk={saveOk.multi_agent}
          >
            <div className="grid grid-cols-2 gap-4">
              <Field label="Max Agents per Project">
                <NumberInput
                  value={c.multi_agent?.max_agents_per_project}
                  onChange={v => update(['multi_agent', 'max_agents_per_project'], v)}
                  min={1} max={50}
                />
              </Field>
              <Field label="Max Concurrent Projects">
                <NumberInput
                  value={c.multi_agent?.max_concurrent_projects}
                  onChange={v => update(['multi_agent', 'max_concurrent_projects'], v)}
                  min={1}
                />
              </Field>
            </div>
          </SectionCard>

          {/* ── Observability ── */}
          <SectionCard
            id="observability"
            title="Observability"

            description="Event stream controls and debug settings."
            onSave={() => save('observability', { observability: c.observability })}
            saving={saving.observability}
            saveError={saveError.observability}
            saveOk={saveOk.observability}
          >
            <ToggleRow
              label="Events Enabled"
              hint="Emit structured events to the pulsebot.events stream"
              checked={c.observability?.events?.enabled}
              onChange={v => update(['observability', 'events', 'enabled'], v)}
            />
            <div className="grid grid-cols-2 gap-4">
              <Field label="Minimum Severity" hint="Events below this level are not emitted">
                <SelectInput
                  value={c.observability?.events?.min_severity}
                  onChange={v => update(['observability', 'events', 'min_severity'], v)}
                  options={[
                    { value: 'debug',    label: 'Debug' },
                    { value: 'info',     label: 'Info' },
                    { value: 'warning',  label: 'Warning' },
                    { value: 'error',    label: 'Error' },
                    { value: 'critical', label: 'Critical' },
                  ]}
                />
              </Field>
            </div>
          </SectionCard>

          {/* ── Logging ── */}
          <SectionCard
            id="logging"
            title="Logging"

            description="Server-side log level and output format."
            onSave={() => save('logging', { logging: c.logging })}
            saving={saving.logging}
            saveError={saveError.logging}
            saveOk={saveOk.logging}
          >
            <div className="grid grid-cols-2 gap-4">
              <Field label="Log Level">
                <SelectInput
                  value={c.logging?.level}
                  onChange={v => update(['logging', 'level'], v)}
                  options={[
                    { value: 'DEBUG',    label: 'Debug' },
                    { value: 'INFO',     label: 'Info' },
                    { value: 'WARNING',  label: 'Warning' },
                    { value: 'ERROR',    label: 'Error' },
                    { value: 'CRITICAL', label: 'Critical' },
                  ]}
                />
              </Field>
              <Field label="Log Format">
                <SelectInput
                  value={c.logging?.format}
                  onChange={v => update(['logging', 'format'], v)}
                  options={[
                    { value: 'json', label: 'JSON (structured)' },
                    { value: 'text', label: 'Text (human-readable)' },
                  ]}
                />
              </Field>
            </div>
          </SectionCard>

          <p className="text-[11px] text-secondary text-center pb-4">
            Changes are applied immediately in memory. To persist across restarts, the agent must be able to write to
            <code className="font-mono"> config.yaml</code>.
          </p>
        </div>
      </div>
    </div>
  );
}
