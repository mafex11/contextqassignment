"""
RSS feed scraper module
"""

import requests
import time
import sys
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from langdetect import detect
from tqdm import tqdm
from dateutil import parser as date_parser
from dateutil.tz import tzutc, tzlocal
import re

from config import RSS_FEEDS, HEADERS, REQUEST_DELAY, MAX_RETRIES

def print_flush(message):
    """Print message and flush immediately for real-time logging"""
    print(message)
    sys.stdout.flush()

class RSSFeedScraper:
    def __init__(self):
        self.feeds = RSS_FEEDS
        # Verify lxml is available
        try:
            BeautifulSoup("<test/>", "lxml-xml")
        except Exception as e:
            raise ImportError(
                "lxml parser is required but not installed. "
                "Please install it with: pip install lxml"
            ) from e

    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """
        Parse date string from RSS feed with multiple fallback formats
        """
        if not date_str:
            return None
            
        try:
            # Try standard RSS date parsing first
            return date_parser.parse(date_str)
        except Exception:
            # Try common date formats as fallbacks
            fallback_formats = [
                "%a, %d %b %Y %H:%M:%S %Z",  # RFC 2822
                "%Y-%m-%d %H:%M:%S",         # ISO format
                "%Y-%m-%dT%H:%M:%S",         # ISO with T
                "%Y-%m-%d",                  # Date only
                "%d %b %Y",                  # Simple format
                "%B %d, %Y"                  # Month Day, Year
            ]
            
            for fmt in fallback_formats:
                try:
                    return datetime.strptime(date_str.strip(), fmt)
                except ValueError:
                    continue
            
            # If all parsing fails, return None
            return None

    def _extract_text_content(self, element) -> str:
        """
        Extract clean text content from HTML/XML element
        """
        if element is None:
            return ""
        
        # If it's already a string, return it
        if isinstance(element, str):
            return element.strip()
        
        # Extract text and clean it
        text = element.get_text() if hasattr(element, 'get_text') else str(element)
        
        # Clean up HTML entities and extra whitespace
        text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
        text = re.sub(r'\s+', ' ', text)     # Normalize whitespace
        text = text.strip()
        
        return text

    def _generate_fallback_summary(self, title: str, content: str = "") -> str:
        """
        Generate a fallback summary when none is available
        """
        if not title:
            return "No summary available"
        
        # If we have content, try to extract first sentence
        if content:
            sentences = re.split(r'[.!?]+', content)
            if len(sentences) > 0 and len(sentences[0].strip()) > 20:
                return sentences[0].strip() + "."
        
        # Fallback: Use title as basis for summary
        if len(title) > 50:
            return title[:47] + "..."
        else:
            return f"Article about: {title}"

    def _parse_feed_content(self, content: str, feed_url: str) -> List[Dict]:
        """
        Parse RSS feed content with improved error handling and fallback mechanisms
        """
        articles = []
        
        try:
            # Parse with lxml-xml parser for better XML handling
            soup = BeautifulSoup(content, 'lxml-xml')
            
            # Try different RSS item selectors
            items = soup.find_all('item')
            if not items:
                items = soup.find_all('entry')  # Atom feeds
            
            if not items:
                print_flush(f"Warning: No items found in feed {feed_url}")
                return articles
            
            current_time = datetime.now()
            
            for item in items:
                try:
                    # Extract title with fallbacks
                    title_elem = item.find('title')
                    title = self._extract_text_content(title_elem) if title_elem else ""
                    
                    if not title:
                        continue  # Skip items without titles
                    
                    # Extract publication date with multiple fallbacks
                    pub_date = None
                    date_fields = ['pubDate', 'published', 'date', 'updated']
                    
                    for field in date_fields:
                        date_elem = item.find(field)
                        if date_elem:
                            date_str = self._extract_text_content(date_elem)
                            pub_date = self._parse_date(date_str)
                            if pub_date:
                                break
                    
                    # Fallback: Use current time if no date found
                    if not pub_date:
                        pub_date = current_time
                        print_flush(f"Warning: No publication date found for '{title[:50]}...', using current time")
                    
                    # Convert to string format
                    pub_date_str = pub_date.strftime("%a, %d %b %Y %H:%M:%S GMT") if pub_date else ""
                    
                    # Extract URL
                    url = ""
                    link_elem = item.find('link')
                    if link_elem:
                        url = link_elem.get('href') or self._extract_text_content(link_elem)
                    
                    # Extract summary/description with fallbacks
                    summary = ""
                    desc_fields = ['description', 'summary', 'content', 'content:encoded']
                    
                    for field in desc_fields:
                        desc_elem = item.find(field)
                        if desc_elem:
                            summary = self._extract_text_content(desc_elem)
                            if summary and len(summary) > 10:  # Ensure meaningful content
                                break
                    
                    # Fallback: Generate summary if none found
                    if not summary or len(summary) < 10:
                        # Try to get content from link text or title
                        content_text = self._extract_text_content(item)
                        summary = self._generate_fallback_summary(title, content_text)
                    
                    # Limit summary length
                    if len(summary) > 500:
                        summary = summary[:497] + "..."
                    
                    articles.append({
                        'title': title,
                        'publication_date': pub_date_str,
                        'summary': summary,
                        'url': url
                    })
                    
                except Exception as e:
                    print_flush(f"Warning: Error parsing article in {feed_url}: {str(e)}")
                    continue
            
        except Exception as e:
            print_flush(f"Error parsing feed {feed_url}: {str(e)}")
            return articles
        
        return articles

    def _detect_language(self, text: str) -> str:
        """
        Detect language of the text with fallback
        """
        try:
            if text and len(text.strip()) > 10:
                return detect(text)
        except Exception:
            pass
        return "en"  # Default to English

    def _fetch_feed(self, url: str) -> Optional[str]:
        """
        Fetch RSS feed content with retry mechanism
        """
        for attempt in range(MAX_RETRIES):
            try:
                response = requests.get(url, headers=HEADERS, timeout=30)
                response.raise_for_status()
                return response.text
            except requests.exceptions.RequestException as e:
                if attempt < MAX_RETRIES - 1:
                    print_flush(f"Retrying feed {url} after error: {str(e)}")
                    time.sleep(REQUEST_DELAY * (attempt + 1))
                else:
                    print_flush(f"Failed to fetch feed {url} after {MAX_RETRIES} retries: {str(e)}")
                    return None
        return None

    def scrape_feeds(self) -> List[Dict]:
        """
        Scrape all RSS feeds and return list of articles
        """
        all_articles = []
        
        # Count total feeds for progress bar
        total_feeds = sum(len(sources) for sources in self.feeds.values())
        
        with tqdm(total=total_feeds, desc="Scraping feeds") as pbar:
            for country, sources in self.feeds.items():
                for source in sources:
                    pbar.set_description(f"Processing feed: {source['name']} ({source['url']})")
                    
                    # Fetch feed content
                    content = self._fetch_feed(source['url'])
                    if not content:
                        pbar.update(1)
                        continue
                    
                    # Parse articles
                    articles = self._parse_feed_content(content, source['url'])
                    
                    # Add metadata to articles
                    for article in articles:
                        article['source'] = source['name']
                        article['country'] = country
                        
                        # Detect language if not specified or use fallback
                        if 'language' in source:
                            article['language'] = source['language']
                        else:
                            article['language'] = self._detect_language(article['title'] + " " + article['summary'])
                    
                    all_articles.extend(articles)
                    print_flush(f"Found {len(articles)} new articles from {source['name']}")
                    
                    # Rate limiting
                    time.sleep(REQUEST_DELAY)
                    pbar.update(1)
        
        return all_articles 