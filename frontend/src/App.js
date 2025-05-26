import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Search, Globe, Calendar, ExternalLink, Filter, BarChart3, Play, RefreshCw, Clock, CheckCircle, XCircle, AlertCircle, Square } from 'lucide-react';
import './App.css';

const API_BASE_URL = 'http://localhost:5000/api';

function App() {
  const [articles, setArticles] = useState([]);
  const [stats, setStats] = useState(null);
  const [countries, setCountries] = useState([]);
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    country: '',
    source: '',
    search: '',
    limit: 50
  });
  const [currentPage, setCurrentPage] = useState(1);
  const [showStats, setShowStats] = useState(false);
  const [showScraper, setShowScraper] = useState(false);
  const [scraperStatus, setScraperStatus] = useState(null);
  const [scraperLogs, setScraperLogs] = useState([]);
  const [logContainer, setLogContainer] = useState(null);

  const itemsPerPage = 12;

  useEffect(() => {
    fetchData();
    fetchStats();
    fetchCountries();
    fetchSources();
    fetchScraperStatus();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    fetchData();
  }, [filters.country, filters.source]); // eslint-disable-line react-hooks/exhaustive-deps

  // Poll scraper status when scraper modal is open
  useEffect(() => {
    let interval;
    if (showScraper) {
      interval = setInterval(() => {
        fetchScraperStatus();
        fetchScraperLogs();
      }, 1000); // Poll every 1 second for real-time updates
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [showScraper]);

  const fetchData = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (filters.country) params.append('country', filters.country);
      if (filters.source) params.append('source', filters.source);
      params.append('limit', filters.limit);

      const response = await axios.get(`${API_BASE_URL}/news?${params}`);
      setArticles(response.data.articles || []);
    } catch (error) {
      console.error('Error fetching articles:', error);
      setArticles([]);
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/news/stats`);
      setStats(response.data.stats);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const fetchCountries = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/news/countries`);
      setCountries(response.data.countries || []);
    } catch (error) {
      console.error('Error fetching countries:', error);
    }
  };

  const fetchSources = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/news/sources`);
      setSources(response.data.sources || []);
    } catch (error) {
      console.error('Error fetching sources:', error);
    }
  };

  const fetchScraperStatus = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/scraper/status`);
      setScraperStatus(response.data.scraper);
    } catch (error) {
      console.error('Error fetching scraper status:', error);
    }
  };

  const fetchScraperLogs = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/scraper/logs`);
      const newLogs = response.data.logs || [];
      setScraperLogs(newLogs);
      
      // Auto-scroll to bottom when new logs arrive
      if (logContainer && newLogs.length > 0) {
        setTimeout(() => {
          logContainer.scrollTop = logContainer.scrollHeight;
        }, 100);
      }
    } catch (error) {
      console.error('Error fetching scraper logs:', error);
    }
  };

  const startScraper = async () => {
    try {
      await axios.post(`${API_BASE_URL}/scraper/start`);
      fetchScraperStatus();
    } catch (error) {
      console.error('Error starting scraper:', error);
      alert('Failed to start scraper: ' + (error.response?.data?.message || error.message));
    }
  };

  const stopScraper = async () => {
    try {
      await axios.post(`${API_BASE_URL}/scraper/stop`);
      fetchScraperStatus();
    } catch (error) {
      console.error('Error stopping scraper:', error);
      alert('Failed to stop scraper: ' + (error.response?.data?.message || error.message));
    }
  };

  const refreshData = async () => {
    await fetchData();
    await fetchStats();
    await fetchCountries();
    await fetchSources();
  };

  const filteredArticles = articles.filter(article =>
    article.title.toLowerCase().includes(filters.search.toLowerCase()) ||
    article.summary.toLowerCase().includes(filters.search.toLowerCase())
  );

  const totalPages = Math.ceil(filteredArticles.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const currentArticles = filteredArticles.slice(startIndex, startIndex + itemsPerPage);

  const formatDate = (dateString) => {
    try {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch {
      return dateString;
    }
  };

  const getCountryFlag = (country) => {
    const flagMap = {
      'United Kingdom': '🇬🇧',
      'United States': '🇺🇸',
      'Japan': '🇯🇵',
      'Qatar': '🇶🇦',
      'India': '🇮🇳',
      'Singapore': '🇸🇬',
      'Malaysia': '🇲🇾',
      'Australia': '🇦🇺',
      'China': '🇨🇳',
      'France': '🇫🇷',
      'Brazil': '🇧🇷',
      'Canada': '🇨🇦',
      'Denmark': '🇩🇰',
      'Egypt': '🇪🇬',
      'South Korea': '🇰🇷',
      'Thailand': '🇹🇭',
      'Philippines': '🇵🇭',
      'Vietnam': '🇻🇳',
      'Turkey': '🇹🇷',
      'Russia': '🇷🇺',
      'South Africa': '🇿🇦',
      'Nigeria': '🇳🇬',
      'Mexico': '🇲🇽',
      'Argentina': '🇦🇷'
    };
    return flagMap[country] || '🌍';
  };

  return (
    <div className="min-h-screen bg-gray-50 animate-fadeIn">
      {/* Header */}
      <header className="bg-white shadow-lg border-b sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <Globe className="h-8 w-8 text-gray-600 mr-3" />
              <div>
                <h1 className="text-3xl font-bold text-gray-900">
                  Global News Hub
                </h1>
                <p className="text-sm text-gray-500">RSS News from {countries.length} Countries</p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <button
                onClick={refreshData}
                className="btn-secondary flex items-center"
              >
                <RefreshCw className="h-4 w-4 mr-2" />
                Refresh
              </button>
              <button
                onClick={() => setShowScraper(!showScraper)}
                className="btn-success flex items-center"
              >
                <Play className="h-4 w-4 mr-2" />
                Scraper
              </button>
              <button
                onClick={() => setShowStats(!showStats)}
                className="btn-primary flex items-center"
              >
                <BarChart3 className="h-4 w-4 mr-2" />
                Stats
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Stats Modal */}
      {showStats && stats && (
        <div className="fixed inset-0 modal-backdrop flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl p-6 max-w-4xl w-full max-h-[80vh] overflow-y-auto shadow-xl">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-gray-900 flex items-center">
                <BarChart3 className="h-6 w-6 mr-2 text-blue-600" />
                Statistics
              </h2>
              <button
                onClick={() => setShowStats(false)}
                className="close-button"
              >
                ✕
              </button>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
              <div className="bg-blue-50 p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow">
                <h3 className="text-lg font-semibold text-blue-900 flex items-center">
                  <CheckCircle className="h-5 w-5 mr-2" />
                  Total Articles
                </h3>
                <p className="text-3xl font-bold text-blue-600">{stats.total_articles}</p>
              </div>
              <div className="bg-green-50 p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow">
                <h3 className="text-lg font-semibold text-green-900 flex items-center">
                  <Globe className="h-5 w-5 mr-2" />
                  Countries
                </h3>
                <p className="text-3xl font-bold text-green-600">{Object.keys(stats.articles_by_country).length}</p>
              </div>
              <div className="bg-purple-50 p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow">
                <h3 className="text-lg font-semibold text-purple-900 flex items-center">
                  <ExternalLink className="h-5 w-5 mr-2" />
                  Sources
                </h3>
                <p className="text-3xl font-bold text-purple-600">{Object.keys(stats.articles_by_source).length}</p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 className="text-lg font-semibold mb-3 flex items-center">
                  <Globe className="h-5 w-5 mr-2 text-blue-600" />
                  Articles by Country
                </h3>
                <div className="space-y-2 max-h-64 overflow-y-auto">
                  {Object.entries(stats.articles_by_country)
                    .sort(([,a], [,b]) => b - a)
                    .map(([country, count]) => (
                      <div key={country} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                        <span className="flex items-center">
                          <span className="mr-2 text-lg">{getCountryFlag(country)}</span>
                          {country}
                        </span>
                        <span className="font-semibold bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-sm">{count}</span>
                      </div>
                    ))}
                </div>
              </div>

              <div>
                <h3 className="text-lg font-semibold mb-3 flex items-center">
                  <ExternalLink className="h-5 w-5 mr-2 text-purple-600" />
                  Articles by Source
                </h3>
                <div className="space-y-2 max-h-64 overflow-y-auto">
                  {Object.entries(stats.articles_by_source)
                    .sort(([,a], [,b]) => b - a)
                    .map(([source, count]) => (
                      <div key={source} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                        <span className="truncate">{source}</span>
                        <span className="font-semibold bg-purple-100 text-purple-800 px-2 py-1 rounded-full text-sm">{count}</span>
                      </div>
                    ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Scraper Modal */}
      {showScraper && (
        <div className="fixed inset-0 modal-backdrop flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl p-6 max-w-4xl w-full max-h-[80vh] overflow-y-auto shadow-xl">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-gray-900 flex items-center">
                <Play className="h-6 w-6 mr-2 text-green-600" />
                News Scraper Control
              </h2>
              <button
                onClick={() => setShowScraper(false)}
                className="close-button"
              >
                ✕
              </button>
            </div>
            
            {/* Scraper Status */}
            <div className="mb-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold flex items-center">
                  <Clock className="h-5 w-5 mr-2 text-blue-600" />
                  Status
                </h3>
                <div className="flex items-center space-x-2">
                  {scraperStatus?.running ? (
                    <div className="flex items-center text-green-600">
                      <RefreshCw className="h-4 w-4 mr-1 animate-spin" />
                      Running
                    </div>
                  ) : (
                    <div className="flex items-center text-gray-600">
                      <Clock className="h-4 w-4 mr-1" />
                      Idle
                    </div>
                  )}
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div className="bg-blue-50 p-4 rounded-xl shadow-sm hover:shadow-md transition-shadow">
                  <h4 className="font-semibold text-blue-900 flex items-center">
                    <CheckCircle className="h-4 w-4 mr-2" />
                    Status
                  </h4>
                  <p className="text-blue-600 font-medium">
                    {scraperStatus?.running ? '🟢 Running' : '🔴 Stopped'}
                  </p>
                </div>
                <div className="bg-green-50 p-4 rounded-xl shadow-sm hover:shadow-md transition-shadow">
                  <h4 className="font-semibold text-green-900 flex items-center">
                    <Calendar className="h-4 w-4 mr-2" />
                    Last Run
                  </h4>
                  <p className="text-green-600 text-sm font-medium">
                    {scraperStatus?.last_run_formatted || 'Never'}
                  </p>
                </div>
                <div className="bg-purple-50 p-4 rounded-xl shadow-sm hover:shadow-md transition-shadow">
                  <h4 className="font-semibold text-purple-900 flex items-center">
                    <Clock className="h-4 w-4 mr-2" />
                    Duration
                  </h4>
                  <p className="text-purple-600 font-medium">
                    {scraperStatus?.running && scraperStatus?.duration 
                      ? `${scraperStatus.duration}s` 
                      : 'N/A'}
                  </p>
                </div>
              </div>

              {/* Control Buttons */}
              <div className="flex items-center space-x-4 mb-6">
                <button
                  onClick={startScraper}
                  disabled={scraperStatus?.running}
                  className="btn-success flex items-center transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Play className="h-5 w-5 mr-2" />
                  Start Scraper
                </button>
                <button
                  onClick={stopScraper}
                  disabled={!scraperStatus?.running}
                  className="btn-danger flex items-center transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Square className="h-5 w-5 mr-2" />
                  Stop Scraper
                </button>
                <button
                  onClick={() => {
                    fetchScraperStatus();
                    fetchScraperLogs();
                  }}
                  className="btn-secondary flex items-center transition-colors"
                >
                  <RefreshCw className="h-4 w-4 mr-2" />
                  Refresh Status
                </button>
              </div>
            </div>

            {/* Logs Section */}
            <div>
              <h3 className="text-lg font-semibold mb-3 flex items-center">
                <AlertCircle className="h-5 w-5 mr-2 text-gray-600" />
                Real-time Logs
              </h3>
              <div 
                ref={setLogContainer}
                className="bg-gray-900 text-green-400 p-4 rounded-xl font-mono text-sm max-h-64 overflow-y-auto shadow-inner"
              >
                {scraperLogs.length > 0 ? (
                  scraperLogs.map((log, index) => (
                    <div key={index} className="mb-1 whitespace-pre-wrap">
                      {log}
                    </div>
                  ))
                ) : (
                  <div className="text-gray-500 text-center py-4">No logs available</div>
                )}
                {scraperStatus?.running && (
                  <div className="text-yellow-400 animate-pulse">
                    <span className="inline-block w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse"></span>
                    Scraper is running...
                  </div>
                )}
              </div>
            </div>

            {/* Errors Section */}
            {/* {scraperStatus?.errors && scraperStatus.errors.length > 0 && (
              <div className="mt-4">
                <h3 className="text-lg font-semibold mb-3 text-red-600 flex items-center">
                  <XCircle className="h-5 w-5 mr-2" />
                  Errors
                </h3>
                <div className="bg-red-50 border border-red-200 rounded-xl p-4">
                  {scraperStatus.errors.map((error, index) => (
                    <div key={index} className="flex items-start mb-2 last:mb-0">
                      <XCircle className="h-4 w-4 text-red-500 mr-2 mt-0.5 flex-shrink-0" />
                      <span className="text-red-700 text-sm">{error}</span>
                    </div>
                  ))}
                </div>
              </div>
            )} */}
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
          <div className="flex items-center mb-4">
            <Filter className="h-5 w-5 text-gray-600 mr-2" />
            <h2 className="text-lg font-semibold text-gray-900">Filters</h2>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search articles..."
                value={filters.search}
                onChange={(e) => setFilters({...filters, search: e.target.value})}
                className="pl-10 w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            
            <select
              value={filters.country}
              onChange={(e) => setFilters({...filters, country: e.target.value})}
              className="px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Countries</option>
              {countries.map(country => (
                <option key={country} value={country}>
                  {getCountryFlag(country)} {country}
                </option>
              ))}
            </select>
            
            <select
              value={filters.source}
              onChange={(e) => setFilters({...filters, source: e.target.value})}
              className="px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Sources</option>
              {sources.map(source => (
                <option key={source} value={source}>{source}</option>
              ))}
            </select>
            
            <select
              value={filters.limit}
              onChange={(e) => setFilters({...filters, limit: parseInt(e.target.value)})}
              className="px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value={50}>50 articles</option>
              <option value={100}>100 articles</option>
              <option value={200}>200 articles</option>
              <option value={500}>500 articles</option>
            </select>
          </div>
        </div>

        {/* Loading */}
        {loading ? (
          <div className="flex justify-center items-center py-12">
            <div className="loading-spinner"></div>
          </div>
        ) : (
          <>
            {/* Results Info */}
            <div className="mb-6">
              <p className="text-gray-600 text-lg">
                Showing <span className="font-semibold">{currentArticles.length}</span> of <span className="font-semibold">{filteredArticles.length}</span> articles
                {filters.country && <span> from {filters.country}</span>}
                {filters.source && <span> from {filters.source}</span>}
              </p>
            </div>

            {/* Articles Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
              {currentArticles.map((article, index) => (
                <div key={index} className="card bg-white rounded-xl shadow-lg hover:shadow-xl border">
                  <div className="p-6">
                    <div className="flex items-center justify-between mb-3">
                      <span className="flex items-center text-sm text-gray-600 bg-gray-100 px-3 py-1 rounded-full">
                        <span className="mr-1 text-lg">{getCountryFlag(article.country)}</span>
                        {article.country}
                      </span>
                      <span className="text-xs text-gray-500 bg-blue-100 text-blue-800 px-2 py-1 rounded-full font-medium">
                        {article.language?.toUpperCase()}
                      </span>
                    </div>
                    
                    <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2 leading-tight hover:text-blue-600 transition-colors">
                      {article.title}
                    </h3>
                    
                    <p className="text-gray-600 text-sm mb-4 line-clamp-3">
                      {article.summary}
                    </p>
                    
                    <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                      <span className="flex items-center bg-gray-50 px-2 py-1 rounded-lg">
                        <Calendar className="h-4 w-4 mr-1" />
                        {formatDate(article.publication_date)}
                      </span>
                      <span className="font-medium text-purple-600 bg-purple-50 px-2 py-1 rounded-lg">{article.source}</span>
                    </div>
                    
                    <div className="mt-4">
                      <a
                        href={article.url}
          target="_blank"
          rel="noopener noreferrer"
                        className="inline-flex items-center text-blue-600 hover:text-blue-800 text-sm font-medium bg-blue-50 hover:bg-blue-100 px-3 py-2 rounded-lg transition-colors"
                      >
                        Read more
                        <ExternalLink className="h-4 w-4 ml-1" />
                      </a>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex justify-center items-center space-x-2">
                <button
                  onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                  disabled={currentPage === 1}
                  className="px-4 py-2 rounded-lg bg-white border border-gray-300 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors shadow-sm"
                >
                  Previous
                </button>
                
                <span className="px-4 py-2 text-sm text-gray-700 bg-blue-50 rounded-lg font-medium">
                  Page {currentPage} of {totalPages}
                </span>
                
                <button
                  onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
                  disabled={currentPage === totalPages}
                  className="px-4 py-2 rounded-lg bg-white border border-gray-300 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors shadow-sm"
                >
                  Next
                </button>
              </div>
            )}
          </>
        )}
      </div>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-gray-500 text-sm">
            Global News Hub - RSS Feed Aggregator | Powered by React & Flask
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
