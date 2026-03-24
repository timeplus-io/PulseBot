import React, { useState, useMemo } from 'react';

const PAGE_SIZE_DEFAULT = 10;

function SearchIcon() {
  return (
    <svg className="w-4 h-4 text-secondary pointer-events-none" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-4.35-4.35M17 11A6 6 0 105 11a6 6 0 0012 0z" />
    </svg>
  );
}

function formatDetailValue(v) {
  if (v === null || v === undefined) return '—';
  if (Array.isArray(v)) return v.length === 0 ? '[]' : v.join(', ');
  if (typeof v === 'object') return JSON.stringify(v, null, 2);
  if (typeof v === 'boolean') return v ? 'true' : 'false';
  return String(v);
}

function isLongValue(v) {
  if (Array.isArray(v)) return v.length > 3;
  if (typeof v === 'object' && v !== null) return true;
  return typeof v === 'string' && v.length > 80;
}

function RowDetail({ row, onClose, colSpan }) {
  return (
    <tr>
      <td colSpan={colSpan} className="p-0">
        <div className="px-6 py-4 bg-surface-container border-b border-outline-variant/20">
          <div className="flex justify-between items-center mb-3">
            <span className="text-[11px] font-bold uppercase tracking-widest text-secondary">Row Details</span>
            <button
              onClick={e => { e.stopPropagation(); onClose(); }}
              className="w-6 h-6 flex items-center justify-center rounded text-secondary hover:bg-surface-container-high hover:text-on-surface transition-colors"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-4 h-4">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <dl className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-x-6 gap-y-3">
            {Object.entries(row).map(([key, value]) => {
              const long = isLongValue(value);
              return (
                <div key={key} className={`min-w-0 ${long ? 'col-span-full' : ''}`}>
                  <dt className="text-[10px] font-bold uppercase tracking-wider text-secondary mb-0.5">{key}</dt>
                  <dd className="text-xs font-mono text-on-surface break-words whitespace-pre-wrap">
                    {formatDetailValue(value)}
                  </dd>
                </div>
              );
            })}
          </dl>
        </div>
      </td>
    </tr>
  );
}

function PaginationButton({ onClick, disabled, children }) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className="w-7 h-7 flex items-center justify-center rounded text-xs font-medium text-secondary hover:bg-surface-container-high transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
    >
      {children}
    </button>
  );
}

/**
 * DataTable — shared table with search + pagination.
 *
 * Props:
 *   data          — full array of row objects
 *   columns       — [{ header, render, headerClassName?, cellClassName? }]
 *   pageSize      — rows per page (default 10)
 *   emptyMessage  — text when data is empty
 *   loading       — shows loading state instead of table
 *   error         — shows error state instead of table
 */
