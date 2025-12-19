Write-Host "🚀 STARTING AUTOMATED DEPLOYMENT..." -ForegroundColor Cyan

# 1. GIT SYNC
Write-Host "1. 💾 Saving changes to Git..." -ForegroundColor Yellow
git add .
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
git commit -m "Auto-Deploy: $timestamp (Standard update)"
# Only push if commit succeeded, but git push is safe to run anyway usually
git push origin main
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Git Push Successful" -ForegroundColor Green
}
else {
    Write-Host "⚠️ Git Push Warning (Continuing to Netlify deploy...)" -ForegroundColor Yellow
}

# 2. NETLIFY DEPLOY
Write-Host "2. 🌍 Deploying to Netlify Production..." -ForegroundColor Yellow
# Using --dir . to ensure we deploy the current folder content
# Using --prod to go straight to live URL
# The netlify command usually returns 0 on success
cmd /c "netlify deploy --prod --dir ."

if ($LASTEXITCODE -eq 0) {
    Write-Host " "
    Write-Host "🎉 SUCCESS! Site is live at: https://kidsdigitalhub.com" -ForegroundColor Green
    Write-Host " "
}
else {
    Write-Host "❌ Netlify Deploy Failed with error code $LASTEXITCODE" -ForegroundColor Red
}

# Script finished. Exiting automatically for automation purposes.

