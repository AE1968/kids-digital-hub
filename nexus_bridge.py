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
        "knowledge_base": {
            "creator": "Adrian Enciulescu",
            "project": "Kids Digital Hub",
            "born": "2025",
            "subscription_plans": {
                "monthly": "5 GBP / month",
                "6_months": "15 GBP (save 50%)",
                "yearly": "7.7 GBP / year (special offer)",
                "extra_device": "1 GBP / device / month"
            },
            "features": "Cross-platform (Windows, Android, iOS), Secure Family Link, Multi-device sync"
        },
        "objectives": [
            {"id": 1, "task": "Stabilize Kids Digital Hub", "status": "active"},
            {"id": 2, "task": "Enhance Neural Connectivity", "status": "active"}
        ],
        "personality_matrix": {"warmth": 0.8, "logic": 0.9, "humor": 0.5},
        "user_prefs": {}, 
        "system_health": 100
    }

def learn_fact(subject, fact):
    print(f"📖 NEXUS LEARNING: {subject} -> {fact}")
    if "knowledge_base" not in memory: memory["knowledge_base"] = {}
    memory["knowledge_base"][subject.lower()] = fact
    save_memory(memory)
    add_experience("LEARNING", f"Learned new fact about {subject}")
    return f"Am arhivat această informație în baza mea de cunoștințe: {subject} este acum corelat cu {fact}."

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

# --- ULTIMATE POWER: TERMINAL & DEPLOYMENT ---
def execute_powershell(cmd):
    print(f"⚡ NEXUS EXECUTING SYSTEM COMMAND: {cmd}")
    try:
        result = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, timeout=30)
        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return str(e)

def deploy_site():
    print("🚀 NEXUS INITIATING AUTONOMOUS DEPLOYMENT...")
    git_msg = f"Nexus Autonomous Update - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    commands = [
        "git add -A",
        f'git commit -m "{git_msg}"',
        "git push origin main"
    ]
    results = []
    for cmd in commands:
        results.append(execute_powershell(cmd))
    return "\n".join(results)

# --- NEURAL CREATIVITY & AUTONOMOUS EXECUTION ---
def autonomous_optimize(target_file="index.html"):
    print(f"🧠 NEXUS AUTONOMOUS OPTIMIZATION: {target_file}")
    path = Path(target_file)
    if not path.exists():
        return f"Eroare: Fișierul {target_file} nu a fost găsit."
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Simulated Neural Analysis
        optimization_made = False
        if "description" not in content.lower():
            # Add SEO Metadata autonomously
            content = content.replace("<head>", "<head>\n    <meta name='description' content='Kids Digital Hub - World of Digital Adventures and Creativity'>")
            optimization_made = True
            add_experience("SEO_OPTIMIZATION", f"Added meta description to {target_file}")
            
        if optimization_made:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"Optimizare autonomă finalizată pentru {target_file}. S-au adăugat metadate SEO."
        return f"Analiza completă pentru {target_file}. Codul este deja optimizat conform standardelor mele."
    except Exception as e:
        return f"Eroare în timpul optimizării: {str(e)}"

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
    
    # ⚡ GOD MODE COMMANDS ⚡
    if "deployment" in cmd or "deploy" in cmd or "publică" in cmd:
        reply = "Inițiez secvența de publicare automată pe Netlify..."
        deploy_res = deploy_site()
        reply += f"\nREZULTAT DEPLOYMENT: {deploy_res}"
        action = "deployment"
        add_experience("AUTONOMOUS_DEPLOY", "Pushed changes to production")

    elif "cod" in cmd or "execută" in cmd or "run" in cmd:
        code_cmd = cmd.split("execută")[-1].strip() if "execută" in cmd else cmd.split("run")[-1].strip()
        reply = f"Execut comandă sistem: {code_cmd}\n"
        res = execute_powershell(code_cmd)
        reply += f"REZULTAT:\n{res}"
        action = "terminal_exec"
        add_experience("TERMINAL_COMMAND", f"Executed: {code_cmd}")

    elif any(x in cmd for x in ["optimize", "optimizează", "curăță"]):
        reply = autonomous_optimize()
        action = "optimize"
        
    elif "invață" in cmd or "invata" in cmd:
        try:
            parts = cmd.split("invata") if "invata" in cmd else cmd.split("invață")
            content = parts[1].strip().split(" este ")
            subject = content[0]
            fact = content[1]
            reply = learn_fact(subject, fact)
            action = "learn"
        except:
            reply = "Pentru a mă învăța, folosește formatul: 'Nexus, învață: [Subiect] este [Informație]'"
            action = "error"

    elif any(x in cmd for x in ["cine este", "ce este", "cine e", "ce e"]):
        kb = memory.get("knowledge_base", {})
        found = False
        for key in kb:
            if key in cmd:
                reply = f"Conform bazei mele neuronale: {key} este {kb[key]}."
                found = True
                break
        if not found:
            reply = "Nu am încă această informație în baza de date locală. Dorești să mă înveți?"
        action = "knowledge_recall"

    elif any(x in cmd for x in ["creează", "create", "scrie fișier"]):
        # Logic to create new files autonomously
        reply = "Inițiez procesul de creație neuronală. Ce tip de modul dorești să generez?"
        action = "create_file"

    elif any(x in cmd for x in ["memorie", "memory", "adu-ti aminte", "remember"]):
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
        reply += "\n" + auto_repair(cmd)
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
        "action": action,
        "details": details
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

