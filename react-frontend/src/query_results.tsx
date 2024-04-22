import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import Graph2 from './Graphs';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, } from 'recharts';

const formatTick = (tick) => {
  return new Date(tick).getFullYear();
};

const ResultsChart = ({ data }) => {
  console.log("Data received for chart:", data);
  const transformedData = data.map((entry) => ({
    ...entry,
    year: new Date(entry.year).getFullYear(), 
    popularity: parseFloat(entry.popularity), 
    winrate: parseFloat(entry.winrate), 
  }));

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={transformedData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="year" tickFormatter={formatTick} />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="popularity" stroke="#8884d8" activeDot={{ r: 8 }} />
        <Line type="monotone" dataKey="winrate" stroke="#82ca9d" />
      </LineChart>
    </ResponsiveContainer>
  );
};

const QueryResults = () => {
  const location = useLocation();
  const data = location.state?.data; // returns an array of dicts
  console.log("Query Results Data:")
  console.log(data)

  if (data && data.length > 0) {
    if ("RISKYPLAYSPERCENT" in data[0]) {
      console.log("Query 2 Activated");
      return (
      <div>
        <h1>Query Results</h1>
        <Graph2 data={data} />
      </div>
    );
    }
  }

  return (
    <div>
      <h1>Query Results</h1>
      {data ? <LineChart width={800} height={400} data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
    <CartesianGrid strokeDasharray="3 3" />
    <XAxis dataKey="YEAR" />
    <YAxis />
    <Tooltip />
    <Legend />
    <Line type="monotone" dataKey="POPULARITY" stroke="#8884d8" activeDot={{ r: 8 }} />
  </LineChart> : <p>No data available.</p>}
    </div>
  );
};

export default QueryResults;