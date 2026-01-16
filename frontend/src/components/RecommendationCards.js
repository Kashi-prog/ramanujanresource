import React from 'react';
import './RecommendationCards.css';

const RecommendationCards = ({ recommendations, onMarkRead }) => {
  const getCategoryIcon = (category) => {
    const icons = {
      streaming: '🎬',
      browsing: '🌐',
      cloud: '☁️',
      ai_query: '🤖',
      general: '💡'
    };
    return icons[category] || '💡';
  };

  const getCategoryColor = (category) => {
    const colors = {
      streaming: '#667eea',
      browsing: '#4facfe',
      cloud: '#43e97b',
      ai_query: '#f093fb',
      general: '#764ba2'
    };
    return colors[category] || '#667eea';
  };

  if (!recommendations || recommendations.length === 0) {
    return (
      <div className="recommendations-container">
        <h3>Personalized Recommendations</h3>
        <div className="no-recommendations">
          Start logging activities to receive personalized recommendations! 🌱
        </div>
      </div>
    );
  }

  return (
    <div className="recommendations-container">
      <h3>Personalized Recommendations</h3>
      <div className="recommendations-grid">
        {recommendations.slice(0, 6).map((rec) => (
          <div 
            key={rec.id} 
            className={`recommendation-card ${rec.is_read ? 'read' : 'unread'}`}
            style={{ borderLeftColor: getCategoryColor(rec.category) }}
          >
            <div className="rec-header">
              <span className="rec-icon">{getCategoryIcon(rec.category)}</span>
              <span 
                className="rec-category" 
                style={{ color: getCategoryColor(rec.category) }}
              >
                {rec.category.replace('_', ' ').toUpperCase()}
              </span>
              {!rec.is_read && <span className="new-badge">NEW</span>}
            </div>
            <p className="rec-text">{rec.recommendation_text}</p>
            <div className="rec-footer">
              <span className="savings">
                💚 Save up to {(rec.potential_savings_gco2 / 1000).toFixed(2)} kg CO₂
              </span>
              {!rec.is_read && onMarkRead && (
                <button 
                  className="mark-read-btn"
                  onClick={() => onMarkRead(rec.id)}
                >
                  ✓
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RecommendationCards;
