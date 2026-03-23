import React from 'react';

/**
 * MetricCard — shared stat card used across observability pages.
 *
 * Props:
 *   label     — uppercase label at top
 *   value     — large bold value
 *   icon      — optional SVG/ReactNode shown top-right
 *   tag       — optional small inline label beside value (e.g. "Stable", "sources")
 *   tagColor  — Tailwind text color class for tag (default: text-secondary)
 *   subtitle  — optional small text below value
 */
export default function MetricCard({ label, value, icon, tag, tagColor = 'text-secondary', subtitle, subtitleColor = 'text-secondary' }) {
  return (
    <div className="bg-surface-container-lowest p-6 rounded-lg ambient-shadow border border-outline-variant/10">
      <div className="flex justify-between items-start mb-4">
        <span className="text-[11px] font-bold uppercase tracking-widest text-secondary">{label}</span>
        {icon && <span>{icon}</span>}
      </div>
      <div className="flex items-baseline gap-2">
        <span className="text-3xl font-bold text-on-surface">{value ?? '—'}</span>
        {tag && <span className={`text-xs font-medium ${tagColor}`}>{tag}</span>}
      </div>
      {subtitle && <p className={`text-[10px] font-semibold mt-2 ${subtitleColor}`}>{subtitle}</p>}
    </div>
  );
}
