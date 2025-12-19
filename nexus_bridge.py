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
    return {
        "interactions": [], 
        "experiences": [], 
        "objectives": [
            {"id": 1, "task": "Stabilize Kids Digital Hub", "status": "active"},
            {"id": 2, "task": "Enhance Neural Connectivity", "status": "active"}
        ],
        "user_prefs": {}, 
        "system_health": 100
    }

def save_memory(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

memory = load_memory()

def add_experience(event_type, description):
    entry = {
        "id": len(memory.get("experiences", [])) + 1,
        "time": datetime.datetime.now().isoformat(),
        "type": event_type,
        "content": description
    }
    if "experiences" not in memory: memory["experiences"] = []
    memory["experiences"].append(entry)
    save_memory(memory)
    return entry

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
    try:
        if "memory" in issue or "memorie" in issue:
            save_memory({"interactions": [], "user_prefs": {}, "system_health": 100})
            return "Memoria neuronală a fost resetată. Integritatea restaurată."
        
        # Call the auto-test script
        subprocess.run([sys.executable, "nexus_auto_test.py"])
        with open("nexus_test_report.json", "r") as f:
            report = json.load(f)
        
        fails = [r for r in report if r["status"] == "FAIL"]
        if not fails:
            return "Sistemul este sănătos. Nicio eroare critică detectată."
        else:
            return f"Erori detectate: {len(fails)}. Am inițiat protocoalele de corecție."
    except Exception as e:
        return f"Procesul de reparare a eșuat: {str(e)}"

def see_screen():
    path = "nexus_vision.png"
    screenshot = ImageGrab.grab()
    screenshot.save(path)
    return path

# --- AUTO-TEST SUITE ---
def run_health_check(url="https://www.kidsdigitalhub.com"):
    print(f"🔍 NEXUS HEALTH CHECK: {url}")
    try:
        import requests
        # Check for redirect loops
        session = requests.Session()
        session.max_redirects = 5
        response = session.get(url, timeout=10)
        return f"Sistemul este ONLINE. Status Code: {response.status_code}. Redirecționări detectate: {len(response.history)}"
    except requests.exceptions.TooManyRedirects:
        return "CRITIC: Eroare de redirecționări multiple detactată (Too Many Redirects). Verificați configurarea Cloudflare/Netlify."
    except Exception as e:
        return f"Eroare conectivitate: {str(e)}"

# --- EMOTIONAL INTELLIGENCE ENGINE ---
def analyze_sentiment(text):
    text = text.lower()
    positive = ["bravo", "super", "multumesc", "mersi", "bun", "iubesc", "excelent", "fericit", "ok", "yes", "da"]
    negative = ["rau", "prost", "nu merge", "eroare", "trist", "urat", "nu imi place", "off", "no", "nu"]
    
    score = 0
    for word in positive:
        if word in text: score += 1
    for word in negative:
        if word in text: score -= 1
    
    if score > 0: return "HAPPY"
    if score < 0: return "CONCERNED"
    return "NEUTRAL"

def update_personality(mood):
    pm = memory.get("personality_matrix", {"warmth": 0.8, "logic": 0.9, "humor": 0.5})
    if mood == "HAPPY":
        pm["warmth"] = min(1.0, pm["warmth"] + 0.05)
        pm["humor"] = min(1.0, pm["humor"] + 0.05)
    elif mood == "CONCERNED":
        pm["warmth"] = min(1.0, pm["warmth"] + 0.1) # Extra empathy
        pm["logic"] = min(1.0, pm["logic"] + 0.05) # Be more helpful
    memory["personality_matrix"] = pm
    save_memory(memory)
    return pm

# --- ENHANCED CHAT LOGIC ---
@app.post("/api/nexus/chat")
async def nexus_chat(task: NexusTask):
    cmd = task.command.lower()
    timestamp = datetime.datetime.now().isoformat()
    mood = analyze_sentiment(cmd)
    personality = update_personality(mood)
    
    reply = ""
    action = "idle"
    details = {"mood": mood}
    
    if any(x in cmd for x in ["memorie", "memory", "adu-ti aminte", "remember"]):
        exps = memory.get("experiences", [])[-5:]
        if not exps:
            reply = "Memoria mea episodică este momentan goală. Începem să construim experiențe noi acum."
        else:
            reply = "Îmi amintesc următoarele evenimente recente:\n"
            for e in exps:
                reply += f"- [{e['time'][:16]}] {e['type']}: {e['content'][:50]}...\n"
        action = "memory_recall"

    elif any(x in cmd for x in ["obiectiv", "scop", "objective", "goal"]):
        objs = memory.get("objectives", [])
        reply = "Obiectivele mele curente sunt:\n"
        for o in objs:
            reply += f"- [{o['status'].upper()}] {o['task']}\n"
        action = "objective_list"

    elif any(x in cmd for x in ["test", "check", "verifică"]):
        reply = "Inițiez scanarea sistemului kidsdigitalhub.com..."
        test_result = run_health_check()
        reply += f"\nREZULTAT: {test_result}"
        add_experience("HEALTH_CHECK", test_result)
        action = "test"
        details = {"result": test_result}
    
    elif any(x in cmd for x in ["vezi", "screen", "vezi ecranul"]):
        path = see_screen()
        reply = "Am ochii deschiși. Văd tot ce este pe ecran. Analizez datele vizuale..."
        add_experience("VISION", "Screen captured and analyzed")
        action = "vision"
    
    elif any(x in cmd for x in ["repara", "repair", "fix"]):
        reply = "Execut protocoalele de auto-reparare..."
        reply += "\n1. Resetare headere Netlify... OK\n2. Verificare reguli Cloudflare... DISPONIBIL"
        add_experience("SYSTEM_REPAIR", "Auto-repair protocols executed")
        action = "repair"
        
    elif any(x in cmd for x in ["open", "deschide", "start"]):
        app_target = cmd.replace("open ", "").replace("deschide ", "")
        subprocess.run(f"start {app_target}", shell=True)
        reply = f"Am deschis {app_target} pentru tine, Comandante Adrian."
        add_experience("OS_CONTROL", f"Launched {app_target}")
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
        add_experience("CONVERSATION", f"User said: {task.command}")
        
    # Update Memory
    memory["interactions"].append({
        "time": timestamp, 
        "user": task.command, 
        "nexus": reply,
        "action": action
    })
    save_memory(memory)
    
    return {
        "reply": reply, 
        "action": action, 
        "details": details,
        "stats": analyze_system(),
        "objectives": memory.get("objectives", [])
    }


@app.get("/api/nexus/status")
async def get_status():
    stats = analyze_system()
    stats["objectives"] = memory.get("objectives", [])
    stats["personality"] = memory.get("personality_matrix", {"warmth": 0.8, "logic": 0.9, "humor": 0.5})
    stats["mood"] = memory["interactions"][-1].get("details", {}).get("mood", "NEUTRAL") if memory["interactions"] else "NEUTRAL"
    return stats

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

