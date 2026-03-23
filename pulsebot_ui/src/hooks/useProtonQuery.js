import { useState, useCallback } from 'react';

const QUERY_URL = import.meta.env.DEV ? 'http://localhost:8000/query' : '/query';

export function useProtonQuery() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const query = useCallback(async (sql) => {
    setLoading(true);
    setError(null);
    try {
      const resp = await fetch(QUERY_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'text/plain' },
        body: sql,
      });
      const text = await resp.text();
      if (!resp.ok) {
        throw new Error(text || `HTTP ${resp.status}`);
      }
      const rows = text
        .trim()
        .split('\n')
        .filter(Boolean)
        .map(line => JSON.parse(line));
      setData(rows);
    } catch (e) {
      setError(e.message);
      setData([]);
    } finally {
      setLoading(false);
    }
  }, []);

  return { data, loading, error, query };
}
