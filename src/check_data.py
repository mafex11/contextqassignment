"""
Script to check data quality of scraped articles
"""

import json
import os
from datetime import datetime
from dateutil import parser

def check_article(article):
    """Check if an article has valid data in all required fields"""
    issues = []
    
    # Check title
    if not article.get('title'):
        issues.append("Missing title")
    elif not isinstance(article['title'], str):
        issues.append("Title is not a string")
        
    # Check publication date
    if not article.get('publication_date'):
        issues.append("Missing publication date")
    else:
        try:
            parser.parse(article['publication_date'])
        except:
            issues.append("Invalid publication date format")
            
    # Check source
    if not article.get('source'):
        issues.append("Missing source")
    elif not isinstance(article['source'], str):
        issues.append("Source is not a string")
        
    # Check country
    if not article.get('country'):
        issues.append("Missing country")
    elif not isinstance(article['country'], str):
        issues.append("Country is not a string")
        
    # Check summary
    if not article.get('summary'):
        issues.append("Missing summary")
    elif not isinstance(article['summary'], str):
        issues.append("Summary is not a string")
        
    # Check URL
    if not article.get('url'):
        issues.append("Missing URL")
    elif not isinstance(article['url'], str):
        issues.append("URL is not a string")
    elif not article['url'].startswith(('http://', 'https://')):
        issues.append("Invalid URL format")
        
    # Check language
    if not article.get('language'):
        issues.append("Missing language")
    elif not isinstance(article['language'], str):
        issues.append("Language is not a string")
    elif len(article['language']) != 2:
        issues.append("Language code should be 2 characters")
        
    return issues

def analyze_json_file(filename):
    """Analyze the JSON file for data quality"""
    with open(filename, 'r', encoding='utf-8') as f:
        articles = json.load(f)
        
    print(f"\nAnalyzing {len(articles)} articles...")
    
    # Track statistics
    total_issues = 0
    articles_with_issues = 0
    issues_by_source = {}
    issues_by_type = {}
    
    # Check each article
    for i, article in enumerate(articles):
        issues = check_article(article)
        if issues:
            total_issues += len(issues)
            articles_with_issues += 1
            source = article.get('source', 'Unknown')
            issues_by_source[source] = issues_by_source.get(source, 0) + len(issues)
            for issue in issues:
                issues_by_type[issue] = issues_by_type.get(issue, 0) + 1
                print(f"\nArticle {i+1} from {source} has issues:")
                print(f"Title: {article.get('title', 'N/A')}")
                for issue in issues:
                    print(f"  - {issue}")
    
    # Print summary
    print("\nData Quality Summary:")
    print(f"Total articles: {len(articles)}")
    print(f"Articles with issues: {articles_with_issues}")
    print(f"Total issues found: {total_issues}")
    
    if issues_by_source:
        print("\nIssues by source:")
        for source, count in sorted(issues_by_source.items()):
            print(f"  {source}: {count} issues")
    
    if issues_by_type:
        print("\nIssues by type:")
        for issue, count in sorted(issues_by_type.items()):
            print(f"  {issue}: {count} occurrences")
    
    # Print sample of valid articles
    print("\nSample of valid articles:")
    valid_articles = [a for i, a in enumerate(articles) if not check_article(a)][:3]
    for article in valid_articles:
        print(f"\nTitle: {article['title']}")
        print(f"Source: {article['source']}")
        print(f"Date: {article['publication_date']}")
        print(f"Language: {article['language']}")
        print(f"URL: {article['url']}")
        print(f"Summary length: {len(article['summary'])} chars")

if __name__ == "__main__":
    # Find the most recent JSON file
    data_dir = "data"
    json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
    if not json_files:
        print("No JSON files found in data directory")
        exit(1)
        
    latest_file = max(json_files, key=lambda x: os.path.getctime(os.path.join(data_dir, x)))
    analyze_json_file(os.path.join(data_dir, latest_file)) 