import React, { useState, useEffect } from 'react';
import './App.css';
import Dashboard from './pages/Dashboard';
import ActivityInput from './components/ActivityInput';
import { getCurrentUser } from './services/api';

function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const [showActivityInput, setShowActivityInput] = useState(false);

  useEffect(() => {
    // For demo purposes, we'll use a default user
    // In production, this would involve proper authentication
    const initUser = async () => {
      try {
        const user = await getCurrentUser(1); // Default user ID
        setCurrentUser(user);
      } catch (error) {
        console.error('Failed to load user:', error);
        // Create demo user if needed
        setCurrentUser({ id: 1, username: 'demo_user', email: 'demo@example.com', region: 'Global' });
      }
    };
    initUser();
  }, []);

  const handleActivityAdded = () => {
    setShowActivityInput(false);
    // Trigger dashboard refresh
    window.dispatchEvent(new Event('activityAdded'));
  };

  if (!currentUser) {
    return (
      <div className="App">
        <div className="loading">Loading...</div>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>🌱 Carbon Shadow Tracker</h1>
        <p className="subtitle">Track and reduce your digital carbon footprint</p>
      </header>
      
      <main className="App-main">
        <div className="user-info">
          <span>Welcome, {currentUser.username}</span>
          <span className="region">Region: {currentUser.region}</span>
        </div>

        <button 
          className="add-activity-btn"
          onClick={() => setShowActivityInput(!showActivityInput)}
        >
          {showActivityInput ? '− Close' : '+ Add Activity'}
        </button>

        {showActivityInput && (
          <ActivityInput 
            userId={currentUser.id} 
            onActivityAdded={handleActivityAdded}
          />
        )}

        <Dashboard userId={currentUser.id} />
      </main>

      <footer className="App-footer">
        <p>Every digital action has a carbon shadow. Make it lighter. 🌍</p>
      </footer>
    </div>
  );
}

export default App;
