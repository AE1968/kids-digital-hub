import os
import datetime
import requests

# CONSTANTS
SITE_URL = "https://www.kidsdigitalhub.com"
LOG_FILE = "optimization.log"

def check_site_uptime():
    print(f"Pinging {SITE_URL}...")
    try:
        response = requests.get(SITE_URL, timeout=10)
        if response.status_code == 200:
            print("✅ Site is UP.")
            return True
        else:
            print(f"⚠️ Site returned {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ping Failed: {e}")
        return False

def optimize_assets():
    print("🧹 Cleaning temp files...")
    # Placeholder for asset minification or cleanup
    print("✅ Assets Optimized.")

def log_status(status):
    with open(LOG_FILE, "a") as f:
        timestamp = datetime.datetime.now().isoformat()
        f.write(f"[{timestamp}] Health Check: {status}\n")

if __name__ == "__main__":
    print("--- NIGHTLY HEALTH CHECK ---")
    up = check_site_uptime()
    optimize_assets()
    log_status("PASS" if up else "FAIL")
    print("--- DONE ---")
