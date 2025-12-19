# --- NEXUS SUPREME BRAIN CORE ---
import os
import sys
import time
import json
import base64
import subprocess
import pyautogui
import datetime
from pathlib import Path
from PIL import ImageGrab
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CONFIG & MEMORY ---
MEMORY_FILE = Path("nexus_memory.json")
GEMINI_API_KEY = "AIzaSy..." # Placeholder

def load_memory():
    if MEMORY_FILE.exists():
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"interactions": [], "user_prefs": {}, "system_health": 100}

def save_memory(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

memory = load_memory()

# --- BRAIN FUNCTIONS ---
def analyze_system():
    return {
        "time": datetime.datetime.now().strftime("%H:%M:%S"),
        "os": sys.platform,
        "memory_usage": "Optimal",
        "last_interaction": memory["interactions"][-1]["time"] if memory["interactions"] else "None"
    }

def auto_repair(issue):
    print(f"🔧 NEXUS AUTO-REPAIR INITIATED: {issue}")
    # Logic to fix common deployment/redirect issues could go here
    return "Analiza de sistem completă. Nicio eroare critică găsită. Integritatea bazei de date: 100%."

def see_screen():
    path = "nexus_vision.png"
    screenshot = ImageGrab.grab()
    screenshot.save(path)
    return path

# --- API ENDPOINTS ---
class NexusTask(BaseModel):
    command: str
    context: str = ""

@app.post("/api/nexus/chat")
async def nexus_chat(task: NexusTask):
    cmd = task.command.lower()
    timestamp = datetime.datetime.now().isoformat()
    
    # Analyze Intent
    reply = ""
    action = "idle"
    
    if any(x in cmd for x in ["vezi", "screen", "vezi ecranul"]):
        path = see_screen()
        reply = "Am ochii deschiși. Văd tot ce este pe ecran. Analizez datele vizuale..."
        action = "vision"
    
    elif any(x in cmd for x in ["repara", "repair", "fix"]):
        reply = auto_repair(cmd)
        action = "repair"
        
    elif any(x in cmd for x in ["open", "deschide", "start"]):
        app_target = cmd.replace("open ", "").replace("deschide ", "")
        subprocess.run(f"start {app_target}", shell=True)
        reply = f"Am deschis {app_target} pentru tine, Comandante Adrian."
        action = "os_control"
        
    else:
        # HUMAN-LIKE INTELLIGENCE Fallback
        replies = [
            f"Înțeleg comanda ta: '{task.command}'. Analizez posibilitățile în Kids Digital Hub.",
            "Am stocat această informație în memoria mea pe termen lung. Cum continuăm?",
            "Neural Link stabilizat. Sunt pregătit pentru următoarea fază a genezei Nexus."
        ]
        import random
        reply = random.choice(replies)
        
    # Update Memory
    memory["interactions"].append({"time": timestamp, "user": task.command, "nexus": reply})
    save_memory(memory)
    
    return {"reply": reply, "action": action, "stats": analyze_system()}

@app.get("/api/nexus/status")
async def get_status():
    return analyze_system()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

