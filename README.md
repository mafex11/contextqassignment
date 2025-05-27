# Global RSS News Scraper

A comprehensive RSS feed news scraper that collects articles from 22+ countries with a modern React frontend and Flask API backend. Features real-time scraping, database storage, and a professional dark-themed web interface.

## 🌟 Features

- **Global Coverage**: 40+ countries across 6 continents
- **Real-time Scraping**: Live log streaming and scraper control
- **Modern UI**: Professional dark theme React frontend
- **Multiple Storage**: SQLite database, CSV, and JSON exports
- **Advanced Filtering**: Search, country, source, and limit filters
- **Statistics Dashboard**: Real-time data visualization
- **API Endpoints**: RESTful Flask API for data access
- **Error Handling**: Comprehensive retry mechanisms and logging
- **Automated Startup**: One-command startup for both frontend and backend

## 📋 Prerequisites

Before running this project, ensure you have the following installed:

### Required Software
- **Python 3.11** - [Download Python](https://www.python.org/downloads/)

## 🚀 Quick Start Guide

### CLI-Only Scraper

1. **Create virtual environment and install dependencies**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

2. **Run the scraper**:
   ```bash
   python src/main.py
   ```

3. **Collect historical data (optional)**:
   ```bash
   python src/historical_scraper.py
   ```
   This will collect news articles from the past 12 months using advanced methods.


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

## 🛠️ Troubleshooting

## 🎯 Bonus Features Implemented

- ✅ **Countries**: 65+ countries (20+ requirement)
- ✅ **RSS Parsing**: Advanced parsing with BeautifulSoup + lxml
- ✅ **Error Handling**: Comprehensive retry mechanisms and fallbacks
- ✅ **Modular Code**: Professional-grade code organization
- ✅ **Data Storage**: Multiple formats (SQLite, CSV, JSON)
- ✅ **Bonus - Database**: ✅ SQLite with advanced features
- ✅ **Bonus - API**: ✅ Complete Flask REST API
- ✅ **Bonus - Language Detection**: ✅ Automatic language identification
- ✅ **Bonus - Scheduling**: ✅ Real-time control (on-demand scheduling)
- ✅ **Extra - Frontend**: 🎁 Professional React web interface
- ✅ **Extra - Real-time Features**: 🎁 Live logging and monitoring

### Common Issues Encountered 

#### 1.Finding RSS Feeds
- **Limited Availability**: Many major news outlets have discontinued or hidden their RSS feeds
- **Country Coverage**: Some countries have limited RSS feed availability from mainstream media
- **Language Barriers**: RSS feeds often only available in local languages
- **Feed Reliability**: Some RSS feeds may become inactive or change URLs without notice
- **Solution**: Current feed list focuses on reliable, actively maintained RSS sources that were verified to work consistently

#### 2.Data Collection Issues
- **Rate Limiting**: Some news sites may block frequent requests
- **Feed Format Variations**: RSS feed structures vary between sources
- **Character Encoding**: Special characters may not display correctly
- **Article Access**: Some feeds only provide partial content

## 🕒 Historical Data Collection

### New Feature: Past Year Data Collection ✅

This project now includes advanced historical data collection to meet the assignment requirement of extracting "at least past one year" of historical data.

#### Methods Implemented:

1. **Wayback Machine Integration**
   - Accesses Internet Archive's Wayback Machine
   - Retrieves historical RSS feed snapshots
   - Covers multiple years of archived data

2. **Archive Page Scraping**
   - Automatically discovers news website archive pages
   - Scrapes historical article links
   - Extracts full article content and metadata

3. **Intelligent Fallbacks**
   - Multiple backup methods for comprehensive coverage
   - Rate limiting to respect server resources
   - Automatic duplicate detection and removal

#### Usage:

**Command Line:**
```bash
# Collect historical data for past 12 months
python src/historical_scraper.py

# Test with shorter timeframe
python test_historical.py
```

**API Endpoint:**
```bash
# Start historical collection via API
curl -X POST http://localhost:5000/api/scraper/historical
```

**Web Interface:**
- Use the scraper control panel
- Monitor progress with real-time logs
- View collected historical articles

#### Features:
- ✅ **12+ Months Coverage**: Collects articles from the past year
- ✅ **Multiple Sources**: Works with all 65+ countries and 80+ sources
- ✅ **Smart Deduplication**: Removes duplicate articles automatically
- ✅ **Progress Tracking**: Real-time logging and progress monitoring
- ✅ **Database Integration**: Seamlessly integrates with existing database
- ✅ **Export Formats**: Saves in JSON, CSV, and SQLite formats

