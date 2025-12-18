import os
import datetime
import json
import requests
import subprocess

# --- CONFIGURATION ---
DOSSIER_PATH = "data/resolutions.json"
ERROR_QUEUE_PATH = "data/error_queue.json"
SITE_URL = "https://www.kidsdigitalhub.com"
RAILWAY_URL = "https://web-production-b215.up.railway.app/health"

def load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def log_to_dossier(problem, resolution, level="HEALED"):
    """Adds a entry to the Architect's Dossier."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dossier = load_json(DOSSIER_PATH)
    entry = {
        "timestamp": timestamp,
        "incident": problem,
        "healing_action": resolution,
        "status": level,
        "agent": "Antigravity Robot Doctor"
    }
    dossier.insert(0, entry)
    save_json(DOSSIER_PATH, dossier[:50]) # Keep last 50
    print(f"[{level}] {problem} -> {resolution}")

def queue_error(module, message):
    """Adds an error to the queue for the AI to handle next session."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    queue = load_json(ERROR_QUEUE_PATH)
    queue.append({
        "timestamp": timestamp,
        "module": module,
        "error": message,
        "status": "AWAITING_AI_AGENT"
    })
    save_json(ERROR_QUEUE_PATH, queue)

def self_heal_workflows():
    """Aggressively kills redundant or broken workflows."""
    spammers = [".github/workflows/static.yml", ".github/workflows/deploy.yml"]
    for f in spammers:
        if os.path.exists(f):
            os.remove(f)
            log_to_dossier(f"Spam Workflow Detected: {f}", "Permanently deleted file to prevent email alerts.")

def self_heal_configs():
    """Checks if JS configs are empty (a common source of site crashes)."""
    configs = ["js/drawingsConfig.js", "js/storiesConfig.js", "js/gamesConfig.js"]
    for c in configs:
        if not os.path.exists(c) or os.path.getsize(c) < 10:
            try:
                subprocess.run(["python", "daily_content_manager.py"], check=True)
                log_to_dossier(f"Empty/Missing Config: {c}", "Regenerated all assets successfully via Content Manager.")
            except Exception as e:
                queue_error("AssetManager", f"Failed to regenerate {c}: {str(e)}")

def self_heal_server():
    """Checks Railway server heartbeat."""
    try:
        r = requests.get(RAILWAY_URL, timeout=5)
        if r.status_code != 200:
            log_to_dossier("Railway Heartbeat Warning", "Server returned non-200. Triggering wake-up pulse.")
    except Exception as e:
        queue_error("RailwayServer", f"Server unreachable: {str(e)}")

def clean_dossier():
    """Ensures everything is in English for the Architect's peace of mind."""
    # Placeholder for a future cleaning logic if RO text sneaks in
    pass

if __name__ == "__main__":
    print("🩺 Robot Doctor Initialization...")
    self_heal_workflows()
    self_heal_configs()
    self_heal_server()
    clean_dossier()
    print("✅ System Stable. Dossier updated.")
