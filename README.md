# 🌱 Carbon Shadow Tracker

An AI-powered web application that estimates and visualizes the carbon footprint of users' digital activities. Track your streaming, browsing, cloud storage, and AI usage to understand and reduce your digital carbon shadow.

![Carbon Shadow Tracker](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![React](https://img.shields.io/badge/react-18.2-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)

## 🌍 Overview

Every digital action—from streaming videos to running AI queries—has a carbon footprint. Carbon Shadow Tracker helps you:

- **Track** digital activities across multiple categories
- **Visualize** your carbon emissions with interactive charts
- **Receive** AI-powered recommendations to reduce your footprint
- **Compare** your usage against averages
- **Monitor** trends over time

## ✨ Features

### Activity Tracking
- **Streaming**: Video and music streaming duration and quality
- **Browsing**: Web browsing time and data consumption
- **Cloud Storage**: File uploads, downloads, and storage
- **AI Queries**: AI model usage and computational activities

### Carbon Calculation
- Real-time emission calculations based on activity type, duration, and device
- Regional carbon intensity data for accurate estimates
- Contextual factors (time of day, energy mix)
- Historical trend analysis

### Visualization Dashboard
- Interactive carbon footprint meter
- Daily/weekly/monthly emission timelines
- Activity breakdown by category
- Sustainability scoring system

### AI Recommendations
- Personalized low-carbon alternatives
- Actionable sustainability tips
- Potential savings calculations
- Category-specific insights

## 🏗️ Architecture

```
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # Application entry point
│   │   ├── config.py       # Configuration settings
│   │   ├── routers/        # API endpoints
│   │   │   ├── activities.py
│   │   │   ├── emissions.py
│   │   │   ├── insights.py
│   │   │   └── users.py
│   │   ├── models/         # Pydantic schemas
│   │   ├── database/       # SQLAlchemy models
│   │   ├── ml/            # ML emission estimator
│   │   ├── recommendations/# Recommendation engine
│   │   └── collectors/     # Data collectors
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/    # Reusable components
│   │   ├── pages/         # Dashboard page
│   │   ├── services/      # API client
│   │   └── App.js
│   ├── package.json
│   └── Dockerfile
│
├── docker-compose.yml
├── .env.example
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- **Docker & Docker Compose** (recommended)
- OR **Python 3.11+** and **Node.js 18+**

### Option 1: Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/Kashi-prog/ramanujanresource.git
   cd ramanujanresource
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings (optional)
   ```

3. **Start the application**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Option 2: Local Development

#### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the backend**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

#### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set environment variable**
   ```bash
   export REACT_APP_API_URL=http://localhost:8000/api/v1
   # On Windows: set REACT_APP_API_URL=http://localhost:8000/api/v1
   ```

4. **Start the development server**
   ```bash
   npm start
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/docs

## 📊 Usage Guide

### 1. Create a User (First Time)

The application uses a demo user by default. To create your own user:

```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "yourname",
    "password": "securepassword",
    "region": "US"
  }'
```

### 2. Log Activities

Click "Add Activity" and enter:
- Activity type (streaming, browsing, cloud, AI queries)
- Duration in minutes
- Data volume (optional)
- Device type

### 3. View Dashboard

Monitor your carbon shadow with:
- Real-time emission calculations
- Interactive charts and graphs
- Timeline views (7/30/90 days)

### 4. Get Recommendations

Receive personalized tips to:
- Reduce streaming emissions
- Optimize cloud usage
- Lower browsing impact
- Minimize AI query footprint

## 🔌 API Documentation

### Base URL
```
http://localhost:8000/api/v1
```

### Key Endpoints

#### Activities
- `POST /activities/` - Create activity
- `GET /activities/` - List activities
- `GET /activities/{id}` - Get specific activity
- `DELETE /activities/{id}` - Delete activity

#### Emissions
- `GET /emissions/stats` - Get emission statistics
- `GET /emissions/timeline` - Get daily timeline
- `GET /emissions/comparison` - Compare with averages

#### Insights
- `GET /insights/` - Get comprehensive insights
- `GET /insights/recommendations` - List recommendations
- `GET /insights/tips` - Get daily tips

#### Users
- `POST /users/` - Create user
- `GET /users/{id}` - Get user
- `PUT /users/{id}/region` - Update region

Full interactive API documentation available at: http://localhost:8000/docs

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🌐 Deployment

### Production Deployment

1. **Update environment variables**
   ```bash
   # Generate a strong secret key
   SECRET_KEY=$(openssl rand -hex 32)
   
   # Update .env file
   DATABASE_URL=postgresql://user:pass@host:5432/dbname
   SECRET_KEY=$SECRET_KEY
   CORS_ORIGINS=https://yourdomain.com
   ```

2. **Deploy with Docker**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Use a production database** (PostgreSQL recommended)
   ```bash
   # Update requirements.txt
   echo "psycopg2-binary==2.9.9" >> backend/requirements.txt
   
   # Update DATABASE_URL in .env
   DATABASE_URL=postgresql://user:pass@host:5432/carbon_tracker
   ```

### Cloud Deployment Options

- **AWS**: ECS with RDS PostgreSQL
- **Google Cloud**: Cloud Run with Cloud SQL
- **Azure**: App Service with Azure Database
- **Heroku**: Simple deployment with Heroku Postgres

## 🔧 Configuration

### Backend Configuration (backend/app/config.py)

```python
DATABASE_URL: Database connection string
SECRET_KEY: JWT secret key
CORS_ORIGINS: Allowed frontend origins
DEFAULT_CARBON_INTENSITY: Global average gCO2/kWh
```

### Frontend Configuration

```bash
REACT_APP_API_URL: Backend API URL
```

## 📈 Carbon Calculation Methodology

### Energy Factors

Activity energy consumption is calculated based on:

- **Device type**: Laptop, desktop, or mobile
- **Activity type**: Streaming, browsing, cloud, AI
- **Duration**: Minutes of activity
- **Data volume**: MB transferred (for cloud activities)

### Carbon Intensity

Regional carbon intensity values (gCO2/kWh):

- Global: 475
- Nordic: 85 (cleanest)
- Europe: 295
- US: 385
- Asia: 550
- Australia: 650 (highest)

### Contextual Adjustments

- **Night time (10 PM - 6 AM)**: 10% reduction
- **Peak hours (5 PM - 9 PM)**: 5% increase
- Based on grid energy mix patterns

## 🤝 Contributing

We welcome contributions! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint configuration for JavaScript
- Write tests for new features
- Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Carbon intensity data inspired by [Electricity Maps](https://app.electricitymaps.com/)
- Energy consumption estimates based on research from:
  - The Shift Project
  - Carbon Trust
  - Green Software Foundation

## 📧 Contact

For questions or feedback:
- Create an issue on GitHub
- Email: support@carbonshadowtracker.com (placeholder)

## 🗺️ Roadmap

- [ ] Browser extension for automatic tracking
- [ ] Mobile app (iOS/Android)
- [ ] Integration with real-time carbon intensity APIs
- [ ] Social features and challenges
- [ ] Carbon offset marketplace integration
- [ ] Advanced ML models for prediction
- [ ] Multi-language support

---

**Made with 💚 for a sustainable digital future**

*Every click counts. Make it carbon-conscious.* 🌍
