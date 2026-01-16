import React from 'react';
import './CarbonMeter.css';

const CarbonMeter = ({ totalCO2, sustainabilityScore }) => {
  const getScoreColor = (score) => {
    if (score >= 80) return '#48bb78';
    if (score >= 60) return '#ecc94b';
    if (score >= 40) return '#ed8936';
    return '#f56565';
  };

  const getScoreLabel = (score) => {
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good';
    if (score >= 40) return 'Fair';
    return 'Needs Improvement';
  };

  const co2InKg = (totalCO2 / 1000).toFixed(2);
  const scoreColor = getScoreColor(sustainabilityScore);
  const scoreLabel = getScoreLabel(sustainabilityScore);

  return (
    <div className="carbon-meter">
      <div className="meter-section">
        <h3>Total Carbon Emissions</h3>
        <div className="co2-display">
          <span className="co2-value">{co2InKg}</span>
          <span className="co2-unit">kg CO₂</span>
        </div>
        <p className="co2-context">
          {co2InKg < 5 ? '🌱 Great job!' : co2InKg < 15 ? '🌿 Good progress!' : '🌍 Room for improvement'}
        </p>
      </div>

      <div className="meter-section">
        <h3>Sustainability Score</h3>
        <div className="score-display">
          <div className="score-circle" style={{ borderColor: scoreColor }}>
            <span className="score-value" style={{ color: scoreColor }}>
              {sustainabilityScore}
            </span>
          </div>
          <div className="score-label" style={{ color: scoreColor }}>
            {scoreLabel}
          </div>
        </div>
        <div className="score-bar">
          <div 
            className="score-fill" 
            style={{ 
              width: `${sustainabilityScore}%`,
              backgroundColor: scoreColor 
            }}
          ></div>
        </div>
      </div>
    </div>
  );
};

export default CarbonMeter;
