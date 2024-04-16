import React, { useState, useEffect } from 'react';

function TestQuery() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError('');
      try {
        const response = await fetch('http://localhost:5000/api/test-query');
        console.log('Response:', response);
        if (!response.ok) {
          throw new Error(`HTTP status ${response.status}`);
        }
        const data = await response.json();
        console.log('Data received:', data);
        setResults(data);
      } catch (err) {
        const message = (err instanceof Error) ? err.message : 'An unknown error occurred';
        console.error('Fetch error:', message);
        setError(`Failed to load data: ${message}`);
      } finally {
        setLoading(false);
      }
    };
  
    fetchData();
  }, []);
  

  return (
    <div>
      <h1>Test Query Results</h1>
      {loading && <p>Loading...</p>}
      {error && <p className="error">{error}</p>}
      {results.length > 0 ? (
        <ul>
          {results.map((result, index) => (
            <li key={index}>
              <pre>{JSON.stringify(result, null, 2)}</pre>
            </li>
          ))}
        </ul>
      ) : !loading && !error && <p>No data found.</p>}
    </div>
  );
}

export default TestQuery;
