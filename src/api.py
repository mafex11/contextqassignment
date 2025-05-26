"""
Flask API for serving news data
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from database import Database
import threading
import subprocess
import time
import os
import json
import queue
import sys
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variables for scraper status
scraper_status = {
    'running': False,
    'start_time': None,
    'last_run': None,
    'articles_scraped': 0,
    'errors': [],
    'logs': []
}

# Thread-safe queue for real-time logs
log_queue = queue.Queue()
scraper_process = None

def log_reader(pipe, log_type='stdout'):
    """Read logs from subprocess pipe in real-time"""
    global scraper_status
    
    try:
        for line in iter(pipe.readline, ''):
            if line:
                timestamp = datetime.now().strftime('%H:%M:%S')
                log_entry = f"[{timestamp}] {line.strip()}"
                
                # Add to logs
                scraper_status['logs'].append(log_entry)
                
                # Keep only last 100 log entries to prevent memory issues
                if len(scraper_status['logs']) > 100:
                    scraper_status['logs'] = scraper_status['logs'][-100:]
                
                # If it's an error, also add to errors
                if log_type == 'stderr' and line.strip():
                    scraper_status['errors'].append(line.strip())
                    
    except Exception as e:
        scraper_status['errors'].append(f'Log reader error: {str(e)}')
    finally:
        pipe.close()

def run_scraper():
    """Run the scraper in a separate thread with real-time logging"""
    global scraper_status, scraper_process
    
    try:
        scraper_status['running'] = True
        scraper_status['start_time'] = time.time()
        scraper_status['errors'] = []
        scraper_status['logs'] = [f"[{datetime.now().strftime('%H:%M:%S')}] Scraper started..."]
        
        # Start the scraper process with real-time output
        scraper_process = subprocess.Popen(
            [sys.executable, 'src/main.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,  # Line buffered
            universal_newlines=True,
            cwd=os.getcwd()
        )
        
        # Start threads to read stdout and stderr in real-time
        stdout_thread = threading.Thread(
            target=log_reader, 
            args=(scraper_process.stdout, 'stdout'),
            daemon=True
        )
        stderr_thread = threading.Thread(
            target=log_reader, 
            args=(scraper_process.stderr, 'stderr'),
            daemon=True
        )
        
        stdout_thread.start()
        stderr_thread.start()
        
        # Wait for process to complete
        return_code = scraper_process.wait()
        
        # Wait for log threads to finish reading
        stdout_thread.join(timeout=5)
        stderr_thread.join(timeout=5)
        
        timestamp = datetime.now().strftime('%H:%M:%S')
        if return_code == 0:
            scraper_status['logs'].append(f'[{timestamp}] Scraper completed successfully')
        else:
            error_msg = f'Scraper failed with return code {return_code}'
            scraper_status['errors'].append(error_msg)
            scraper_status['logs'].append(f'[{timestamp}] {error_msg}')
            
    except Exception as e:
        timestamp = datetime.now().strftime('%H:%M:%S')
        error_msg = f'Exception running scraper: {str(e)}'
        scraper_status['errors'].append(error_msg)
        scraper_status['logs'].append(f'[{timestamp}] {error_msg}')
    
    finally:
        scraper_status['running'] = False
        scraper_status['last_run'] = time.time()
        scraper_process = None

@app.route('/api/news')
def get_news():
    """Get news articles with optional filters"""
    country = request.args.get('country')
    source = request.args.get('source')
    language = request.args.get('language')
    limit = request.args.get('limit', default=100, type=int)

    with Database() as db:
        articles = db.get_articles(
            country=country,
            source=source,
            language=language,
            limit=limit
        )
    
    return jsonify({
        'status': 'success',
        'count': len(articles),
        'articles': articles
    })

@app.route('/api/news/stats')
def get_stats():
    """Get statistics about collected news data"""
    with Database() as db:
        stats = db.get_stats()
    
    return jsonify({
        'status': 'success',
        'stats': stats
    })

@app.route('/api/news/countries')
def get_countries():
    """Get list of available countries"""
    with Database() as db:
        stats = db.get_stats()
        countries = list(stats['articles_by_country'].keys())
    
    return jsonify({
        'status': 'success',
        'countries': countries
    })

@app.route('/api/news/sources')
def get_sources():
    """Get list of available news sources"""
    with Database() as db:
        stats = db.get_stats()
        sources = list(stats['articles_by_source'].keys())
    
    return jsonify({
        'status': 'success',
        'sources': sources
    })

@app.route('/api/scraper/start', methods=['POST'])
def start_scraper():
    """Start the news scraper"""
    global scraper_status
    
    if scraper_status['running']:
        return jsonify({
            'status': 'error',
            'message': 'Scraper is already running'
        }), 400
    
    # Start scraper in background thread
    thread = threading.Thread(target=run_scraper)
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'status': 'success',
        'message': 'Scraper started successfully'
    })

@app.route('/api/scraper/stop', methods=['POST'])
def stop_scraper():
    """Stop the running scraper"""
    global scraper_status, scraper_process
    
    if not scraper_status['running']:
        return jsonify({
            'status': 'error',
            'message': 'No scraper is currently running'
        }), 400
    
    try:
        if scraper_process:
            scraper_process.terminate()
            # Give it a moment to terminate gracefully
            time.sleep(2)
            if scraper_process.poll() is None:
                scraper_process.kill()
            
            timestamp = datetime.now().strftime('%H:%M:%S')
            scraper_status['logs'].append(f'[{timestamp}] Scraper stopped by user')
            scraper_status['running'] = False
            scraper_status['last_run'] = time.time()
            
        return jsonify({
            'status': 'success',
            'message': 'Scraper stopped successfully'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error stopping scraper: {str(e)}'
        }), 500

@app.route('/api/scraper/status')
def get_scraper_status():
    """Get current scraper status"""
    global scraper_status
    
    status_copy = scraper_status.copy()
    
    # Add formatted timestamps
    if status_copy['start_time']:
        status_copy['start_time_formatted'] = time.strftime(
            '%Y-%m-%d %H:%M:%S', 
            time.localtime(status_copy['start_time'])
        )
        if status_copy['running']:
            status_copy['duration'] = int(time.time() - status_copy['start_time'])
    
    if status_copy['last_run']:
        status_copy['last_run_formatted'] = time.strftime(
            '%Y-%m-%d %H:%M:%S', 
            time.localtime(status_copy['last_run'])
        )
    
    return jsonify({
        'status': 'success',
        'scraper': status_copy
    })

@app.route('/api/scraper/logs')
def get_scraper_logs():
    """Get scraper logs"""
    global scraper_status
    
    return jsonify({
        'status': 'success',
        'logs': scraper_status['logs'],  # Return all current logs
        'errors': scraper_status['errors']
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 