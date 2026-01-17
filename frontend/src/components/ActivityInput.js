import React, { useState } from 'react';
import { createActivity } from '../services/api';
import './ActivityInput.css';

const ActivityInput = ({ userId, onActivityAdded }) => {
  const [formData, setFormData] = useState({
    activity_type: 'streaming',
    duration_minutes: '',
    data_volume_mb: '',
    device_type: 'laptop'
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess(false);

    try {
      const data = {
        ...formData,
        duration_minutes: parseFloat(formData.duration_minutes),
        data_volume_mb: parseFloat(formData.data_volume_mb || 0)
      };

      await createActivity(userId, data);
      setSuccess(true);
      setFormData({
        activity_type: 'streaming',
        duration_minutes: '',
        data_volume_mb: '',
        device_type: 'laptop'
      });

      setTimeout(() => {
        setSuccess(false);
        if (onActivityAdded) {
          onActivityAdded();
        }
      }, 2000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to add activity');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="activity-input-container">
      <h2>Log Digital Activity</h2>
      <form onSubmit={handleSubmit} className="activity-form">
        <div className="form-group">
          <label htmlFor="activity_type">Activity Type</label>
          <select
            id="activity_type"
            name="activity_type"
            value={formData.activity_type}
            onChange={handleChange}
            required
          >
            <option value="streaming">Streaming (Video/Music)</option>
            <option value="browsing">Web Browsing</option>
            <option value="cloud">Cloud Storage/Transfer</option>
            <option value="ai_query">AI Queries</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="duration_minutes">Duration (minutes)</label>
          <input
            type="number"
            id="duration_minutes"
            name="duration_minutes"
            value={formData.duration_minutes}
            onChange={handleChange}
            min="1"
            step="1"
            required
            placeholder="e.g., 60"
          />
        </div>

        <div className="form-group">
          <label htmlFor="data_volume_mb">Data Volume (MB) - Optional</label>
          <input
            type="number"
            id="data_volume_mb"
            name="data_volume_mb"
            value={formData.data_volume_mb}
            onChange={handleChange}
            min="0"
            step="0.1"
            placeholder="e.g., 1500"
          />
        </div>

        <div className="form-group">
          <label htmlFor="device_type">Device Type</label>
          <select
            id="device_type"
            name="device_type"
            value={formData.device_type}
            onChange={handleChange}
            required
          >
            <option value="laptop">Laptop</option>
            <option value="desktop">Desktop</option>
            <option value="mobile">Mobile</option>
          </select>
        </div>

        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">✓ Activity added successfully!</div>}

        <button type="submit" disabled={loading} className="submit-btn">
          {loading ? 'Adding...' : 'Add Activity'}
        </button>
      </form>
    </div>
  );
};

export default ActivityInput;
