import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, Label } from 'recharts';



const ResultsChart = ({ data, openingMoves, openingName, dataChoice, graphBy, YaxisLabel, queryNumber }) => {
  const elo_colors = ['#00B4FD', 'red', '#0EE86B'];
  const uniqueColors = [
    '#6A5ACD', 
    '#20B2AA', 
    '#4682B4', 
    '#008080', 
    '#40E0D0', 
    '#FF6347', 
    '#D2691E', 
    '#6495ED', 
    '#FF7F50', 
    '#DC143C', 
    '#00BFFF', 
    '#F08080', 
    '#FA8072', 
    '#E9967A', 
    '#FFA07A', 
    '#B0C4DE', 
    '#778899', 
    '#2E8B57', 
    '#3CB371', 
    '#48D1CC', 
    '#C71585', 
    '#DB7093', 
    '#6B8E23', 
    '#556B2F', 
    '#8FBC8F', 
    '#BDB76B', 
    '#9ACD32', 
    '#32CD32', 
    '#66CDAA', 
    '#00CED1'  
  ];

  const chessOpenings = {
    "B44": "Sicilian Defense: Szen Variation",
    "B48": "Sicilian Defense: Taimanov Variation",
    "E97": "King's Indian Defense: Orthodox Variation",
    "B02": "Alekhine's Defense: Scandinavian Variation",
    "E92": "King's Indian Defense: Gligoric-Taimanov System",
    "B42": "Sicilian Defense: Kan Variation",
    "B80": "Sicilian Defense: Scheveningen Variation",
    "B52": "Sicilian Defense: Canal-Sokolsky Attack",
    "B85": "Sicilian Defense: Scheveningen Variation, Classical",
    "B83": "Sicilian Defense: Scheveningen, 6.Be2",
    "B33": "Sicilian Defense: Sveshnikov Variation",
    "B51": "Sicilian Defense: Canal-Sokolsky (Najdorf) Variation",
    "E12": "Queen's Indian Defense",
    "E15": "Queen's Indian Defense: Fianchetto Variation",
    "E11": "Bogo-Indian Defense",
    "E94": "King's Indian Defense: Orthodox Variation",
    "A45": "Trompowsky Attack",
    "B90": "Sicilian Defense: Najdorf Variation",
    "B30": "Sicilian Defense",
    "B31": "Sicilian Defense: Nyezhmetdinov-Rossolimo Attack",
    "D45": "Semi-Slav Defense",
    "B23": "Sicilian Defense: Closed",
    "B43": "Sicilian Defense: Kan Variation, 5.Nc3",
    "D35": "Queen's Gambit Declined: Exchange Variation"
  }

  const formatYAxisTick = (tick) => {
    if (queryNumber === 1) {
      return tick.toFixed(2);
    }
    if (queryNumber === 2) {
      return tick.toFixed(2);
    }
    if (queryNumber === 3) {
      return tick.toFixed(2);
    }
    if (queryNumber === 4) {
      return tick.toFixed(0);
    }
    if (queryNumber === 5) {
      return tick.toFixed(0);
    }
    else {
      return tick.toFixed(2);
    }
  };

  const tooltipFormatter = (value, name, props) => {
    // 'name' should correspond to the ECOCODE, which we will map to the full name
    return [value, chessOpenings[name] || name];
  };

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
    YaxisLabel: entry.YaxisLabel,
    ecocode: entry.ECOCODE,
    OpeningName: chessOpenings[entry.ECOCODE] || entry.ECOCODE,
    rank: entry.RANK,
    queryNumber: entry.QUERYNUMBER,
  }));

  const x_key = compare_data[0].hasOwnProperty("MONTH") ? 'monthYear' : 'year';
  const y_key = queryNumber === 5 ? [0.8, 3.2] : ['auto', 'auto'];
  const yTicks = queryNumber === 5 ? [1, 2, 3] : undefined;

  const elo_groups = [...new Set(transformedData.map(entry => entry.elogroup))];
  const eco_codes = [...new Set(transformedData.map(entry => entry.ecocode))];
  

  let legendPayload = [
    { value: dataChoice === 'winrate' ? 'Winrate' : (dataChoice === 'popularity' ? 'Popularity' : 'Proportion'), type: 'line', id: dataChoice, color: '#00B4FD'}
  ];
  if (queryNumber === 1) {
    legendPayload = [{ value: 'Popularity %', type: 'line', id: 'popularity', color: '#00B4FD' }];
  }
  if (queryNumber === 2) {
    legendPayload = [{ value: 'Popularity %', type: 'line', id: 'popularity', color: '#00B4FD' }];
  }
  if (queryNumber === 3) {
    legendPayload = [{ value: 'Predictive Power', type: 'line', id: 'proportion', color: '#00B4FD' }];
  }
  if (queryNumber === 4) {
    legendPayload = [
      { value: 'WithinStdDevPair', type: 'line', id: '1', color: '#00B4FD' },
      { value: 'AboveStdDevPair', type: 'line', id: '2', color: 'red' },
      { value: 'BelowStdDevPair', type: 'line', id: '3', color: '#0EE86B' }
    ];
  }
  if (queryNumber === 5) {
    legendPayload = eco_codes.map((ecoCode, index) => ({
      value: chessOpenings[ecoCode] || ecoCode, // Use the mapped name or ECOCODE as fallback
      type: 'line',
      id: ecoCode,
      color: uniqueColors[index % uniqueColors.length], // Cycle through colors
    }));
  }
  

  return (
    <div style={{height: '75vh', marginLeft: '10px'}} >
      <div style={{ width: '100%', textAlign: 'center' }}>
        {dataChoice === 'popularity' && <h2 style={{ margin: '0.5em 0', fontSize: '40px' }}>Popularity of {openingMoves} over Time</h2>}
        {dataChoice === 'winrate' && <h2 style={{ margin: '0.5em 0', fontSize: '40px' }}>Winrate of {openingMoves} over Time</h2>}
        {queryNumber === 1 && <h2 style={{ margin: '0.5em 0', fontSize: '40px' }}>Prominence of {openingMoves} over Time</h2>}
        {queryNumber === 2 && <h2 style={{ margin: '0.5em 0', fontSize: '40px' }}>Risky Openings</h2>}
        {queryNumber === 3 && <h2 style={{ margin: '0.5em 0', fontSize: '40px' }}>Result Predictions based on Elo</h2>}
        {queryNumber === 4 && <h2 style={{ margin: '0.5em 0', fontSize: '35px' }}>Average Number of Turns between Evenly Matched Players over Time</h2>}
        {queryNumber === 5 && <h2 style={{ margin: '0.5em 0', fontSize: '40px' }}>3 Most Popular Openings through Time</h2>}
      </div>
      {/* <h2>{dataChoice === 'winrate' ? 'Winrate' : (dataChoice === 'popularity' ? 'Popularity' : 'Proportion')} of {openingMoves}</h2>
      <h3>{openingName}</h3> */}
      <ResponsiveContainer  width="100%">
        <LineChart data={transformedData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }} >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={x_key} allowDuplicatedCategory={false} />
          <YAxis domain={y_key} tickFormatter={formatYAxisTick} ticks={yTicks} reversed={"RANK" in compare_data[0]}>
            <Label
              value={YaxisLabel}
              angle={-90}
              position="insideLeft"
              offset={-10}
              style={{ textAnchor: 'middle' }}
              fontSize={30}
            />
          </YAxis>
          <Tooltip formatter={tooltipFormatter} />
          <Legend payload={legendPayload} />
          {dataChoice === 'popularity' && <Line type="monotone" dataKey="popularity" stroke="#00B4FD" strokeWidth={4} activeDot={{ r: 8 }} />}
          {dataChoice === 'winrate' && <Line type="monotone" dataKey="winrate" stroke="#00B4FD" strokeWidth={4}/>}
          {queryNumber === 1 && <Line type = "monotone" dataKey = "popularity" stroke="#00B4FD" strokeWidth={4} activeDot={{ r: 8 }} />}
          {queryNumber === 2 && <Line type = "monotone" dataKey = "popularity" stroke="#00B4FD" strokeWidth={4} activeDot={{ r: 8 }} />}
          {queryNumber === 3 && <Line type = "monotone" dataKey = "proportion" stroke="#00B4FD" strokeWidth={4}/>}
          {queryNumber === 4 && elo_groups.map((eloGroup, index) => (<Line key={index} type="monotone" dataKey='avgturns' data={transformedData.filter(entry => entry.elogroup === eloGroup)} stroke={elo_colors[index % elo_colors.length]} strokeWidth={4} activeDot={{ r: 8 }} name={eloGroup} />))}
          {queryNumber === 5 && eco_codes.map((ecoCode, index) => (<Line key={index} type="monotone" dataKey='rank' data={transformedData.filter(entry => entry.ecocode === ecoCode)} stroke={uniqueColors[index % uniqueColors.length]} name={ecoCode} strokeWidth={4}/>))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

const QueryResults = () => {
  const location = useLocation();
  const {data, openingMoves, openingName, dataChoice, graphBy, YaxisLabel, queryNumber} = location.state || {
    data: null,
    openingMoves: '',
    openingName: '',
    dataChoice: '',
    graphBy: 'year',
    YaxisNumber: 'Data',
    queryNumber: 0
  };

  if (data && data.length > 0) {
    return (
        <div>
          <ResultsChart data={data} openingMoves={openingMoves} openingName={openingName} dataChoice={dataChoice}
                        graphBy={graphBy} YaxisLabel={YaxisLabel} queryNumber={queryNumber} />
        </div>
    );
  }
};

export default QueryResults;