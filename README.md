# AAAAAAAAAAA

## SUSH - Network Analysis Tool for OpenBullet 2

A powerful tool with a beautiful GUI to analyze login page network traffic and help create OpenBullet 2 configurations.

### Features

- 🎨 **Beautiful Purple GUI** - Modern, dark-themed interface with "SUSH" prominently displayed in purple
- 🔍 **Network Traffic Capture** - Captures all HTTP/HTTPS requests and responses
- 📊 **Detailed Analysis** - Shows headers, cookies, POST data, status codes, and more
- 🌐 **Browser Integration** - Opens a real browser to interact with login pages
- 💾 **Complete Data Capture** - Get all the information needed for OpenBullet 2 configs

### Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Make sure you have Chrome/Chromium browser installed
4. Install chromedriver (must be in PATH):
   - Ubuntu/Debian: `sudo apt-get install chromium-chromedriver`
   - macOS: `brew install chromedriver`
   - Windows: Download from https://chromedriver.chromium.org/

### Usage

Run the tool:
```bash
python sush_tool.py
```

1. Enter the login page URL
2. Click "ANALYZE" 
3. A browser window will open
4. Perform the login in the browser
5. All network traffic will be captured and displayed
6. Use the captured data to create your OpenBullet 2 configuration

### What It Captures

- Request URLs and methods (GET, POST, etc.)
- Request headers (User-Agent, Referer, Cookies, etc.)
- POST data (login credentials format, CSRF tokens, etc.)
- Response status codes
- Response headers
- All network requests during the login process

### Tips for OpenBullet 2

- Look for POST requests to login endpoints
- Note the parameter names for username/password
- Check for CSRF tokens or hidden form fields
- Observe cookie handling and session management
- Pay attention to request headers that might be required

### Screenshots

The GUI features:
- Large "SUSH" title in beautiful purple (#9b59b6)
- Dark theme for comfortable viewing
- Real-time network traffic display
- Clean and modern interface

### Requirements

- Python 3.7+
- selenium
- selenium-wire
- Chrome/Chromium browser
- chromedriver

### License

Open source - feel free to use and modify!