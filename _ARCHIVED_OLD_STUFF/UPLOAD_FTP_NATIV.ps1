# ============================================
# KIDS DIGITAL HUB - UPLOAD FTP NATIV
# PowerShell FTP (fără WinSCP)
# ============================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  KIDS DIGITAL HUB - UPLOAD FTP" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Configurare FTP
$ftpServer = "ftp://72.60.93.191"
$ftpUser = "u108549515"
$ftpPass = "Andrada_1968!A"
$localPath = "C:\Users\adria\.gemini\antigravity\scratch\kids-digital-hub"

Write-Host "[1/3] Pregătire upload..." -ForegroundColor Yellow
Write-Host "Server: $ftpServer" -ForegroundColor Gray
Write-Host "User: $ftpUser" -ForegroundColor Gray
Write-Host ""

# Creează credențiale
$credentials = New-Object System.Net.NetworkCredential($ftpUser, $ftpPass)

# Funcție upload fișier
function Upload-File {
    param($localFile, $remotePath)
    
    try {
        $fileName = Split-Path $localFile -Leaf
        $uri = "$ftpServer/$remotePath/$fileName"
        
        $request = [System.Net.FtpWebRequest]::Create($uri)
        $request.Credentials = $credentials
        $request.Method = [System.Net.WebRequestMethods+Ftp]::UploadFile
        $request.UseBinary = $true
        $request.KeepAlive = $false
        
        $fileContent = [System.IO.File]::ReadAllBytes($localFile)
        $request.ContentLength = $fileContent.Length
        
        $requestStream = $request.GetRequestStream()
        $requestStream.Write($fileContent, 0, $fileContent.Length)
        $requestStream.Close()
        
        $response = $request.GetResponse()
        $response.Close()
        
        Write-Host "  ✅ $fileName" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "  ❌ $fileName - $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Funcție creare director
function Create-Directory {
    param($remotePath)
    
    try {
        $uri = "$ftpServer/$remotePath"
        $request = [System.Net.FtpWebRequest]::Create($uri)
        $request.Credentials = $credentials
        $request.Method = [System.Net.WebRequestMethods+Ftp]::MakeDirectory
        
        $response = $request.GetResponse()
        $response.Close()
        return $true
    }
    catch {
        # Director deja există sau altă eroare
        return $false
    }
}

Write-Host "[2/3] Upload fișiere..." -ForegroundColor Yellow
Write-Host "Acest proces poate dura 10-15 minute..." -ForegroundColor Gray
Write-Host ""

$totalFiles = 0
$uploadedFiles = 0

# Upload fișiere root
Write-Host "Upload fișiere principale..." -ForegroundColor Cyan
Get-ChildItem -Path $localPath -File | ForEach-Object {
    $totalFiles++
    if (Upload-File $_.FullName "public_html") {
        $uploadedFiles++
    }
}

# Upload foldere
$folders = @("css", "js", "data", "assets", "admin", "demo")

foreach ($folder in $folders) {
    $folderPath = Join-Path $localPath $folder
    if (Test-Path $folderPath) {
        Write-Host ""
        Write-Host "Upload folder: $folder..." -ForegroundColor Cyan
        
        # Creează director remote
        Create-Directory "public_html/$folder" | Out-Null
        
        # Upload fișiere din folder
        Get-ChildItem -Path $folderPath -File -Recurse | ForEach-Object {
            $totalFiles++
            $relativePath = $_.FullName.Substring($localPath.Length + 1).Replace("\", "/")
            $remoteDir = Split-Path "public_html/$relativePath" -Parent
            
            # Creează subdirectoare dacă e necesar
            $dirs = $remoteDir.Split("/")
            $currentPath = ""
            foreach ($dir in $dirs) {
                if ($dir) {
                    $currentPath += "$dir/"
                    Create-Directory $currentPath.TrimEnd("/") | Out-Null
                }
            }
            
            if (Upload-File $_.FullName $remoteDir) {
                $uploadedFiles++
            }
        }
    }
}

Write-Host ""
Write-Host "[3/3] Verificare finală..." -ForegroundColor Yellow
Write-Host "Total fișiere: $totalFiles" -ForegroundColor Gray
Write-Host "Uploadate cu succes: $uploadedFiles" -ForegroundColor Green

if ($uploadedFiles -eq $totalFiles) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  ✅ DEPLOYMENT COMPLET!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Site-ul tău este LIVE la:" -ForegroundColor Cyan
    Write-Host "https://kidsdigitalhub.com" -ForegroundColor White
    Write-Host ""
}
else {
    Write-Host ""
    Write-Host "⚠️ Upload parțial completat" -ForegroundColor Yellow
    Write-Host "Unele fișiere nu s-au uploadat. Verifică conexiunea FTP." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Apasă orice tastă pentru a închide..." -ForegroundColor Cyan
pause
