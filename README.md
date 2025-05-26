# Global RSS News Scraper

A comprehensive RSS feed news scraper that collects articles from 22+ countries with a modern React frontend and Flask API backend. Features real-time scraping, database storage, and a professional dark-themed web interface.

## 🌟 Features

- **Global Coverage**: 22+ countries across 6 continents
- **Real-time Scraping**: Live log streaming and scraper control
- **Modern UI**: Professional dark theme React frontend
- **Multiple Storage**: SQLite database, CSV, and JSON exports
- **Advanced Filtering**: Search, country, source, and limit filters
- **Statistics Dashboard**: Real-time data visualization
- **API Endpoints**: RESTful Flask API for data access
- **Error Handling**: Comprehensive retry mechanisms and logging

## 📋 Prerequisites

Before running this project, ensure you have the following installed:

### Required Software
- **Python 3.11** - [Download Python](https://www.python.org/downloads/)
- **Node.js 14+** - [Download Node.js](https://nodejs.org/)
- **npm** (comes with Node.js)

### Verify Installation
```bash
python --version    # Should show Python 3.8+
node --version      # Should show Node.js 14+
npm --version       # Should show npm 6+
```

## 🚀 Quick Start Guide

### ONLY SCRAPER RUN
### Step 1: just create an venv and do pip install-r requirements.txt
then from the root directory run python src/main.py
you'll see the logs and everything.

### FULL STACK APPROACH
### Step 1: Clone/Download the Project
```bash
# If using Git
git clone <repository-url>
cd contextqassignment

# Or download and extract the ZIP file
```

### Step 2: Backend Setup (Python/Flask)

1. **Navigate to project root**:
   ```bash
   cd contextqassignment
   ```

2. **Install Python dependencies**:
   ```bash
   python -m venv venv
   source venv/scripts/activate
   pip install -r requirements.txt
   ```

3. **Verify backend works**:
   ```bash
   cd src
   python main.py
   ```
   This should start scraping RSS feeds and show progress.

### Step 3: Frontend Setup (React)

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

3. **Verify frontend builds**:
   ```bash
   npm run build
   ```

### Step 4: Run the Complete Application

#### Option A: Run Both Services Manually

**Terminal 1 - Start Backend API**:
```bash
stay in the root directory
python api.py
```
The API will start on `http://localhost:5000`

**Terminal 2 - Start Frontend**:
```bash
cd frontend
npm start
```
The frontend will start on `http://localhost:3000`

### Step 5: Access the Application

Open your web browser and go to:
```
http://localhost:3000
```

## 📖 Detailed Usage Instructions

### Initial Data Collection

1. **First Run**: Click the "Scraper" button in the top-right corner
2. **Start Scraping**: Click "Start Scraper" to begin collecting news
3. **Monitor Progress**: Watch real-time logs as articles are collected
4. **View Results**: Browse collected articles in the main interface

### Using the Interface

#### Main Dashboard
- **Browse Articles**: Scroll through news cards with summaries
- **Filter Content**: Use search, country, source, and limit filters
- **View Statistics**: Click "Stats" to see collection metrics
- **Pagination**: Navigate through multiple pages of articles

#### Scraper Control
- **Start/Stop**: Control scraper execution in real-time
- **Live Logs**: Monitor scraping progress with timestamped logs
- **Status Monitoring**: View current status, duration, and last run time

#### Data Export
Articles are automatically saved in multiple formats:
- **Database**: SQLite file at `data/news.db`
- **JSON**: Timestamped files in `data/` directory
- **CSV**: Timestamped files in `data/` directory

## 🔧 Configuration

### RSS Feed Sources
Edit `src/config.py` to modify RSS feeds:
```python
RSS_FEEDS = {
    'Country Name': [
        {
            'name': 'Source Name',
            'url': 'https://example.com/rss.xml',
            'language': 'en'  # optional
        }
    ]
}
```

### API Settings
Modify API settings in `src/config.py`:
```python
REQUEST_DELAY = 2      # Seconds between requests
MAX_RETRIES = 3        # Retry attempts for failed requests
UPDATE_INTERVAL = 24   # Hours between automatic updates
```

## 📁 Project Structure

```
contextqassignment/
├── src/                    # Backend Python code
│   ├── main.py            # Main scraper script
│   ├── api.py             # Flask API server
│   ├── scraper.py         # RSS scraping logic
│   ├── database.py        # Database operations
│   └── config.py          # Configuration settings
├── frontend/              # React frontend
│   ├── src/
│   │   ├── App.js         # Main React component
│   │   └── index.css      # Styling
│   ├── public/            # Static files
│   └── package.json       # Node.js dependencies
├── data/                  # Generated data files
│   ├── news.db           # SQLite database
│   ├── articles_*.json   # JSON exports
│   └── articles_*.csv    # CSV exports
├── requirements.txt       # Python dependencies
├── package.json          # Root npm scripts
└── README.md             # This file
```

## 🛠️ Troubleshooting

### Common Issues

#### Backend Issues
```bash
# If Python packages fail to install
pip install --upgrade pip
pip install -r requirements.txt

# If lxml fails to install (Windows)
pip install lxml

# If database errors occur
rm data/news.db  # Delete and recreate database
```

#### Frontend Issues
```bash
# If npm install fails
rm -rf node_modules package-lock.json
npm install

# If build fails
npm run build

# If port 3000 is busy
# The app will automatically use the next available port
```

#### Network Issues
- **Firewall**: Ensure ports 3000 and 5000 are not blocked
- **Antivirus**: Some antivirus software may block the scraper
- **Proxy**: Configure proxy settings if behind corporate firewall

### Performance Tips

1. **Large Datasets**: Increase database limit in filters for better performance
2. **Memory Usage**: Restart scraper periodically for long-running sessions
3. **Network Speed**: Adjust `REQUEST_DELAY` in config for slower connections

## 📊 API Endpoints

The Flask API provides the following endpoints:

### News Data
- `GET /api/news` - Get articles with optional filters
- `GET /api/news/stats` - Get collection statistics
- `GET /api/news/countries` - Get available countries
- `GET /api/news/sources` - Get available sources

### Scraper Control
- `POST /api/scraper/start` - Start the scraper
- `POST /api/scraper/stop` - Stop the scraper
- `GET /api/scraper/status` - Get scraper status
- `GET /api/scraper/logs` - Get scraper logs

### Example API Usage
```bash
# Get latest 50 articles
curl http://localhost:5000/api/news?limit=50

# Get articles from specific country
curl http://localhost:5000/api/news?country=United%20States

# Start scraper
curl -X POST http://localhost:5000/api/scraper/start
```

## 🎯 Assignment Compliance

This project exceeds all assignment requirements:

- ✅ **20+ Countries**: Covers 22 countries (110% of requirement)
- ✅ **RSS Parsing**: Uses BeautifulSoup + lxml for robust parsing
- ✅ **Error Handling**: Comprehensive retry mechanisms and fallbacks
- ✅ **Modular Code**: Well-organized classes and functions
- ✅ **Data Storage**: Multiple formats (CSV, JSON, SQLite)
- ✅ **Advanced Features**: 
  - Database storage with duplicate handling
  - Flask API with CORS support
  - Language detection for articles
  - Real-time scraper control
  - Modern React frontend
  - Professional dark theme UI

## 🔄 Maintenance

### Regular Tasks
1. **Update RSS Feeds**: Check and update feed URLs in `config.py`
2. **Database Cleanup**: Periodically clean old articles if needed
3. **Log Management**: Clear old log files from `data/` directory
4. **Dependency Updates**: Update Python and Node.js packages

### Backup
Important files to backup:
- `data/news.db` - Main database
- `src/config.py` - RSS feed configuration
- `data/articles_*.json` - Exported data files

## 📞 Support

If you encounter any issues:

1. **Check Prerequisites**: Ensure Python 3.8+ and Node.js 14+ are installed
2. **Review Logs**: Check console output for error messages
3. **Verify Ports**: Ensure ports 3000 and 5000 are available
4. **Check Network**: Verify internet connection for RSS feeds
5. **Restart Services**: Stop and restart both backend and frontend

## 🏆 Success Metrics

After successful setup, you should see:
- ✅ Backend API running on port 5000
- ✅ Frontend interface on port 3000
- ✅ Articles being collected from 22+ countries
- ✅ Real-time logs during scraping
- ✅ Data saved in multiple formats
- ✅ Responsive dark theme interface

---

**Happy News Scraping! 🌍📰** 