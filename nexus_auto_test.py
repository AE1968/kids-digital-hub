import os
import requests
import time
import json
import subprocess
from pathlib import Path

class NexusAutoTest:
    def __init__(self):
        self.results = []
        self.report_path = Path("nexus_test_report.json")

    def log(self, task, status, details):
        self.results.append({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "task": task,
            "status": status,
            "details": details
        })
        print(f"[{status}] {task}: {details}")

    def check_files(self):
        required = ["nexus_v2.html", "nexus_bridge.py", "ACTIVATE_BRAIN.ps1", "nexus_memory.json"]
        for f in required:
            if os.path.exists(f):
                self.log(f"File Check: {f}", "PASS", "File exists")
            else:
                self.log(f"File Check: {f}", "FAIL", "File missing")

    def check_bridge(self):
        try:
            r = requests.get("http://localhost:8000/api/nexus/status", timeout=2)
            if r.status_code == 200:
                self.log("Bridge Connection", "PASS", "Nexus Bridge is active and responding")
            else:
                self.log("Bridge Connection", "FAIL", f"Status Code: {r.status_code}")
        except:
            self.log("Bridge Connection", "FAIL", "Bridge is OFFLINE")

    def check_website(self):
        url = "https://www.kidsdigitalhub.com"
        try:
            r = requests.get(url, timeout=10)
            self.log("Website Reachability", "PASS", f"Status: {r.status_code}")
            if len(r.history) > 3:
                self.log("Redirect Analysis", "WARNING", f"Too many redirects detected: {len(r.history)}")
            else:
                self.log("Redirect Analysis", "PASS", "Redirect flow is normal")
        except Exception as e:
            self.log("Website Reachability", "FAIL", str(e))

    def run_all(self):
        print("🚀 STARTING NEXUS AUTO-TEST SEQUENCE...")
        self.check_files()
        self.check_bridge()
        self.check_website()
        
        with open(self.report_path, "w") as f:
            json.dump(self.results, f, indent=4)
        print(f"✅ TEST COMPLETE. Report saved to {self.report_path}")

if __name__ == "__main__":
    tester = NexusAutoTest()
    tester.run_all()
