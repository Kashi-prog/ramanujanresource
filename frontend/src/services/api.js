import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Users
export const getCurrentUser = async (userId) => {
  const response = await api.get(`/users/${userId}`);
  return response.data;
};

export const createUser = async (userData) => {
  const response = await api.post('/users/', userData);
  return response.data;
};

// Activities
export const createActivity = async (userId, activityData) => {
  const response = await api.post(`/activities/?user_id=${userId}`, activityData);
  return response.data;
};

export const getActivities = async (userId, days = 30) => {
  const response = await api.get(`/activities/?user_id=${userId}&days=${days}`);
  return response.data;
};

export const getActivity = async (activityId) => {
  const response = await api.get(`/activities/${activityId}`);
  return response.data;
};

export const deleteActivity = async (activityId) => {
  const response = await api.delete(`/activities/${activityId}`);
  return response.data;
};

// Emissions
export const getEmissionStats = async (userId, days = 30) => {
  const response = await api.get(`/emissions/stats?user_id=${userId}&days=${days}`);
  return response.data;
};

export const getEmissionTimeline = async (userId, days = 30) => {
  const response = await api.get(`/emissions/timeline?user_id=${userId}&days=${days}`);
  return response.data;
};

export const getEmissionComparison = async (userId) => {
  const response = await api.get(`/emissions/comparison?user_id=${userId}`);
  return response.data;
};

// Insights
export const getInsights = async (userId, days = 30) => {
  const response = await api.get(`/insights/?user_id=${userId}&days=${days}`);
  return response.data;
};

export const getRecommendations = async (userId, unreadOnly = false) => {
  const response = await api.get(`/insights/recommendations?user_id=${userId}&unread_only=${unreadOnly}`);
  return response.data;
};

export const markRecommendationRead = async (recommendationId) => {
  const response = await api.put(`/insights/recommendations/${recommendationId}/read`);
  return response.data;
};

export const getDailyTips = async () => {
  const response = await api.get('/insights/tips');
  return response.data;
};

export default api;
