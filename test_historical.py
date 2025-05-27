#!/usr/bin/env python3
"""
Test script for historical data collection
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from historical_scraper import HistoricalNewsScraper

def main():
    print("🕒 Testing Historical News Data Collection")
    print("=" * 50)
    
    scraper = HistoricalNewsScraper()
    
    # Test with a smaller subset for demonstration
    print("Testing with a few sources for demonstration...")
    
    # Collect historical data for the past 3 months (to speed up demo)
    articles = scraper.collect_historical_data(months_back=3)
    
    if articles:
        print(f"\n✅ Success! Collected {len(articles)} historical articles")
        
        # Show some examples
        print("\n📰 Sample historical articles:")
        for i, article in enumerate(articles[:5]):
            print(f"\n{i+1}. {article['title']}")
            print(f"   Source: {article['source']} ({article['country']})")
            print(f"   Date: {article['publication_date']}")
            print(f"   Summary: {article['summary'][:100]}...")
        
        # Save to database
        saved_count = scraper.save_historical_data(articles)
        print(f"\n💾 Saved {saved_count} articles to database")
        
    else:
        print("❌ No historical articles were found")

if __name__ == "__main__":
    main() 