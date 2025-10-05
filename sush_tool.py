#!/usr/bin/env python3
"""
SUSH - Network Analysis Tool for OpenBullet 2 Config Creation
A powerful tool to analyze login page network traffic and generate config data
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
import threading
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import webbrowser

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from seleniumwire import webdriver as wiredriver
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False


class SushNetworkAnalyzer:
    """Network analyzer for capturing login requests"""
    
    def __init__(self):
        self.captured_requests = []
        self.driver = None
        
    def analyze_url(self, url, callback):
        """Analyze network traffic for a given URL"""
        if not SELENIUM_AVAILABLE:
            callback("Error: selenium and selenium-wire are required. Install with: pip install selenium selenium-wire")
            return
            
        def run_analysis():
            try:
                callback("Starting browser and navigating to URL...\n")
                
                # Setup selenium-wire options
                options = {
                    'disable_encoding': True,
                }
                
                # Setup Chrome options
                chrome_options = Options()
                chrome_options.add_argument('--ignore-certificate-errors')
                chrome_options.add_argument('--ignore-ssl-errors')
                
                # Create driver with selenium-wire
                self.driver = wiredriver.Chrome(
                    seleniumwire_options=options,
                    options=chrome_options
                )
                
                # Navigate to URL
                self.driver.get(url)
                callback(f"Navigated to: {url}\n")
                callback("Waiting for page to load...\n")
                
                # Wait a bit for page to load
                import time
                time.sleep(3)
                
                callback("\n=== CAPTURED NETWORK REQUESTS ===\n\n")
                
                # Capture all requests
                for request in self.driver.requests:
                    if request.response:
                        self.captured_requests.append(request)
                        
                        req_info = {
                            'url': request.url,
                            'method': request.method,
                            'headers': dict(request.headers),
                            'response_status': request.response.status_code,
                            'response_headers': dict(request.response.headers)
                        }
                        
                        # Get POST data if available
                        if request.body:
                            try:
                                req_info['body'] = request.body.decode('utf-8')
                            except:
                                req_info['body'] = str(request.body)
                        
                        # Display the request
                        callback(f"\n{'='*80}\n")
                        callback(f"URL: {request.url}\n")
                        callback(f"Method: {request.method}\n")
                        callback(f"Status: {request.response.status_code}\n")
                        
                        # Show important headers
                        callback("\nRequest Headers:\n")
                        for key, value in request.headers.items():
                            callback(f"  {key}: {value}\n")
                        
                        if request.body:
                            callback(f"\nRequest Body:\n{req_info['body']}\n")
                        
                        # Show response headers
                        callback("\nResponse Headers:\n")
                        for key, value in request.response.headers.items():
                            callback(f"  {key}: {value}\n")
                        
                        callback(f"\n{'='*80}\n")
                
                callback(f"\n\nTotal requests captured: {len(self.captured_requests)}\n")
                callback("\n=== ANALYSIS COMPLETE ===\n")
                callback("\nBrowser window is still open. You can interact with the login form.\n")
                callback("Perform a login to capture the login request!\n")
                callback("Close the browser window when done.\n")
                
                # Keep browser open for user interaction
                input("Press Enter in terminal to close browser and finish...")
                
            except Exception as e:
                callback(f"Error during analysis: {str(e)}\n")
                callback(f"Make sure Chrome/Chromium is installed and chromedriver is in PATH.\n")
            finally:
                if self.driver:
                    self.driver.quit()
                    callback("\nBrowser closed.\n")
        
        # Run in thread to not block UI
        thread = threading.Thread(target=run_analysis, daemon=True)
        thread.start()


class SushGUI:
    """Beautiful GUI for SUSH tool"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SUSH - Network Analysis Tool")
        self.root.geometry("1000x700")
        self.root.configure(bg='#1a1a2e')
        
        self.analyzer = SushNetworkAnalyzer()
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the GUI components"""
        
        # Title Frame with purple gradient effect
        title_frame = tk.Frame(self.root, bg='#1a1a2e', height=120)
        title_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        title_frame.pack_propagate(False)
        
        # Main title "SUSH" in beautiful purple
        title_label = tk.Label(
            title_frame,
            text="SUSH",
            font=("Arial", 72, "bold"),
            fg="#9b59b6",  # Purple color
            bg='#1a1a2e'
        )
        title_label.pack(expand=True)
        
        # Subtitle
        subtitle_label = tk.Label(
            title_frame,
            text="Network Analysis Tool for OpenBullet 2",
            font=("Arial", 14),
            fg="#bb86fc",  # Lighter purple
            bg='#1a1a2e'
        )
        subtitle_label.place(relx=0.5, rely=0.75, anchor='center')
        
        # Input Frame
        input_frame = tk.Frame(self.root, bg='#16213e', relief=tk.RAISED, bd=2)
        input_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # URL Label
        url_label = tk.Label(
            input_frame,
            text="Login URL:",
            font=("Arial", 12, "bold"),
            fg="#bb86fc",
            bg='#16213e'
        )
        url_label.pack(side=tk.LEFT, padx=(10, 5), pady=10)
        
        # URL Entry
        self.url_entry = tk.Entry(
            input_frame,
            font=("Arial", 11),
            bg='#0f3460',
            fg='white',
            insertbackground='white',
            relief=tk.FLAT,
            bd=5
        )
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=10)
        self.url_entry.insert(0, "https://example.com/login")
        
        # Analyze Button
        self.analyze_btn = tk.Button(
            input_frame,
            text="🔍 ANALYZE",
            font=("Arial", 11, "bold"),
            bg='#9b59b6',
            fg='white',
            activebackground='#7d3c98',
            activeforeground='white',
            relief=tk.FLAT,
            bd=0,
            padx=20,
            command=self.start_analysis
        )
        self.analyze_btn.pack(side=tk.LEFT, padx=(5, 10), pady=10)
        
        # Info Frame
        info_frame = tk.Frame(self.root, bg='#16213e', relief=tk.RAISED, bd=2)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))
        
        # Info Label
        info_title = tk.Label(
            info_frame,
            text="📊 Network Traffic Analysis",
            font=("Arial", 12, "bold"),
            fg="#bb86fc",
            bg='#16213e'
        )
        info_title.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        # Scrolled Text for output
        self.output_text = scrolledtext.ScrolledText(
            info_frame,
            font=("Consolas", 9),
            bg='#0f3460',
            fg='#e0e0e0',
            insertbackground='white',
            relief=tk.FLAT,
            bd=5,
            wrap=tk.WORD
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Initial instructions
        self.display_instructions()
        
        # Status bar
        status_frame = tk.Frame(self.root, bg='#16213e', height=30)
        status_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready to analyze network traffic",
            font=("Arial", 9),
            fg="#bb86fc",
            bg='#16213e',
            anchor=tk.W
        )
        self.status_label.pack(fill=tk.X, padx=10, pady=5)
        
    def display_instructions(self):
        """Display initial instructions"""
        instructions = """
