import React from 'react';

/**
 * Card — shared container card for table sections and panels.
 *
 * Props:
 *   children   — card content
 *   className  — additional classes (e.g. for margin/flex overrides)
 */
export default function Card({ children, className = '' }) {
  return (
    <div className={`bg-surface-container-lowest rounded-lg ambient-shadow border border-outline-variant/10 overflow-hidden ${className}`}>
      {children}
    </div>
  );
}