export default function DataTable({
  data = [],
  columns = [],
  pageSize = PAGE_SIZE_DEFAULT,
  emptyMessage = 'No records found',
  loading = false,
  error = null,
}) {
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);
  const [expandedRow, setExpandedRow] = useState(null);

  const filtered = useMemo(() => {
    const q = search.trim().toLowerCase();
    if (!q) return data;
    return data.filter(row =>
      Object.values(row).some(v => String(v ?? '').toLowerCase().includes(q))
    );
  }, [data, search]);

  const totalPages = Math.max(1, Math.ceil(filtered.length / pageSize));
  const safePage = Math.min(page, totalPages);
  const paged = filtered.slice((safePage - 1) * pageSize, safePage * pageSize);

  const handleSearch = (e) => {
    setSearch(e.target.value);
    setPage(1);
    setExpandedRow(null);
  };

  const handlePageChange = (newPage) => {
    setPage(newPage);
    setExpandedRow(null);
  };

  if (loading) {
    return <div className="px-6 py-12 text-center text-sm text-secondary">Loading...</div>;
  }

  if (error) {
    return <div className="px-6 py-3 text-sm text-on-error-container bg-error-container">Error: {error}</div>;
  }

  return (
    <>
      {/* Search bar */}
      <div className="px-6 py-3 border-b border-outline-variant/10 flex items-center gap-3">
        <div className="relative flex items-center">
          <span className="absolute left-2.5 top-1/2 -translate-y-1/2">
            <SearchIcon />
          </span>
          <input
            type="text"
            value={search}
            onChange={handleSearch}
            placeholder="Search..."
            className="pl-8 pr-3 py-1.5 text-sm bg-surface-container-low rounded border border-outline-variant/20 text-on-surface placeholder:text-secondary outline-none focus:border-primary/40 transition-colors w-60"
          />
        </div>
        {search.trim() && (
          <span className="text-xs text-secondary">
            {filtered.length} result{filtered.length !== 1 ? 's' : ''}
          </span>
        )}
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-surface-container-low">
              {columns.map((col, i) => (
                <th
                  key={i}
                  className={`px-6 py-3 text-[11px] font-bold uppercase tracking-widest text-secondary ${col.headerClassName || ''}`}
                >
                  {col.header}
                </th>
              ))}
              {/* Expand indicator column */}
              <th className="w-8 px-2 py-3" />
            </tr>
          </thead>
          <tbody className="divide-y divide-outline-variant/10">
            {paged.length === 0 ? (
              <tr>
                <td colSpan={columns.length + 1} className="px-6 py-12 text-center text-sm text-secondary">
                  {search.trim() ? 'No results match your search' : emptyMessage}
                </td>
              </tr>
            ) : (
              paged.map((row, i) => {
                const isExpanded = expandedRow === i;
                return (
                  <React.Fragment key={i}>
                    <tr
                      onClick={() => setExpandedRow(isExpanded ? null : i)}
                      className={`hover:bg-surface-container transition-colors cursor-pointer select-none ${isExpanded ? 'bg-surface-container' : i % 2 === 1 ? 'bg-surface-container-low/30' : ''}`}
                    >
                      {columns.map((col, j) => (
                        <td key={j} className={`px-6 py-3.5 ${col.cellClassName || ''}`}>
                          {col.render(row)}
                        </td>
                      ))}
                      <td className="w-8 px-2 py-3.5 text-secondary">
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          fill="none"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                          className={`w-3.5 h-3.5 transition-transform duration-150 ${isExpanded ? 'rotate-180' : ''}`}
                        >
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
                        </svg>
                      </td>
                    </tr>
                    {isExpanded && (
                      <RowDetail
                        row={row}
                        onClose={() => setExpandedRow(null)}
                        colSpan={columns.length + 1}
                      />
                    )}
                  </React.Fragment>
                );
              })
            )}
          </tbody>
        </table>
      </div>

      {/* Footer: record count + pagination */}
      <div className="px-6 py-3 bg-surface-container-low flex justify-between items-center">
        <span className="text-xs text-secondary font-medium">
          {search.trim()
            ? `${filtered.length} of ${data.length} records match`
            : `Showing ${paged.length === data.length ? paged.length : `${(safePage - 1) * pageSize + 1}–${Math.min(safePage * pageSize, filtered.length)}`} of ${data.length} records`}
        </span>
        {totalPages > 1 && (
          <div className="flex items-center gap-1">
            <PaginationButton onClick={() => handlePageChange(1)} disabled={safePage === 1}>«</PaginationButton>
            <PaginationButton onClick={() => handlePageChange(safePage - 1)} disabled={safePage === 1}>‹</PaginationButton>
            <span className="text-xs text-secondary px-2">
              {safePage} / {totalPages}
            </span>
            <PaginationButton onClick={() => handlePageChange(safePage + 1)} disabled={safePage === totalPages}>›</PaginationButton>
            <PaginationButton onClick={() => handlePageChange(totalPages)} disabled={safePage === totalPages}>»</PaginationButton>
          </div>
        )}
      </div>
    </>
  );
}
