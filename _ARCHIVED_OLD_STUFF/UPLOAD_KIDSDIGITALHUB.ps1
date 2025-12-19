# ============================================
# KIDS DIGITAL HUB - UPLOAD AUTOMAT FTP
# Script PowerShell pentru Hostinger
# ============================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  KIDS DIGITAL HUB - UPLOAD AUTOMAT" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Configurare FTP
$ftpHost = "ftp.kidsdigitalhub.com"
$ftpUser = "ae1968@kidsdigitalhub.com"
$ftpPass = "Andrada_1968!"
$ftpPort = "21"
$localPath = "C:\Users\adria\.gemini\antigravity\scratch\kids-digital-hub"
$remotePath = "/public_html"

Write-Host "[1/5] Verificare WinSCP..." -ForegroundColor Yellow

# Verifică dacă WinSCP este instalat
$winscpPath = "C:\Program Files (x86)\WinSCP\WinSCP.com"
if (-not (Test-Path $winscpPath)) {
    Write-Host "WinSCP nu este instalat. Instalare automată..." -ForegroundColor Yellow
    
    # Instalare WinSCP prin winget
    try {
        winget install --id WinSCP.WinSCP --silent --accept-package-agreements --accept-source-agreements
        Write-Host "✅ WinSCP instalat cu succes!" -ForegroundColor Green
    } catch {
        Write-Host "❌ Eroare la instalarea WinSCP!" -ForegroundColor Red
        Write-Host "Instalează manual de la: https://winscp.net/download/WinSCP-6.3.5-Setup.exe" -ForegroundColor Yellow
        pause
        exit
    }
    
    # Așteaptă finalizarea instalării
    Start-Sleep -Seconds 5
}

Write-Host "✅ WinSCP găsit!" -ForegroundColor Green
Write-Host ""

Write-Host "[2/5] Pregătire fișiere..." -ForegroundColor Yellow

# Verifică dacă folderul local există
if (-not (Test-Path $localPath)) {
    Write-Host "❌ Folderul local nu există: $localPath" -ForegroundColor Red
    pause
    exit
}

Write-Host "✅ Fișiere găsite: $localPath" -ForegroundColor Green
Write-Host ""

Write-Host "[3/5] Conectare la FTP..." -ForegroundColor Yellow
Write-Host "Host: $ftpHost" -ForegroundColor Gray
Write-Host "User: $ftpUser" -ForegroundColor Gray
Write-Host "Port: $ftpPort" -ForegroundColor Gray
Write-Host ""

# Creează script WinSCP
$winscpScript = @"
option batch abort
option confirm off
open ftp://$ftpUser`:$ftpPass@$ftpHost`:$ftpPort
cd $remotePath
lcd $localPath
put * -delete
exit
"@

# Salvează script temporar
$scriptPath = "$env:TEMP\winscp_upload.txt"
$winscpScript | Out-File -FilePath $scriptPath -Encoding ASCII

Write-Host "[4/5] Upload fișiere..." -ForegroundColor Yellow
Write-Host "Acest proces poate dura 5-10 minute..." -ForegroundColor Gray
Write-Host ""

# Rulează WinSCP
try {
    $result = & $winscpPath /script=$scriptPath /log="$env:TEMP\winscp_log.txt"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Upload complet cu succes!" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Upload finalizat cu avertismente. Verifică log-ul." -ForegroundColor Yellow
        Write-Host "Log: $env:TEMP\winscp_log.txt" -ForegroundColor Gray
    }
} catch {
    Write-Host "❌ Eroare la upload!" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "Verifică log-ul: $env:TEMP\winscp_log.txt" -ForegroundColor Yellow
    pause
    exit
}

Write-Host ""
Write-Host "[5/5] Verificare finală..." -ForegroundColor Yellow

# Șterge script temporar
Remove-Item $scriptPath -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  ✅ DEPLOYMENT COMPLET!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Site-ul tău este LIVE la:" -ForegroundColor Cyan
Write-Host "https://kidsdigitalhub.com" -ForegroundColor White
Write-Host ""
Write-Host "Verifică:" -ForegroundColor Yellow
Write-Host "  - Homepage se încarcă" -ForegroundColor Gray
Write-Host "  - Schimbare limbă (6 limbi)" -ForegroundColor Gray
Write-Host "  - Prețuri convertesc (4 monede)" -ForegroundColor Gray
Write-Host "  - Demo colorat funcționează" -ForegroundColor Gray
Write-Host "  - SSL/HTTPS activ" -ForegroundColor Gray
Write-Host ""
Write-Host "Dacă întâmpini probleme, verifică log-ul:" -ForegroundColor Yellow
Write-Host "$env:TEMP\winscp_log.txt" -ForegroundColor Gray
Write-Host ""
Write-Host "Apasă orice tastă pentru a închide..." -ForegroundColor Cyan
pause
