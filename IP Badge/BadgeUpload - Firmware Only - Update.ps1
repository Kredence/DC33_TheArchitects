Write-Host "`n--- Step 1: Python Check ---"

# Check if Python is installed
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "Python is NOT installed."
    exit 1
} else {
    Write-Host "Python is installed."
}

Write-Host "`n--- Step 2: MPRemote Check ---"

# Check if mpremote is installed
try {
    $mpremoteCheck = mpremote --version
    Write-Host "mpremote is installed: $mpremoteCheck"
} catch {
    Write-Host "mpremote is NOT installed."
    exit 1
}

# Check if inside 'IP Badge' folder
$currDir = Split-Path -Leaf (Get-Location)
if ($currDir -ne "IP Badge") {
    Write-Host "Not in 'IP Badge' folder. Current folder is: $currDir"
    exit 1
} else {
    Write-Host "In the 'IP Badge' folder."
}

Write-Host "`n--- Step 3: Recursive Copy Dev folder ---"
mpremote cp -r .\Dev\. :
#Write-Host "Waiting for 30 seconds..."
#Start-Sleep -Seconds 30

mpremote reset
Write-Host "`n--- Step 4: Rebooting the board. You should see blinky stuff ---"
Start-Sleep -Seconds 15