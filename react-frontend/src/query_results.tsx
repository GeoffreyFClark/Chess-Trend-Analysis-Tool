import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';

const QueryResults = () => {
  const location = useLocation();
  const data = location.state?.data;

  return (
    <div>
      <h1>Query Results</h1>
      {data ? <pre>{JSON.stringify(data, null, 2)}</pre> : <p>No data available.</p>}
    </div>
  );
};

export default QueryResults;