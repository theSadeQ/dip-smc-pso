#==========================================================================================\
#======================= .dev_tools/fix-task-scheduler.ps1 ============================\
#==========================================================================================\

<#
.SYNOPSIS
    Fix Task Scheduler working directory issue.

.DESCRIPTION
    Deletes and recreates the ClaudeCode-AutoBackup task with proper working directory.
    This fixes the ERROR_FILE_NOT_FOUND (-2147024894) issue.

.NOTES
    Run as Administrator if deletion requires elevated privileges.
#>

$ErrorActionPreference = 'Continue'

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Task Scheduler Fix Script" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Step 1: Delete existing task
Write-Host "[1/3] Deleting existing task..." -ForegroundColor Yellow
& C:\Windows\System32\schtasks.exe /Delete /TN "ClaudeCode-AutoBackup" /F 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "  [OK] Task deleted successfully" -ForegroundColor Green
} else {
    Write-Host "  [INFO] Task may not exist (this is OK)" -ForegroundColor Cyan
}

# Step 2: Create new task with working directory fix
Write-Host "`n[2/3] Creating task with working directory fix..." -ForegroundColor Yellow

$taskCommand = "powershell.exe -NoProfile -ExecutionPolicy Bypass -File D:\Projects\main\.dev_tools\claude-backup-wrapper.ps1"

& C:\Windows\System32\schtasks.exe /Create `
 /TN "ClaudeCode-AutoBackup" `
 /TR $taskCommand `
 /SC MINUTE `
 /MO 1 `
 /RL LIMITED `
 /F

if ($LASTEXITCODE -eq 0) {
    Write-Host "  [OK] Task created successfully" -ForegroundColor Green

    # Step 3: Test the task
    Write-Host "`n[3/3] Testing task execution..." -ForegroundColor Yellow
    & C:\Windows\System32\schtasks.exe /Run /TN "ClaudeCode-AutoBackup"

    Write-Host "  Waiting 15 seconds for task to complete..." -ForegroundColor Cyan
    Start-Sleep -Seconds 15

    # Check result
    Write-Host "`n  Checking result..." -ForegroundColor Cyan
    $taskInfo = & C:\Windows\System32\schtasks.exe /Query /TN "ClaudeCode-AutoBackup" /V /FO LIST
    $lastResult = $taskInfo | Select-String -Pattern "Last Result:" | Select-Object -First 1

    Write-Host "  $lastResult" -ForegroundColor $(if ($lastResult -match "0x0") { "Green" } else { "Red" })

    if ($lastResult -match "0x0") {
        Write-Host "`n[SUCCESS] Task is now working correctly!" -ForegroundColor Green
        Write-Host "`nChecking for new commits..." -ForegroundColor Yellow
        Set-Location "D:\Projects\main"
        git log --oneline --grep="Auto-backup" -5
    } else {
        Write-Host "`n[WARNING] Task may still have issues. Check backup log:" -ForegroundColor Yellow
        Write-Host "  Get-Content .dev_tools\backup\backup.log -Tail 20" -ForegroundColor White
    }

} else {
    Write-Host "  [ERROR] Failed to create task" -ForegroundColor Red
    Write-Host "`nError code: $LASTEXITCODE" -ForegroundColor Red
}

Write-Host "`n========================================`n" -ForegroundColor Cyan
