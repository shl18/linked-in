#!/usr/bin/env python3
"""
LinkedIn Bot API Server
This server provides a REST API for the LinkedIn bot frontend.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import subprocess
import tempfile
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

def create_temp_config(message, target_name, target_industry):
    """Create a temporary config file for the bot execution"""
    config_content = f'''# LinkedIn Bot Configuration
# Generated for API request at {datetime.now()}

# LinkedIn login credentials
username = "dhrtayal2004@gmail.com"
password = "dhruv2004"

# Message template settings
MESSAGE_TEMPLATE = "{message.replace('"', '\\"')}"

# Target profile settings
TARGET_PROFILE_URL = "https://www.linkedin.com/in/sahilrevankar/"  # Direct URL to the profile
TARGET_NAME = "{target_name.replace('"', '\\"')}"  # The name to use in the message template
TARGET_INDUSTRY = "{target_industry.replace('"', '\\"')}"  # The industry to mention in the message

# Browser settings
HEADLESS_MODE = False  # Set to True to run browser in background
BROWSER_WAIT_TIME = 10  # Maximum wait time for elements to load (seconds)
'''
    
    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
    temp_file.write(config_content)
    temp_file.close()
    return temp_file.name

def run_bot_with_config(config_path):
    """Run the LinkedIn bot with the given config file"""
    try:
        # Get the path to the virtual environment
        venv_python = os.path.join(os.path.dirname(__file__), 'venv', 'bin', 'python')
        main_script = os.path.join(os.path.dirname(__file__), 'main.py')
        
        # Set environment variable for config path
        env = os.environ.copy()
        env['CONFIG_PATH'] = config_path
        
        # Run the bot
        result = subprocess.run(
            [venv_python, main_script],
            cwd=os.path.dirname(__file__),
            env=env,
            capture_output=True,
            text=True,
            timeout=120  # 2 minute timeout
        )
        
        return {
            'success': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
        
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'stdout': '',
            'stderr': 'Bot execution timed out',
            'returncode': -1
        }
    except Exception as e:
        return {
            'success': False,
            'stdout': '',
            'stderr': str(e),
            'returncode': -1
        }

@app.route('/api/send-messages', methods=['POST'])
def send_messages():
    """API endpoint to send messages to LinkedIn contacts"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        emails = data.get('emails', [])
        message = data.get('message', '')
        target_name = data.get('targetName', '')
        target_industry = data.get('targetIndustry', '')
        
        # Validate input
        if not emails or not isinstance(emails, list) or len(emails) == 0:
            return jsonify({'error': 'Please provide at least one email address'}), 400
        
        if not message or not target_name or not target_industry:
            return jsonify({'error': 'Please provide message, target name, and target industry'}), 400
        
        # Process each email
        results = []
        for email in emails:
            try:
                # Create temporary config for this email
                config_path = create_temp_config(message, target_name, target_industry)
                
                # Run the bot
                bot_result = run_bot_with_config(config_path)
                
                # Clean up temporary config
                try:
                    os.unlink(config_path)
                except:
                    pass
                
                if bot_result['success']:
                    results.append({
                        'email': email,
                        'success': True,
                        'message': f'Message sent successfully to {email}'
                    })
                else:
                    results.append({
                        'email': email,
                        'success': False,
                        'error': bot_result['stderr'] or 'Unknown error occurred'
                    })
                    
            except Exception as e:
                results.append({
                    'email': email,
                    'success': False,
                    'error': str(e)
                })
        
        # Calculate summary
        success_count = sum(1 for r in results if r['success'])
        failure_count = len(results) - success_count
        
        return jsonify({
            'success': True,
            'message': f'Processed {len(emails)} emails: {success_count} successful, {failure_count} failed',
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/send-messages-linkedin', methods=['POST'])
def send_messages_linkedin():
    """API endpoint to send messages to LinkedIn contacts via URLs"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        contacts = data.get('contacts', [])
        message = data.get('message', '')
        
        # Validate input
        if not contacts or not isinstance(contacts, list) or len(contacts) == 0:
            return jsonify({'error': 'Please provide at least one contact'}), 400
        
        if not message:
            return jsonify({'error': 'Please provide a message'}), 400
        
        # Process each contact
        results = []
        for contact in contacts:
            try:
                name = contact.get('name', 'Contact')
                linkedin_url = contact.get('linkedinUrl', '')
                industry = contact.get('industry', 'technology')
                
                if not linkedin_url:
                    results.append({
                        'name': name,
                        'success': False,
                        'error': 'No LinkedIn URL provided'
                    })
                    continue
                
                # Create temporary config for this contact
                config_path = create_temp_config(message, name, industry)
                
                # Update the config to use the specific LinkedIn URL
                with open(config_path, 'r') as f:
                    config_content = f.read()
                
                # Replace the target URL with the specific contact's URL
                config_content = config_content.replace(
                    'TARGET_PROFILE_URL = "https://www.linkedin.com/in/sahilrevankar/"',
                    f'TARGET_PROFILE_URL = "{linkedin_url}"'
                )
                
                with open(config_path, 'w') as f:
                    f.write(config_content)
                
                # Run the bot
                bot_result = run_bot_with_config(config_path)
                
                # Clean up temporary config
                try:
                    os.unlink(config_path)
                except:
                    pass
                
                if bot_result['success']:
                    results.append({
                        'name': name,
                        'linkedinUrl': linkedin_url,
                        'success': True,
                        'message': f'Message sent successfully to {name}'
                    })
                else:
                    results.append({
                        'name': name,
                        'linkedinUrl': linkedin_url,
                        'success': False,
                        'error': bot_result['stderr'] or 'Unknown error occurred'
                    })
                    
            except Exception as e:
                results.append({
                    'name': contact.get('name', 'Unknown'),
                    'linkedinUrl': contact.get('linkedinUrl', ''),
                    'success': False,
                    'error': str(e)
                })
        
        # Calculate summary
        success_count = sum(1 for r in results if r['success'])
        failure_count = len(results) - success_count
        
        return jsonify({
            'success': True,
            'message': f'Processed {len(contacts)} contacts: {success_count} successful, {failure_count} failed',
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/', methods=['GET'])
def index():
    """Root endpoint with API information"""
    return jsonify({
        'message': 'LinkedIn Bot API Server',
        'version': '1.0.0',
        'endpoints': {
            'POST /api/send-messages': 'Send messages to LinkedIn contacts',
            'GET /api/health': 'Health check'
        }
    })

if __name__ == '__main__':
    print("Starting LinkedIn Bot API Server...")
    print("API will be available at: http://localhost:5000")
    print("Frontend should connect to: http://localhost:5000/api/send-messages")
    app.run(host='0.0.0.0', port=5000, debug=True)
