$desktopPath = [Environment]::GetFolderPath("Desktop")
$sourcePath = "C:\Users\adria\.gemini\antigravity\scratch\kids-digital-hub\START_MANAGER_V2.py"
$targetLink = Join-Path $desktopPath "KIDS_HUB_ADMIN.bat"
$projectDir = "C:\Users\adria\.gemini\antigravity\scratch\kids-digital-hub"

# 1. Cleanup Old Version
if (Test-Path $targetLink) {
    Remove-Item $targetLink -Force
    Write-Host "🗑️ Old version removed."
}

# 2. Create New Launcher
$content = "@echo off`r`ncd /d `"$projectDir`"`r`npython START_MANAGER_V2.py"
Set-Content -Path $targetLink -Value $content

Write-Host "✅ SUCCESS! Latest Admin Panel placed on Desktop."
Start-Sleep -Seconds 3
