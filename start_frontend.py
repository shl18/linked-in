#!/usr/bin/env python3
"""
Startup script for the LinkedIn Bot Frontend
This script starts both the Python API server and the Next.js frontend.
"""

import subprocess
import sys
import os
import time
import threading
import signal
import webbrowser

def start_api_server():
    """Start the Python API server"""
    print("Starting Python API server...")
    try:
        # Activate virtual environment and start API server
        if os.name == 'nt':  # Windows
            python_path = os.path.join('venv', 'Scripts', 'python.exe')
        else:  # Unix/Linux/macOS
            python_path = os.path.join('venv', 'bin', 'python')
        
        subprocess.run([python_path, 'api_server.py'])
    except Exception as e:
        print(f"Failed to start API server: {e}")

def start_frontend():
    """Start the Next.js frontend"""
    print("Starting Next.js frontend...")
    try:
        os.chdir('frontend')
        
        # Install dependencies if needed
        if not os.path.exists('node_modules'):
            print("Installing frontend dependencies...")
            subprocess.run(['npm', 'install'], check=True)
        
        # Start the development server
        subprocess.run(['npm', 'run', 'dev'])
    except Exception as e:
        print(f"Failed to start frontend: {e}")

def main():
    print("LinkedIn Bot Frontend Startup")
    print("============================")
    
    # Check if we're in the right directory
    if not os.path.exists('api_server.py'):
        print("Error: Please run this script from the project root directory")
        sys.exit(1)
    
    # Check if virtual environment exists
    if not os.path.exists('venv'):
        print("Error: Virtual environment not found. Please run:")
        print("python3 -m venv venv")
        print("source venv/bin/activate")
        print("pip install -r requirements.txt")
        sys.exit(1)
    
    # Start API server in a separate thread
    api_thread = threading.Thread(target=start_api_server, daemon=True)
    api_thread.start()
    
    # Wait a moment for API server to start
    time.sleep(3)
    
    # Start frontend
    try:
        start_frontend()
    except KeyboardInterrupt:
        print("\nShutting down...")
        sys.exit(0)

if __name__ == "__main__":
    main()
