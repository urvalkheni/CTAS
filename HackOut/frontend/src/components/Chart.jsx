import React from 'react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

const Chart = ({ data, color = '#06b6d4', title }) => (
  <div className="bg-white/30 backdrop-blur-lg rounded-2xl p-4 shadow-lg">
    <h4 className="font-semibold text-lg mb-2 text-blue-700">{title}</h4>
    <ResponsiveContainer width="100%" height={200}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="value" stroke={color} strokeWidth={3} dot={false} />
      </LineChart>
    </ResponsiveContainer>
  </div>
);

export default Chart;