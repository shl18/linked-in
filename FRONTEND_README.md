# LinkedIn Bot Frontend

A modern Next.js frontend for the LinkedIn Bot that allows you to send automated messages to LinkedIn contacts through a web interface.

## Features

- **Dual Input Methods**: 
  - Manual email input (comma-separated)
  - Excel file upload with LinkedIn URLs
- **Excel File Support**: Upload .xlsx/.xls files with contact information
- **Message Template**: Customize your message with placeholders for name and industry
- **Contact Preview**: Review and select contacts before sending messages
- **Real-time Feedback**: See success/error messages for each contact
- **Modern UI**: Clean, responsive design with Tailwind CSS

## Setup Instructions

### 1. Install Python Dependencies

Make sure you're in the project root directory and have the virtual environment activated:

```bash
# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 3. Start the Application

You have two options:

#### Option A: Use the Startup Script (Recommended)
```bash
# From the project root directory
python start_frontend.py
```

This will start both the Python API server and the Next.js frontend automatically.

#### Option B: Start Manually

**Terminal 1 - Start Python API Server:**
```bash
# From the project root directory
python api_server.py
```

**Terminal 2 - Start Next.js Frontend:**
```bash
# From the frontend directory
cd frontend
npm run dev
```

### 4. Access the Application

- Frontend: http://localhost:3000
- API Server: http://localhost:5000

## Usage

### Method 1: Manual Input
1. **Enter Email Addresses**: In the "Email Addresses" field, enter one or more email addresses separated by commas.
2. **Set Target Information**: 
   - **Target Name**: The name that will replace `{name}` in your message
   - **Target Industry**: The industry that will replace `{industry}` in your message
3. **Customize Message**: Edit the message template. Use `{name}` and `{industry}` as placeholders.
4. **Send Messages**: Click "Send Messages" to start the automation process.

### Method 2: Excel File Upload
1. **Prepare Excel File**: Create an Excel file with columns for:
   - **Name**: Contact's name
   - **LinkedIn URL**: Full LinkedIn profile URL (e.g., https://www.linkedin.com/in/username)
   - **Industry**: Contact's industry (optional)
2. **Upload File**: Click "Upload Excel File" and drag/drop your file or click to browse
3. **Review Contacts**: Preview the parsed data and select which contacts to message
4. **Send Messages**: Click "Send Messages" to start the automation process

### Excel File Format
Your Excel file should have these columns (case-insensitive):
- `Name` or `name` - Contact's name
- `LinkedIn URL` or `linkedin_url` or `LinkedIn` - Full LinkedIn profile URL
- `Industry` or `industry` - Contact's industry (optional, defaults to "technology")

## How It Works

1. The frontend sends a POST request to the Python API server with the email list and message details.
2. The API server creates a temporary configuration file for each email.
3. The LinkedIn bot runs for each email, using the provided message template and target information.
4. Results are returned to the frontend showing success/failure for each email.

## Configuration

The bot uses the credentials and settings from `config.py`. Make sure to update these before running:

- `username`: Your LinkedIn email
- `password`: Your LinkedIn password
- `TARGET_PROFILE_URL`: The LinkedIn profile URL to message

## Troubleshooting

### Common Issues

1. **CORS Errors**: Make sure the Python API server is running on port 5000
2. **Bot Execution Fails**: Check that Chrome is installed and the LinkedIn credentials are correct
3. **Frontend Won't Start**: Make sure you've run `npm install` in the frontend directory

### Logs

- Python API server logs are displayed in the terminal where you started it
- Frontend logs are available in the browser's developer console

## Security Notes

- The LinkedIn credentials are stored in `config.py` - keep this file secure
- The API server runs on localhost by default for security
- Consider using environment variables for production deployments

## File Structure

```
linkdin-bot/
├── frontend/                 # Next.js frontend
│   ├── app/
│   │   ├── page.tsx         # Main page component
│   │   ├── layout.tsx       # Root layout
│   │   └── globals.css      # Global styles
│   ├── package.json         # Frontend dependencies
│   └── tailwind.config.js   # Tailwind configuration
├── api_server.py            # Python Flask API server
├── main.py                  # LinkedIn bot main script
├── config.py                # Bot configuration
├── start_frontend.py        # Startup script
└── requirements.txt         # Python dependencies
```
