#!/usr/bin/env python3
"""
LinkedIn Bot Runner
This script helps you run the LinkedIn bot with proper setup.
"""

import os
import sys
import subprocess

def check_virtual_env():
    """Check if we're in a virtual environment"""
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

def activate_virtual_env():
    """Activate the virtual environment if not already active"""
    if not check_virtual_env():
        print("Activating virtual environment...")
        venv_path = os.path.join(os.path.dirname(__file__), 'venv')
        if os.name == 'nt':  # Windows
            activate_script = os.path.join(venv_path, 'Scripts', 'activate.bat')
        else:  # Unix/Linux/macOS
            activate_script = os.path.join(venv_path, 'bin', 'activate')
        
        if os.path.exists(activate_script):
            print("Please run: source venv/bin/activate")
            print("Then run: python main.py")
        else:
            print("Virtual environment not found. Please run:")
            print("python3 -m venv venv")
            print("source venv/bin/activate")
            print("pip install -r requirements.txt")
    else:
        print("Virtual environment is active. Running bot...")
        subprocess.run([sys.executable, 'main.py'])

if __name__ == "__main__":
    print("LinkedIn Bot Runner")
    print("==================")
    
    if not os.path.exists('config.py'):
        print("Error: config.py not found!")
        print("Please make sure config.py exists and contains your LinkedIn credentials.")
        sys.exit(1)
    
    activate_virtual_env()
