import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import Graph2 from './Graphs';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const formatYAxisTick = (tick) => {
  return tick.toFixed(2);
};

const ResultsChart = ({ data, openingMoves, openingName, dataChoice, graphBy }) => {

  console.log("Query Results Data:")
  console.log(data, openingMoves)
  console.log("Data received for chart:", data);
  const elo_colors = ['#FF5733', '#33FF57', '#5733FF'];
  const uniqueColors = [
  '#0792db', '#FFC300', '#DAF7A6', '#5733FF', '#FF5733', '#900C3F', '#F4D03F', '#9B59B6', '#2980B9', '#008B8B',
  '#e959c9', '#4CAF50', '#FFA07A', '#FF69B4', '#FF5733', '#FF5733', '#DAF7A6', '#F5FFFA', '#009ACD', '#34495E',
  '#DD5713', '#DAF7A6', '#33FF57', '#C70039', '#005F5E', '#FF5733', '#F0FFFF', '#9B59B6', '#00E5EE', '#5733FF',
];
  const compare_data = data;

  const transformedData = data.map((entry) => ({
    ...entry,
    month: entry.MONTH,
    year: entry.YEAR,  // Ensure you have proper key for year, month, or quarter
    monthYear: `${entry.YEAR}-${entry.MONTH}`,
    popularity: parseFloat(entry.POPULARITY),
    proportion: parseFloat(entry.PROPORTION),
    winrate: parseFloat(entry.WINRATE),
    avgturns: parseFloat(entry.AVERAGENUMBEROFTURNS),
    elogroup: entry.ELOGROUP,
    ecocode: entry.ECOCODE,
    rank: entry.RANK
}));
  const x_key = compare_data[0].hasOwnProperty("MONTH") ? 'monthYear' : 'year';
  const y_key = compare_data[0].hasOwnProperty("RANK") ? [1, 4] : ['auto', 'auto']

  const elo_groups = [...new Set(transformedData.map(entry => entry.elogroup))];
  const eco_codes = [...new Set(transformedData.map(entry => entry.ecocode))];
  // Decide on the key for the XAxis based on graphBy

  return (
    <div>
      <h2>{dataChoice === 'winrate' ? 'Winrate' : (dataChoice === 'popularity' ? 'Popularity' : 'Proportion')} of {openingMoves}</h2>
      <h3>{openingName}</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={transformedData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={x_key} allowDuplicatedCategory={false} />
          <YAxis domain={y_key} tickFormatter={formatYAxisTick} reversed={"RANK" in compare_data[0]}/>
          <Tooltip />
          <Legend payload={[
            { value: dataChoice === 'winrate' ? 'Winrate' : (dataChoice === 'popularity' ? 'Popularity' : 'Proportion'), type: 'line', id: dataChoice, color: dataChoice === 'winrate' ? '#82ca9d' : '#8884d8' }
          ]} />

          {dataChoice === 'popularity' && <Line type="monotone" dataKey="popularity" stroke="#8884d8" activeDot={{ r: 8 }} />}
          {dataChoice === 'winrate' && <Line type="monotone" dataKey="winrate" stroke="#82ca9d" />}
          {!dataChoice && <Line type = "monotone" dataKey = "popularity" stroke="#8884d8" activeDot={{ r: 8 }} />}
          {!dataChoice && <Line type = "monotone" dataKey = "proportion" stroke="#8884d8" />}
          {elo_groups.map((eloGroup, index) => (<Line key={index} type="monotone" dataKey='avgturns' data={transformedData.filter(entry => entry.elogroup === eloGroup)} stroke={elo_colors[index % elo_colors.length]} activeDot={{ r: 8 }} name={eloGroup}/>))}
          {eco_codes.map((ecoCode, index) => (<Line key={index} type="monotone" dataKey='rank' data={transformedData.filter(entry => entry.ecocode === ecoCode)} stroke={uniqueColors[index % uniqueColors.length]} name={ecoCode}/>))}


        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

const QueryResults = () => {
  const location = useLocation();
  const {data, openingMoves, openingName, dataChoice, graphBy} = location.state || {
    data: null,
    openingMoves: '',
    openingName: '',
    dataChoice: '',
    graphBy: 'year'
  };
  console.log("Query Results Data:")
  console.log(data, openingMoves)

  if (data && data.length > 0) {
    return (
        <div>
          <h1>Query Results</h1>
          <ResultsChart data={data} openingMoves={openingMoves} openingName={openingName} dataChoice={dataChoice}
                        graphBy={graphBy}/>
        </div>
    );
  }
};

export default QueryResults;