"""
Main script for RSS feed scraper with database storage
"""

import json
import csv
import os
import sys
from datetime import datetime
from scraper import RSSFeedScraper
from database import Database
from config import UPDATE_INTERVAL

def print_flush(message):
    """Print message and flush immediately for real-time logging"""
    print(message)
    sys.stdout.flush()

def ensure_data_dir():
    """Create data directory if it doesn't exist"""
    os.makedirs("data", exist_ok=True)

def save_to_json(articles):
    """Save articles to JSON file"""
    filename = f"data/articles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    print_flush(f"Saved {len(articles)} articles to {filename}")

def save_to_csv(articles):
    """Save articles to CSV file with proper handling of special characters"""
    if not articles:
        print_flush("No articles to save")
        return
        
    filename = f"data/articles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    fieldnames = ['title', 'publication_date', 'source', 'country', 'summary', 'url', 'language']
    
    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL, 
                               quotechar='"', escapechar=None, doublequote=True)
        writer.writeheader()
        for article in articles:
            # Clean any potential issues with the data
            clean_article = {}
            for key, value in article.items():
                if value is None:
                    clean_article[key] = ""
                else:
                    # Ensure value is string and clean problematic characters
                    clean_value = str(value)
                    # Remove newlines, carriage returns, and tabs
                    clean_value = clean_value.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
                    # Remove extra whitespace
                    clean_value = ' '.join(clean_value.split())
                    # Handle quotes properly by ensuring they're properly escaped
                    clean_article[key] = clean_value
            writer.writerow(clean_article)
    print_flush(f"Saved {len(articles)} articles to {filename}")

def save_to_database(articles):
    """Save articles to SQLite database"""
    if not articles:
        print_flush("No articles to save to database")
        return
    
    with Database() as db:
        new_articles = 0
        duplicate_articles = 0
        
        for article in articles:
            if db.insert_article(article):
                new_articles += 1
            else:
                duplicate_articles += 1
        
        print_flush(f"Database: {new_articles} new articles, {duplicate_articles} duplicates skipped")

def print_stats(articles):
    """Print statistics about the scraped articles"""
    if not articles:
        print_flush("No articles to analyze")
        return
        
    # Count articles by source
    sources = {}
    countries = {}
    for article in articles:
        source = article['source']
        country = article['country']
        sources[source] = sources.get(source, 0) + 1
        countries[country] = countries.get(country, 0) + 1
    
    print_flush("Scraping Statistics:")
    print_flush(f"Total Articles: {len(articles)}")
    print_flush(f"Countries Covered: {len(countries)}")
    print_flush(f"News Sources: {len(sources)}")
    
    print_flush("Articles by Country:")
    for country, count in sorted(countries.items()):
        print_flush(f"  {country}: {count}")
    
    print_flush("Articles by Source:")
    for source, count in sorted(sources.items()):
        print_flush(f"  {source}: {count}")

def scrape_and_save():
    """
    Scrape RSS feeds and save articles to files
    """
    print_flush(f"Starting scrape at {datetime.now().isoformat()}")
    
    # Initialize scraper
    print_flush("Initializing RSS scraper...")
    scraper = RSSFeedScraper()
    
    try:
        # Scrape feeds
        print_flush("Starting to scrape RSS feeds...")
        articles = scraper.scrape_feeds()
        
        print_flush(f"Scraping completed. Found {len(articles)} articles.")
        
        # Create data directory
        print_flush("Creating data directory...")
        ensure_data_dir()
        
        # Save to files
        print_flush("Saving to JSON file...")
        save_to_json(articles)
        
        print_flush("Saving to CSV file...")
        save_to_csv(articles)
        
        # Save to database
        print_flush("Saving to database...")
        save_to_database(articles)
        
        # Print statistics
        print_flush("Generating statistics...")
        print_stats(articles)
        
        print_flush("Scraping process completed successfully!")
        
    except Exception as e:
        print_flush(f"Error during scrape: {str(e)}")
        sys.stderr.write(f"Error during scrape: {str(e)}\n")
        sys.stderr.flush()

def main():
    """
    Main function to run the scraper with database storage
    """
    print_flush("RSS Feed Scraper (with Database)")
    print_flush("--------------------------------")
    print_flush(f"Update interval: {UPDATE_INTERVAL} hours")
    
    # Run scraper
    scrape_and_save()

if __name__ == "__main__":
    main() 