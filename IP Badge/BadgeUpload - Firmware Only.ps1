# Check if Python is installed
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "Python is NOT installed."
    exit 1
} else {
    Write-Host "Python is installed."
}

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

Write-Host "`n--- Step 1: Erase board ---"

$processInfo = New-Object System.Diagnostics.ProcessStartInfo
$processInfo.FileName = "mpremote"
$processInfo.Arguments = "fs rm -rv :/"
$processInfo.RedirectStandardOutput = $true
$processInfo.RedirectStandardError = $true
$processInfo.UseShellExecute = $false
$processInfo.CreateNoWindow = $true

$process = New-Object System.Diagnostics.Process
$process.StartInfo = $processInfo
$process.Start() | Out-Null

$outputLines = @()

while (-not $process.StandardOutput.EndOfStream) {
    $line = $process.StandardOutput.ReadLine()
    Write-Host $line
    $outputLines += $line
}

$process.WaitForExit()

Start-Sleep -Seconds 2

# Only require that rm :/ OR "Operation not permitted" appears
if (
    ($outputLines | Where-Object { $_ -like "rm :/*" }) -or
    ($outputLines | Where-Object { $_ -like "*Operation not permitted*" })
) {
    Write-Host "Erase complete (or nothing to erase). Continuing..."
} else {
    Write-Host "Erase did not complete as expected. You may need to check the device."
    exit 1
}


Write-Host "`n--- Step 1.5: Sanity Check - No files shown ---"
mpremote ls :
start-sleep 5

Write-Host "`n--- Step 2: Copy Dev folder ---"
mpremote cp -r .\Dev\. :
#Write-Host "Waiting for 30 seconds..."
#Start-Sleep -Seconds 30

mpremote reset
Write-Host "`n--- Step 3: Rebooting the board. You should see blinky stuff ---"
Start-Sleep -Seconds 15