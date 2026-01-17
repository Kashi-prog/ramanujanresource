import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line } from 'recharts';
import './EmissionCharts.css';

const COLORS = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b'];

const EmissionCharts = ({ stats, timeline }) => {
  // Prepare data for pie chart (breakdown by type)
  const pieData = Object.entries(stats.breakdown_by_type || {}).map(([name, value]) => ({
    name: name.replace('_', ' ').toUpperCase(),
    value: parseFloat(value.toFixed(2))
  }));

  // Prepare data for timeline chart
  const timelineData = (timeline || []).map(item => ({
    date: new Date(item.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    co2: parseFloat(item.co2_grams.toFixed(2))
  }));

  return (
    <div className="emission-charts">
      <div className="chart-container">
        <h3>Emissions by Activity Type</h3>
        {pieData.length > 0 ? (
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        ) : (
          <div className="no-data">No activity data yet</div>
        )}
      </div>

      <div className="chart-container">
        <h3>Emissions Over Time</h3>
        {timelineData.length > 0 ? (
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={timelineData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis label={{ value: 'CO₂ (grams)', angle: -90, position: 'insideLeft' }} />
              <Tooltip />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="co2" 
                stroke="#667eea" 
                strokeWidth={3}
                name="CO₂ Emissions"
                dot={{ fill: '#667eea', r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <div className="no-data">No timeline data yet</div>
        )}
      </div>

      <div className="chart-container full-width">
        <h3>Activity Statistics</h3>
        <div className="stats-grid">
          <div className="stat-box">
            <div className="stat-value">{stats.total_activities}</div>
            <div className="stat-label">Total Activities</div>
          </div>
          <div className="stat-box">
            <div className="stat-value">{(stats.total_co2_grams / 1000).toFixed(2)}</div>
            <div className="stat-label">Total CO₂ (kg)</div>
          </div>
          <div className="stat-box">
            <div className="stat-value">{stats.average_co2_per_activity.toFixed(0)}</div>
            <div className="stat-label">Avg CO₂ per Activity (g)</div>
          </div>
          <div className="stat-box">
            <div className="stat-value">{((stats.total_co2_grams / 1000) / 30).toFixed(2)}</div>
            <div className="stat-label">Daily Avg (kg)</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EmissionCharts;
