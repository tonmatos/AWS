#!/usr/bin/env python3
"""
AWS SAA Quiz App Launcher
Starts HTTP server if not running, then opens the quiz app in browser
"""

import subprocess
import sys
import time
import webbrowser
import requests
import os
from pathlib import Path

def is_server_running(port=8000):
    """Check if HTTP server is already running on the specified port"""
    try:
        response = requests.get(f"http://localhost:{port}", timeout=2)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def start_server(port=8000):
    """Start HTTP server in the background"""
    print(f"Starting HTTP server on port {port}...")
    try:
        # Start server in background
        subprocess.Popen([
            sys.executable, "-m", "http.server", str(port)
        ], cwd=os.getcwd(), creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
        
        # Wait for server to start
        for i in range(10):
            time.sleep(0.5)
            if is_server_running(port):
                print(f"✓ Server started successfully on http://localhost:{port}")
                return True
        
        print("✗ Failed to start server")
        return False
    except Exception as e:
        print(f"✗ Error starting server: {e}")
        return False

def main():
    """Main launcher function"""
    port = 8000
    html_file = "aws_saa_quiz_app.html"
    
    # Check if HTML file exists
    if not Path(html_file).exists():
        print(f"✗ {html_file} not found in current directory")
        return 1
    
    # Check if server is already running
    if is_server_running(port):
        print(f"✓ Server already running on http://localhost:{port}")
    else:
        # Start the server
        if not start_server(port):
            return 1
    
    # Open browser
    url = f"http://localhost:{port}/{html_file}"
    print(f"Opening {url} in browser...")
    try:
        webbrowser.open(url)
        print("✓ Browser opened successfully")
        print("\n" + "="*50)
        print("AWS SAA Quiz App is now running!")
        print(f"URL: {url}")
        print("Press Ctrl+C in the server console to stop the server")
        print("="*50)
    except Exception as e:
        print(f"✗ Error opening browser: {e}")
        print(f"Please manually open: {url}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
