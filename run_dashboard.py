"""
run_dashboard.py
----------------
Convenience launcher for the India Unemployment Analysis Localhost Dashboard.
Runs on http://localhost:5005 by default.
"""

import os
import sys
import webbrowser

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from app.app import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5005))
    host = '127.0.0.1'
    url = f"http://{host}:{port}"
    
    print("=" * 70)
    print("   INDIA UNEMPLOYMENT ANALYSIS & COVID-19 SHOCK DASHBOARD   ")
    print("=" * 70)
    print(f"\n[+] Localhost Server starting at: {url}")
    print("[+] Press CTRL+C to stop the server at any time.\n")

    # Start Flask application
    app.run(host=host, port=port, debug=False)
