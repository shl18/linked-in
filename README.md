# LinkedIn Bot

A Python automation script for LinkedIn that can search for users and send automated messages.

## Setup

### 1. Virtual Environment
The project uses a virtual environment to avoid conflicts with system Python packages.

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment (macOS/Linux)
source venv/bin/activate

# Activate virtual environment (Windows)
venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Credentials
Edit `config.py` and add your LinkedIn credentials:

```python
username = "your_linkedin_email@example.com"
password = "your_linkedin_password"
```

## Usage

### Running the Bot
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run the main bot
python main.py

# Or use the runner script
python run_bot.py
```

### Configuration Options

Edit `config.py` to customize:

- `username` and `password`: Your LinkedIn credentials
- `MESSAGE_TEMPLATE`: The message template to send
- `SEARCH_QUERY`: The person to search for
- `TARGET_NAME`: Name to use in the message
- `TARGET_INDUSTRY`: Industry to mention in the message
- `HEADLESS_MODE`: Run browser in background (True/False)
- `BROWSER_WAIT_TIME`: Maximum wait time for elements (seconds)

## Files

- `main.py`: Main bot script with modern Selenium practices
- `message_automation.py`: Alternative automation script
- `config.py`: Configuration file with credentials and settings
- `requirements.txt`: Python dependencies
- `run_bot.py`: Helper script to run the bot
- `README.md`: This documentation

## Important Notes

⚠️ **Use Responsibly**: This bot is for educational purposes. Always follow LinkedIn's Terms of Service and use automation responsibly.

⚠️ **Rate Limiting**: Add delays between actions to avoid being detected as a bot.

⚠️ **Credentials**: Never commit your actual credentials to version control.

## Troubleshooting

### Virtual Environment Issues
If you get "externally-managed-environment" error:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Chrome Driver Issues
The bot uses `webdriver-manager` to automatically handle ChromeDriver installation.

### LinkedIn Detection
The bot includes anti-detection measures, but LinkedIn may still detect automation. Use responsibly and add human-like delays.
