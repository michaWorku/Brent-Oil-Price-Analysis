// Displays a line chart of the preprocessed log returns.
import React from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer, ReferenceLine } from 'recharts';

const ReturnsChart = ({ data, changePointDate }) => {
  const chartData = data.map(d => ({
    date: d.Date,
    logReturns: d.Log_Returns
  }));
  
  const changePointIndex = chartData?.findIndex(item => item.date === changePointDate);

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 h-96">
      <h2 className="text-2xl font-semibold text-gray-800 mb-4">Daily Log Returns</h2>
      <ResponsiveContainer width="100%" height="80%">
        <LineChart data={chartData} margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="date" 
            tick={{ fontSize: 10 }} 
            angle={-45} 
            textAnchor="end" 
            height={60}
            tickFormatter={(tick) => new Date(tick).getFullYear()}
          />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="logReturns" stroke="#10b981" dot={false} />
          {changePointIndex !== -1 && (
            <ReferenceLine 
              x={chartData[changePointIndex]?.date} 
              stroke="#ef4444" 
              strokeDasharray="5 5" 
              label={{ value: 'Change Point', position: 'insideTopRight', fill: '#ef4444' }} 
            />
          )}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ReturnsChart;

