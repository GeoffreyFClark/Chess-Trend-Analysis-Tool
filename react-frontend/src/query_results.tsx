import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import Graph2 from './Graphs';

const QueryResults = () => {
  const location = useLocation();
  const data = location.state?.data; // returns an array of dicts

  if ("RISKYPLAYSPERCENT" in data[0]) {
    console.log("Query 2 Activated");
    return (
    <div>
      <h1>Query Results</h1>
      <Graph2 data={data} />
    </div>
  );
  }
  if ("SAMPLEOVEREXPECTED" in data[0] ){
    console.log("Query 3 Activated");
    return(
        <div>
          <h1>Query Results</h1>

        </div>
    );
  }
  else {
    return (
        <div>
          <h1>Query Results</h1>
          {data ? <pre>{JSON.stringify(data, null, 2)}</pre> : <p>No data available.</p>}
        </div>
    );
  }
};

export default QueryResults;