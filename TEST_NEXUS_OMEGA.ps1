# NEXUS PROTOCOL OMEGA - Auto Test Script
# Opens browser and provides testing instructions

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  NEXUS PROTOCOL OMEGA - AUTO TESTER  " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# URLs to test
$localUrl = "file:///$PWD/nexus_core.html" -replace '\\', '/'
$liveUrl = "https://www.kidsdigitalhub.com/nexus_core.html"

Write-Host "Available Test Options:" -ForegroundColor Yellow
Write-Host "1. Test LOCAL version (file://)" -ForegroundColor Green
Write-Host "2. Test LIVE version (https://)" -ForegroundColor Green
Write-Host "3. Test BOTH versions" -ForegroundColor Green
Write-Host ""

$choice = Read-Host "Select option (1/2/3)"

function Open-BrowserWithInstructions {
    param($url, $type)
    
    Write-Host ""
    Write-Host "Opening $type version..." -ForegroundColor Cyan
    Write-Host "URL: $url" -ForegroundColor Gray
    Write-Host ""
    
    # Try to open in default browser
    Start-Process $url
    
    Start-Sleep -Seconds 2
    
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host "  TESTING INSTRUCTIONS" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "STEP 1: Allow Permissions" -ForegroundColor Green
    Write-Host "  - When browser asks, click ALLOW for:" -ForegroundColor White
    Write-Host "    * Microphone access" -ForegroundColor Gray
    Write-Host "    * Camera access" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "STEP 2: Wait for Voice Activation" -ForegroundColor Green
    Write-Host "  - Look for message in chat:" -ForegroundColor White
    Write-Host "    'Voice activation ready. Say Hey Nexus...'" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "STEP 3: Activate Protocol Omega" -ForegroundColor Green
    Write-Host "  - Say clearly: 'Hey Nexus'" -ForegroundColor White
    Write-Host "  - Or try: 'Hei Nexus' (Romanian)" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "STEP 4: Verify Camera Activation" -ForegroundColor Green
    Write-Host "  - Nexus eyes should turn GREEN" -ForegroundColor White
    Write-Host "  - Status: 'CAMERA ACTIVE'" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "STEP 5: Face Recognition" -ForegroundColor Green
    Write-Host "  - Look at camera" -ForegroundColor White
    Write-Host "  - Wait for scanning..." -ForegroundColor Gray
    Write-Host "  - If first time: Enter password '196816'" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "STEP 6: Test Contact System" -ForegroundColor Green
    Write-Host "  - Click AE logo (top-right corner)" -ForegroundColor White
    Write-Host "  - Verify contact modal opens" -ForegroundColor Gray
    Write-Host "  - Check gesture changes to HAPPY (yellow)" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host "  WHAT TO VERIFY" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "[✓] Page loads completely" -ForegroundColor White
    Write-Host "[✓] Nexus avatar visible and animated" -ForegroundColor White
    Write-Host "[✓] AE logo in top-right corner" -ForegroundColor White
    Write-Host "[✓] Voice activation message appears" -ForegroundColor White
    Write-Host "[✓] 'Hey Nexus' triggers Protocol Omega" -ForegroundColor White
    Write-Host "[✓] Eyes turn GREEN when camera active" -ForegroundColor White
    Write-Host "[✓] Face recognition works" -ForegroundColor White
    Write-Host "[✓] Gestures change based on context" -ForegroundColor White
    Write-Host "[✓] Contact modal opens on logo click" -ForegroundColor White
    Write-Host ""
}

switch ($choice) {
    "1" {
        Open-BrowserWithInstructions $localUrl "LOCAL"
    }
    "2" {
        Open-BrowserWithInstructions $liveUrl "LIVE"
    }
    "3" {
        Open-BrowserWithInstructions $localUrl "LOCAL"
        Write-Host ""
        Write-Host "Press Enter to open LIVE version..." -ForegroundColor Yellow
        Read-Host
        Open-BrowserWithInstructions $liveUrl "LIVE"
    }
    default {
        Write-Host "Invalid choice. Opening LIVE version..." -ForegroundColor Red
        Open-BrowserWithInstructions $liveUrl "LIVE"
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  TROUBLESHOOTING" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "If voice activation doesn't work:" -ForegroundColor Yellow
Write-Host "  - Use Chrome or Edge browser" -ForegroundColor White
Write-Host "  - Check microphone permissions" -ForegroundColor White
Write-Host "  - Speak clearly and close to mic" -ForegroundColor White
Write-Host ""
Write-Host "If camera doesn't start:" -ForegroundColor Yellow
Write-Host "  - Check camera permissions" -ForegroundColor White
Write-Host "  - Close other apps using camera" -ForegroundColor White
Write-Host "  - Reload the page" -ForegroundColor White
Write-Host ""
Write-Host "If face-api.js doesn't load:" -ForegroundColor Yellow
Write-Host "  - Check internet connection" -ForegroundColor White
Write-Host "  - Wait 2-3 seconds for models" -ForegroundColor White
Write-Host "  - Check browser console (F12)" -ForegroundColor White
Write-Host ""

Write-Host "========================================" -ForegroundColor Green
Write-Host "  Testing in progress..." -ForegroundColor Green
Write-Host "  Press Ctrl+C to exit this script" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Keep script running
Read-Host "Press Enter when testing is complete"

Write-Host ""
Write-Host "Thank you for testing Nexus Protocol Omega!" -ForegroundColor Cyan
Write-Host "Report any issues to: ae1968@kidsdigitalhub.com" -ForegroundColor Gray
Write-Host ""
