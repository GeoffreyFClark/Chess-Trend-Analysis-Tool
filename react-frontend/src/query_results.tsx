import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import Graph2 from './Graphs';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const formatYAxisTick = (tick) => {
  return tick.toFixed(2);
};

const ResultsChart = ({ data, openingMoves, openingName, dataChoice, graphBy }) => {
  console.log("Data received for chart:", data);

  const transformedData = data.map((entry) => ({
    ...entry,
    year: entry.YEAR,  // Ensure you have proper key for year, month, or quarter
    popularity: parseFloat(entry.POPULARITY),
    winrate: parseFloat(entry.WINRATE),
  }));

  // Decide on the key for the XAxis based on graphBy
  
  return (
    <div>
      <h2>{dataChoice === 'winrate' ? 'Winrate' : 'Popularity'} of {openingMoves}</h2>
      <h3>{openingName}</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={transformedData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={'year'} />  
            {/* 
            Fix key to get year+month. https://recharts.org/en-US/api/XAxis#type
            e.g. Try  { date: "20210103", category: "b", value: 1000 },
            ].map(row => ({ ...row, ts: moment(row.date, "YYYYMMDD").valueOf() }));   
            tickFormatter={(unixTimestamp) => moment(unixTimestamp).format("YYYY-MM")}
            */}
          <YAxis domain={['auto', 'auto']} tickFormatter={formatYAxisTick} />
          <Tooltip />
          <Legend payload={[
            { value: dataChoice === 'winrate' ? 'Winrate' : 'Popularity', type: 'line', id: dataChoice, color: dataChoice === 'winrate' ? '#82ca9d' : '#8884d8' }
          ]} />
          {dataChoice === 'popularity' && <Line type="monotone" dataKey="popularity" stroke="#8884d8" activeDot={{ r: 8 }} />}
          {dataChoice === 'winrate' && <Line type="monotone" dataKey="winrate" stroke="#82ca9d" />}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

const QueryResults = () => {
  const location = useLocation();
  const { data, openingMoves, openingName, dataChoice, graphBy } = location.state || { data: null, openingMoves: '', openingName: '', dataChoice: '', graphBy: 'year' };
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
    else {
      return (
        <div>
          <h1>Query Results</h1>
          <ResultsChart data={data} openingMoves={openingMoves} openingName={openingName} dataChoice={dataChoice} graphBy={graphBy} />
        </div>
      );
    }
  }
};

export default QueryResults;
