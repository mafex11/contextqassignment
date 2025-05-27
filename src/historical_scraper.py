"""
Historical news data scraper for collecting past year's news articles
Uses multiple approaches: Wayback Machine, web scraping, and external APIs
"""

import requests
import time
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from bs4 import BeautifulSoup
from dateutil import parser as date_parser
from urllib.parse import urljoin, urlparse
import re
from tqdm import tqdm
import sys

from config import RSS_FEEDS, HEADERS, REQUEST_DELAY, MAX_RETRIES
from database import Database

def print_flush(message):
    """Print message and flush immediately for real-time logging"""
    print(message)
    sys.stdout.flush()

class HistoricalNewsScraper:
    def __init__(self):
        self.wayback_api = "http://web.archive.org/cdx/search/cdx"
        self.newsapi_key = os.getenv('NEWSAPI_KEY')  # Users can add their API key
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        
    def get_wayback_snapshots(self, url: str, start_date: str, end_date: str) -> List[Dict]:
        """
        Get historical snapshots of RSS feeds from Wayback Machine
        """
        print_flush(f"Searching Wayback Machine for {url} from {start_date} to {end_date}")
        
        params = {
            'url': url,
            'from': start_date.replace('-', ''),
            'to': end_date.replace('-', ''),
            'output': 'json',
            'fl': 'timestamp,original,statuscode',
            'filter': 'statuscode:200',
            'collapse': 'timestamp:8'  # One snapshot per day
        }
        
        try:
            response = requests.get(self.wayback_api, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            if not data:
                return []
            
            # Skip the header row
            snapshots = []
            for row in data[1:]:
                if len(row) >= 3:
                    timestamp, original_url, status_code = row[:3]
                    if status_code == '200':
                        # Convert timestamp to readable date
                        snapshot_date = datetime.strptime(timestamp[:8], '%Y%m%d')
                        wayback_url = f"http://web.archive.org/web/{timestamp}/{original_url}"
                        
                        snapshots.append({
                            'date': snapshot_date.strftime('%Y-%m-%d'),
                            'wayback_url': wayback_url,
                            'original_url': original_url
                        })
            
            print_flush(f"Found {len(snapshots)} historical snapshots for {url}")
            return snapshots
            
        except Exception as e:
            print_flush(f"Error accessing Wayback Machine for {url}: {str(e)}")
            return []
    
    def fetch_historical_rss(self, wayback_url: str) -> Optional[str]:
        """
        Fetch RSS content from Wayback Machine
        """
        try:
            response = self.session.get(wayback_url, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print_flush(f"Error fetching {wayback_url}: {str(e)}")
            return None
    
    def parse_historical_feed(self, content: str, snapshot_date: str, source_name: str, country: str) -> List[Dict]:
        """
        Parse historical RSS feed content and extract articles
        """
        articles = []
        
        try:
            soup = BeautifulSoup(content, 'lxml-xml')
            
            # Try different RSS item selectors
            items = soup.find_all('item')
            if not items:
                items = soup.find_all('entry')  # Atom feeds
            
            for item in items:
                try:
                    # Extract title
                    title_elem = item.find('title')
                    title = title_elem.get_text().strip() if title_elem else ""
                    
                    if not title:
                        continue
                    
                    # Extract publication date
                    pub_date = None
                    date_fields = ['pubDate', 'published', 'date', 'updated']
                    
                    for field in date_fields:
                        date_elem = item.find(field)
                        if date_elem:
                            try:
                                date_str = date_elem.get_text().strip()
                                pub_date = date_parser.parse(date_str)
                                break
                            except:
                                continue
                    
                    # Use snapshot date as fallback
                    if not pub_date:
                        pub_date = datetime.strptime(snapshot_date, '%Y-%m-%d')
                    
                    # Extract URL
                    url = ""
                    link_elem = item.find('link')
                    if link_elem:
                        url = link_elem.get('href') or link_elem.get_text().strip()
                    
                    # Extract summary
                    summary = ""
                    desc_fields = ['description', 'summary', 'content', 'content:encoded']
                    
                    for field in desc_fields:
                        desc_elem = item.find(field)
                        if desc_elem:
                            summary = desc_elem.get_text().strip()
                            if summary and len(summary) > 10:
                                break
                    
                    # Clean up summary
                    if summary:
                        summary = re.sub(r'<[^>]+>', '', summary)  # Remove HTML tags
                        summary = re.sub(r'\s+', ' ', summary).strip()
                        if len(summary) > 500:
                            summary = summary[:497] + "..."
                    
                    if not summary:
                        summary = f"Historical article: {title[:100]}..."
                    
                    articles.append({
                        'title': title,
                        'publication_date': pub_date.strftime("%a, %d %b %Y %H:%M:%S GMT"),
                        'summary': summary,
                        'url': url,
                        'source': source_name,
                        'country': country,
                        'language': 'en',  # Default, can be enhanced
                        'historical': True,
                        'snapshot_date': snapshot_date
                    })
                    
                except Exception as e:
                    print_flush(f"Error parsing article: {str(e)}")
                    continue
                    
        except Exception as e:
            print_flush(f"Error parsing feed content: {str(e)}")
            
        return articles
    
    def scrape_news_archive_pages(self, base_url: str, source_name: str, country: str, start_date: str) -> List[Dict]:
        """
        Try to scrape historical articles from news website archive pages
        """
        articles = []
        print_flush(f"Attempting to scrape archive pages for {source_name}")
        
        # Common archive URL patterns
        archive_patterns = [
            f"{base_url}/archive",
            f"{base_url}/archives",
            f"{base_url}/sitemap",
            f"{base_url}/news/archive",
            f"{base_url}/category/news"
        ]
        
        for archive_url in archive_patterns:
            try:
                response = self.session.get(archive_url, timeout=30)
                if response.status_code == 200:
                    print_flush(f"Found archive page: {archive_url}")
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Look for article links
                    article_links = []
                    
                    # Common selectors for article links
                    selectors = [
                        'a[href*="/news/"]',
                        'a[href*="/article/"]',
                        'a[href*="/story/"]',
                        'a[href*="/post/"]',
                        '.article-link',
                        '.news-link'
                    ]
                    
                    for selector in selectors:
                        links = soup.select(selector)
                        for link in links[:20]:  # Limit to prevent overload
                            href = link.get('href')
                            if href:
                                full_url = urljoin(archive_url, href)
                                article_links.append(full_url)
                    
                    # Process found article links
                    for article_url in article_links[:10]:  # Limit for demo
                        article_data = self.scrape_individual_article(article_url, source_name, country)
                        if article_data:
                            articles.append(article_data)
                        
                        time.sleep(REQUEST_DELAY)  # Rate limiting
                    
                    break  # Found working archive page
                    
            except Exception as e:
                print_flush(f"Error accessing archive {archive_url}: {str(e)}")
                continue
        
        return articles
    
    def scrape_individual_article(self, url: str, source_name: str, country: str) -> Optional[Dict]:
        """
        Scrape individual article page for content
        """
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = ""
            title_selectors = ['h1', '.article-title', '.entry-title', 'title']
            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem:
                    title = title_elem.get_text().strip()
                    break
            
            if not title:
                return None
            
            # Extract publication date from meta tags or content
            pub_date = datetime.now()
            date_selectors = [
                'meta[property="article:published_time"]',
                'meta[name="publish-date"]',
                'meta[name="date"]',
                '.publish-date',
                '.article-date',
                'time'
            ]
            
            for selector in date_selectors:
                date_elem = soup.select_one(selector)
                if date_elem:
                    date_str = date_elem.get('content') or date_elem.get_text()
                    try:
                        pub_date = date_parser.parse(date_str)
                        break
                    except:
                        continue
            
            # Extract content/summary
            summary = ""
            content_selectors = [
                '.article-content',
                '.entry-content',
                '.post-content',
                'meta[name="description"]',
                'meta[property="og:description"]'
            ]
            
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    if content_elem.name == 'meta':
                        summary = content_elem.get('content', '')
                    else:
                        summary = content_elem.get_text().strip()
                    
                    if summary and len(summary) > 20:
                        break
            
            # Clean summary
            if summary:
                summary = re.sub(r'\s+', ' ', summary).strip()
                if len(summary) > 500:
                    summary = summary[:497] + "..."
            
            if not summary:
                summary = f"Article from {source_name}: {title[:100]}..."
            
            return {
                'title': title,
                'publication_date': pub_date.strftime("%a, %d %b %Y %H:%M:%S GMT"),
                'summary': summary,
                'url': url,
                'source': source_name,
                'country': country,
                'language': 'en',
                'historical': True
            }
            
        except Exception as e:
            print_flush(f"Error scraping article {url}: {str(e)}")
            return None
    
    def collect_historical_data(self, months_back: int = 12) -> List[Dict]:
        """
        Main method to collect historical data using multiple approaches
        """
        all_articles = []
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months_back * 30)
        
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')
        
        print_flush(f"Collecting historical data from {start_date_str} to {end_date_str}")
        print_flush(f"Using multiple approaches: Wayback Machine, Archive scraping")
        
        total_sources = sum(len(sources) for sources in RSS_FEEDS.values())
        
        with tqdm(total=total_sources, desc="Processing sources for historical data") as pbar:
            for country, sources in RSS_FEEDS.items():
                for source in sources:
                    pbar.set_description(f"Historical data: {source['name']} ({country})")
                    
                    # Method 1: Wayback Machine RSS snapshots
                    snapshots = self.get_wayback_snapshots(
                        source['url'], 
                        start_date_str, 
                        end_date_str
                    )
                    
                    # Process snapshots (limit to prevent overload)
                    for snapshot in snapshots[:12]:  # Max 12 snapshots per source
                        if snapshot['wayback_url']:
                            content = self.fetch_historical_rss(snapshot['wayback_url'])
                            if content:
                                articles = self.parse_historical_feed(
                                    content, 
                                    snapshot['date'], 
                                    source['name'], 
                                    country
                                )
                                all_articles.extend(articles)
                        
                        time.sleep(REQUEST_DELAY)  # Rate limiting
                    
                    # Method 2: Try to find archive pages (for major sources)
                    if len(snapshots) < 5:  # If Wayback didn't find much
                        try:
                            base_url = f"https://{urlparse(source['url']).netloc}"
                            archive_articles = self.scrape_news_archive_pages(
                                base_url, 
                                source['name'], 
                                country, 
                                start_date_str
                            )
                            all_articles.extend(archive_articles)
                        except Exception as e:
                            print_flush(f"Archive scraping failed for {source['name']}: {str(e)}")
                    
                    time.sleep(REQUEST_DELAY * 2)  # Rate limiting between sources
                    pbar.update(1)
        
        # Remove duplicates based on URL and title
        unique_articles = []
        seen_urls = set()
        seen_titles = set()
        
        for article in all_articles:
            identifier = f"{article.get('url', '')}-{article.get('title', '')}"
            if identifier not in seen_urls and article.get('title') not in seen_titles:
                unique_articles.append(article)
                seen_urls.add(identifier)
                seen_titles.add(article.get('title', ''))
        
        print_flush(f"Collected {len(unique_articles)} unique historical articles")
        return unique_articles
    
    def save_historical_data(self, articles: List[Dict]) -> int:
        """
        Save historical articles to database
        """
        saved_count = 0
        
        with Database() as db:
            for article in tqdm(articles, desc="Saving historical articles"):
                try:
                    if db.insert_article(article):
                        saved_count += 1
                except Exception as e:
                    print_flush(f"Error saving article '{article.get('title', '')}': {str(e)}")
        
        print_flush(f"Successfully saved {saved_count} historical articles to database")
        return saved_count

def main():
    """
    Main function to run historical data collection
    """
    print_flush("=== Historical News Data Collection ===")
    print_flush("This will collect news articles from the past 12 months using:")
    print_flush("1. Wayback Machine RSS feed snapshots")
    print_flush("2. News website archive page scraping")
    print_flush("3. Multiple fallback methods")
    print_flush("")
    
    scraper = HistoricalNewsScraper()
    
    # Collect historical data
    historical_articles = scraper.collect_historical_data(months_back=12)
    
    if historical_articles:
        # Save to database
        saved_count = scraper.save_historical_data(historical_articles)
        
        # Export to files
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save to JSON
        json_filename = f"data/historical_articles_{timestamp}.json"
        os.makedirs('data', exist_ok=True)
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(historical_articles, f, indent=2, ensure_ascii=False)
        
        print_flush(f"Historical data collection completed!")
        print_flush(f"- Collected: {len(historical_articles)} articles")
        print_flush(f"- Saved to database: {saved_count} articles")
        print_flush(f"- Exported to: {json_filename}")
    else:
        print_flush("No historical articles were collected.")

if __name__ == "__main__":
    main() 