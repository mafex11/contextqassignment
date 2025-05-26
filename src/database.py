"""
Database operations module for the RSS feed scraper
"""

import sqlite3
import os
from datetime import datetime
from typing import Dict, List, Optional
from dateutil.parser import parse as parse_date
from dateutil.tz import tzutc

from config import DATABASE_PATH, TABLE_SCHEMA

class Database:
    def __init__(self):
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
        
        self.conn = sqlite3.connect(DATABASE_PATH)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        """Create the news table if it doesn't exist"""
        self.cursor.execute(TABLE_SCHEMA)
        self.conn.commit()

    def insert_article(self, article: Dict) -> bool:
        """
        Insert a news article into the database
        
        Args:
            article (Dict): Article data containing title, date, source, etc.
            
        Returns:
            bool: True if insertion was successful, False if article already exists
        """
        try:
            # Parse the date string to datetime
            pub_date = parse_date(article['publication_date'])
            if pub_date.tzinfo is None:
                pub_date = pub_date.replace(tzinfo=tzutc())
            
            self.cursor.execute("""
                INSERT INTO news (title, publication_date, source, country, summary, url, language)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                article['title'],
                pub_date.isoformat(),
                article['source'],
                article['country'],
                article.get('summary', ''),
                article['url'],
                article.get('language', 'en')
            ))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Article already exists (due to UNIQUE constraint on url)
            return False

    def get_articles(self, 
                    country: Optional[str] = None, 
                    source: Optional[str] = None,
                    language: Optional[str] = None,
                    limit: int = 100) -> List[Dict]:
        """
        Retrieve articles from the database with optional filters
        
        Args:
            country (str, optional): Filter by country
            source (str, optional): Filter by news source
            language (str, optional): Filter by language
            limit (int): Maximum number of articles to return
            
        Returns:
            List[Dict]: List of articles matching the criteria
        """
        query = "SELECT * FROM news WHERE 1=1"
        params = []

        if country:
            query += " AND country = ?"
            params.append(country)
        
        if source:
            query += " AND source = ?"
            params.append(source)
            
        if language:
            query += " AND language = ?"
            params.append(language)

        query += " ORDER BY publication_date DESC LIMIT ?"
        params.append(limit)

        self.cursor.execute(query, params)
        return [dict(row) for row in self.cursor.fetchall()]

    def get_stats(self) -> Dict:
        """
        Get statistics about the collected data
        
        Returns:
            Dict: Statistics including total articles per country/source
        """
        # Get articles per country
        self.cursor.execute("""
            SELECT country, COUNT(*) as count 
            FROM news 
            GROUP BY country
        """)
        countries = {row['country']: row['count'] for row in self.cursor.fetchall()}

        # Get articles per source
        self.cursor.execute("""
            SELECT source, COUNT(*) as count 
            FROM news 
            GROUP BY source
        """)
        sources = {row['source']: row['count'] for row in self.cursor.fetchall()}

        # Get date range
        self.cursor.execute("""
            SELECT 
                MIN(publication_date) as oldest,
                MAX(publication_date) as newest
            FROM news
        """)
        date_range = self.cursor.fetchone()

        return {
            'total_articles': sum(countries.values()),
            'articles_by_country': countries,
            'articles_by_source': sources,
            'date_range': {
                'oldest': date_range['oldest'],
                'newest': date_range['newest']
            }
        }

    def close(self):
        """Close the database connection"""
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close() 