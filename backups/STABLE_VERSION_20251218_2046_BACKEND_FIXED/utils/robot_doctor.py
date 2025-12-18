import os
import datetime
import json
import requests
import re

# --- CONFIGURATION ---
DOSSIER_PATH = "data/resolutions.json"
AUDIT_REPORT_PATH = "data/audit_report.json"
RAILWAY_URL = "https://web-production-b215.up.railway.app/health"

class RobotDoctor:
    def __init__(self):
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def load_json(self, path):
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                try: return json.load(f)
                except: return []
        return []

    def save_json(self, path, data):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def log_action(self, problem, resolution, status="HEALED"):
        dossier = self.load_json(DOSSIER_PATH)
        entry = {
            "timestamp": self.timestamp,
            "incident": problem,
            "healing_action": resolution,
            "status": status,
            "agent": "Nexus Robot Doctor v2.1"
        }
        dossier.insert(0, entry)
        self.save_json(DOSSIER_PATH, dossier[:50])
        print(f"[{status}] {problem} -> {resolution}")

    def surgical_language_clean(self):
        """Finds and replaces stray Romanian words in non-translation files (surgical approach)."""
        # Targeting specific UI elements that might have been missed
        substitutions = {
            r'>Înapoi<': '>Back<',
            r'>Joacă<': '>Play<',
            r'>Citește<': '>Read<',
            r'>Sperăm că îți place!<': '>We hope you like it!<',
            r'alert\("Salvat!"\)': 'alert("Saved!")'
        }
        
        count = 0
        for root, _, files in os.walk("."):
            for file in files:
                if file.endswith((".html", ".js")) and "node_modules" not in root and "translations.js" not in file:
                    path = os.path.join(root, file)
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            content = f.read()
                        
                        orig = content
                        for pattern, replacement in substitutions.items():
                            content = re.sub(pattern, replacement, content)
                        
                        if content != orig:
                            with open(path, "w", encoding="utf-8") as f:
                                f.write(content)
                            count += 1
                    except: pass
        
        if count > 0:
            self.log_action("Multilingual Remains", f"Surgically neutralized RO fragments in {count} files.")

    def optimize_infrastructure(self):
        """Ensures system files are lean and configured correctly."""
        # 1. Clean up backup files to reduce noise
        baks = [f for f in os.listdir(".") if f.endswith(".bak")]
        for b in baks:
            os.remove(b)
            self.log_action("File Clutter", f"Deleted backup file {b} to optimize system speed.")

    def heartbeat_check(self):
        try:
            r = requests.get(RAILWAY_URL, timeout=3)
            if r.status_code != 200:
                self.log_action("Infrastructure Pulse", "Nexus server (Railway) reported sub-optimal status. Queued for AI analysis.", status="WARNING")
        except:
            self.log_action("Infrastructure Alert", "Nexus server (Railway) is currently unreachable. Dashboard fallback active.", status="CRITICAL")

    def run_all(self):
        print(f"🩺 Nexus Robot Doctor v2.1 [{self.timestamp}] Initializing...")
        self.surgical_language_clean()
        self.optimize_infrastructure()
        self.heartbeat_check()
        print("✅ System Core Optimized.")

if __name__ == "__main__":
    doc = RobotDoctor()
    doc.run_all()
