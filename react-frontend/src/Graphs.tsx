import React, { useEffect } from 'react';
import Chart from 'chart.js/auto';

const Graph2 = ({ data }) => {
    useEffect(() => {
        if (!data || data.length === 0) {
          console.error("No data provided to Graph2 function");
          return;
        }

        const ctx = document.getElementById('data');
        const newChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.map(row => (row.MONTH, row.YEAR)),
                datasets: [{
                    label: 'Percentage of Risky Openings',
                    data: data.map(row => row.RISKYPLAYSPERCENT),
                    backgroundColor: 'rgba(54, 162, 235, 0.6)', // Example color
                    borderColor: 'rgba(54, 162, 235, 1)', // Example border color
                    borderWidth: 3
                }]
            },
        });
        return () => {
          newChart.destroy()
        }
    }, [data]);

    return <canvas id="data" />;
};

export default Graph2;