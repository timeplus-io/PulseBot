import React from 'react';

export default function PageHeader({ onRefresh, loading }) {
  return (
    <header className="glass-header ambient-shadow sticky top-0 z-50 flex justify-end items-center w-full px-4 py-2 flex-shrink-0">
      <button
        onClick={onRefresh}
        disabled={loading}
        title="Refresh"
        className="p-2 rounded-lg text-secondary hover:bg-surface-container-high transition-colors active:scale-95 duration-200 disabled:opacity-50"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className={`w-5 h-5 ${loading ? 'animate-spin' : ''}`}>
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
      </button>
    </header>
  );
}
