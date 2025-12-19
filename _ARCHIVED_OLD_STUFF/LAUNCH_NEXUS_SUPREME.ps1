# NEXUS SUPREME - MASTER LAUNCHER
# Created for Commander Adrian

$ProjectDir = "C:\Users\adria\.gemini\antigravity\scratch\kids-digital-hub"
$BridgeFile = "nexus_bridge.py"

Write-Host "🚀 INITIATING NEXUS SUPREME NEURAL LINK..." -ForegroundColor Cyan

# 1. Kill any existing instances
Stop-Process -Name "python" -ErrorAction SilentlyContinue

# 2. Start the Bridge in a new window
# We use 'python' to start the bridge
Start-Process "python" -ArgumentList "$ProjectDir\$BridgeFile" -WorkingDirectory $ProjectDir -WindowStyle Hidden

Write-Host "📡 SYNCING WITH GLOBAL HUB..." -ForegroundColor Green
Start-Sleep -Seconds 4

# 3. Open the Nexus Interface
Start-Process "https://www.kidsdigitalhub.com/nexus_v2.html"

Write-Host "✨ NEURAL CONNECTION ESTABLISHED. WELCOME, COMMANDER." -ForegroundColor Yellow
Start-Sleep -Seconds 2
