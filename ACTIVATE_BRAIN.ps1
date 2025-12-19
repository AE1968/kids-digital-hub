Write-Output "🚀 INIȚIERE NEXUS BRAIN AUTO-SETUP..."
Write-Output ""

# 1. Install Dependencies
Write-Output "📦 Instalare biblioteci neuronale (Python)..."
pip install fastapi uvicorn google-generativeai pyautogui pillow

# 2. Start the Bridge
Write-Output "🧠 Pornire NEXUS SUPREME BRIDGE..."
Write-Output "Nucleul va fi disponibil la http://localhost:8000"
Write-Output ""
Write-Output "------------------------------------------------"
python nexus_bridge.py