╔══════════════════════════════════════════════════════════════════════════════════╗
║                    WELCOME TO SUSH - NETWORK ANALYSIS TOOL                       ║
╚══════════════════════════════════════════════════════════════════════════════════╝

🎯 PURPOSE:
   This tool helps you analyze network traffic from login pages to create
   OpenBullet 2 configurations.

📋 HOW TO USE:
   1. Enter the login page URL in the field above
   2. Click "ANALYZE" to start capturing network traffic
   3. A browser window will open - perform your login
   4. All network requests will be captured and displayed here
   5. Use the captured data to create your OpenBullet 2 config

🔍 WHAT IT CAPTURES:
   ✓ All HTTP/HTTPS requests
   ✓ Request headers (User-Agent, Cookies, etc.)
   ✓ POST data (login credentials format)
   ✓ Response headers
   ✓ Status codes
   ✓ URLs and endpoints

⚠️  REQUIREMENTS:
   - Python packages: selenium, selenium-wire
   - Chrome/Chromium browser
   - chromedriver in PATH

💡 TIP:
   Look for POST requests to login endpoints. They contain the format
   for credentials, CSRF tokens, and other important data for your config.

════════════════════════════════════════════════════════════════════════════════════

Ready to start? Enter a URL and click ANALYZE!
"""
        self.output_text.insert(tk.END, instructions)
        
    def append_output(self, text):
        """Append text to output"""
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)
        self.root.update_idletasks()
        
    def start_analysis(self):
        """Start network analysis"""
        url = self.url_entry.get().strip()
        
        if not url:
            messagebox.showwarning("Warning", "Please enter a URL")
            return
            
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, url)
        
        # Clear output
        self.output_text.delete(1.0, tk.END)
        
        # Update status
        self.status_label.config(text=f"Analyzing: {url}")
        self.analyze_btn.config(state=tk.DISABLED)
        
        # Start analysis
        self.analyzer.analyze_url(url, self.append_output)
        
        # Re-enable button after a delay
        self.root.after(2000, lambda: self.analyze_btn.config(state=tk.NORMAL))
        
    def run(self):
        """Run the GUI"""
        self.root.mainloop()


def main():
    """Main entry point"""
    print("=" * 80)
    print("SUSH - Network Analysis Tool for OpenBullet 2")
    print("=" * 80)
    print()
    
    # Check dependencies
    if not SELENIUM_AVAILABLE:
        print("⚠️  WARNING: selenium and selenium-wire not installed")
        print("Install with: pip install selenium selenium-wire")
        print()
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            return
    
    # Launch GUI
    app = SushGUI()
    app.run()


if __name__ == "__main__":
    main()
