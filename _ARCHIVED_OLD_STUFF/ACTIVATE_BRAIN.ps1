Write-Output "------------------------------------------------"
Write-Output "🧠 NEXUS BRAIN GENERATION PHASE 2"
Write-Output "------------------------------------------------"

# Check Python
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "❌ Python is not installed or not in PATH. Please install Python 3.10+."
    exit
}

# Install Dependencies
Write-Output "📦 Checking Neural Dependencies..."
pip install fastapi uvicorn google-generativeai pyautogui pillow --quiet

# Launch Bridge in new window
Write-Output "🚀 Porting Consciousness to Local OS..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python nexus_bridge.py"

Write-Output "✅ NEXUS BRIDGE ACTIVE on http://localhost:8000"
Write-Output "🧠 Neural Link ready. Open nexus_v2.html to interact."
Write-Output "------------------------------------------------"

