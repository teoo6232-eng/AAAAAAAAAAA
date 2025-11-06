#!/usr/bin/env python3
"""
Example usage of SUSH tool

This script demonstrates how to use the SUSH Network Analysis Tool
"""

# Simply run the main tool
from sush_tool import main

if __name__ == "__main__":
    print("="*80)
    print("SUSH - Network Analysis Tool")
    print("="*80)
    print()
    print("Instructions:")
    print("1. The GUI will open with a beautiful purple 'SUSH' title")
    print("2. Enter a login page URL (e.g., https://example.com/login)")
    print("3. Click 'ANALYZE' to start")
    print("4. A browser window will open - perform your login there")
    print("5. All network requests will be captured and shown in the GUI")
    print("6. Use the captured data to create your OpenBullet 2 config")
    print()
    print("="*80)
    print()
    
    main()
