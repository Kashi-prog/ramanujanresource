import React, { useState, useEffect } from 'react';
import { getEmissionStats, getEmissionTimeline, getInsights, markRecommendationRead } from '../services/api';
import CarbonMeter from '../components/CarbonMeter';
import EmissionCharts from '../components/EmissionCharts';
import RecommendationCards from '../components/RecommendationCards';
import './Dashboard.css';

const Dashboard = ({ userId }) => {
  const [stats, setStats] = useState(null);
  const [timeline, setTimeline] = useState([]);
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [period, setPeriod] = useState(30);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const [statsData, timelineData, insightsData] = await Promise.all([
        getEmissionStats(userId, period),
        getEmissionTimeline(userId, period),
        getInsights(userId, period)
      ]);

      setStats(statsData);
      setTimeline(timelineData.timeline);
      setInsights(insightsData);
    } catch (err) {
      console.error('Error fetching dashboard data:', err);
      setError('Failed to load dashboard data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();

    // Listen for activity additions
    const handleActivityAdded = () => {
      fetchData();
    };
    
    window.addEventListener('activityAdded', handleActivityAdded);
    return () => window.removeEventListener('activityAdded', handleActivityAdded);
  }, [userId, period]);

  const handleMarkRead = async (recommendationId) => {
    try {
      await markRecommendationRead(recommendationId);
      // Refresh insights to update read status
      const insightsData = await getInsights(userId, period);
      setInsights(insightsData);
    } catch (err) {
      console.error('Error marking recommendation as read:', err);
    }
  };

  const handlePeriodChange = (newPeriod) => {
    setPeriod(newPeriod);
  };

  if (loading) {
    return (
      <div className="dashboard">
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Loading your carbon shadow...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard">
        <div className="error-container">
          <p>{error}</p>
          <button onClick={fetchData}>Retry</button>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="period-selector">
        <button 
          className={period === 7 ? 'active' : ''} 
          onClick={() => handlePeriodChange(7)}
        >
          7 Days
        </button>
        <button 
          className={period === 30 ? 'active' : ''} 
          onClick={() => handlePeriodChange(30)}
        >
          30 Days
        </button>
        <button 
          className={period === 90 ? 'active' : ''} 
          onClick={() => handlePeriodChange(90)}
        >
          90 Days
        </button>
      </div>

      {stats && insights && (
        <>
          <CarbonMeter 
            totalCO2={stats.total_co2_grams} 
            sustainabilityScore={insights.sustainability_score}
          />

          <EmissionCharts stats={stats} timeline={timeline} />

          <RecommendationCards 
            recommendations={insights.recommendations}
            onMarkRead={handleMarkRead}
          />
        </>
      )}

      {stats && stats.total_activities === 0 && (
        <div className="empty-state">
          <h2>🌱 Start Your Journey</h2>
          <p>Begin tracking your digital activities to see your carbon shadow and get personalized recommendations!</p>
          <p className="tip">Tip: Click the "Add Activity" button above to log your first activity.</p>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
