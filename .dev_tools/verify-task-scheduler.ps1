#==========================================================================================\
#========================== .dev_tools/verify-task-scheduler.ps1 ==========================\
#==========================================================================================\

<#
.SYNOPSIS
    Verify Task Scheduler setup for Claude Code automated backups.

.DESCRIPTION
    This script checks if the ClaudeCode-AutoBackup task is properly registered,
    shows its status, and provides diagnostic information.

.EXAMPLE
    .\verify-task-scheduler.ps1
    Run verification checks

.NOTES
    Run this after registering the Task Scheduler to verify everything is working.
#>

$ErrorActionPreference = 'Continue'

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Claude Code Task Scheduler Verification" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check 1: Task exists
Write-Host "[1/5] Checking if task is registered..." -ForegroundColor Yellow
$task = schtasks /Query /TN "ClaudeCode-AutoBackup" /FO CSV /NH 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "  [OK] Task 'ClaudeCode-AutoBackup' is registered" -ForegroundColor Green
    $taskExists = $true
} else {
    Write-Host "  [FAIL] Task 'ClaudeCode-AutoBackup' is NOT registered" -ForegroundColor Red
    Write-Host "  Run: .dev_tools\register-task-scheduler.bat" -ForegroundColor Yellow
    $taskExists = $false
}

# Check 2: Task status
if ($taskExists) {
    Write-Host "`n[2/5] Checking task status..." -ForegroundColor Yellow
    $taskInfo = schtasks /Query /TN "ClaudeCode-AutoBackup" /V /FO LIST
    $status = $taskInfo | Select-String -Pattern "Status:" | Select-Object -First 1
    $nextRun = $taskInfo | Select-String -Pattern "Next Run Time:" | Select-Object -First 1
    $lastRun = $taskInfo | Select-String -Pattern "Last Run Time:" | Select-Object -First 1
    $lastResult = $taskInfo | Select-String -Pattern "Last Result:" | Select-Object -First 1

    Write-Host "  $status" -ForegroundColor Cyan
    Write-Host "  $nextRun" -ForegroundColor Cyan
    Write-Host "  $lastRun" -ForegroundColor Cyan
    Write-Host "  $lastResult" -ForegroundColor Cyan
}

# Check 3: Backup script exists
Write-Host "`n[3/5] Checking backup script..." -ForegroundColor Yellow
$scriptPath = "D:\Projects\main\.dev_tools\claude-backup.ps1"
if (Test-Path $scriptPath) {
    Write-Host "  [OK] Backup script exists: $scriptPath" -ForegroundColor Green
} else {
    Write-Host "  [FAIL] Backup script NOT found: $scriptPath" -ForegroundColor Red
}

# Check 4: Repository status
Write-Host "`n[4/5] Checking repository status..." -ForegroundColor Yellow
Push-Location "D:\Projects\main"
$gitStatus = git status --porcelain 2>&1
if ($gitStatus) {
    Write-Host "  [INFO] Changes detected (will trigger backup):" -ForegroundColor Cyan
    Write-Host "  $gitStatus" -ForegroundColor Gray
} else {
    Write-Host "  [INFO] No changes detected (backup will skip)" -ForegroundColor Cyan
}
Pop-Location

# Check 5: Backup logs
Write-Host "`n[5/5] Checking backup logs..." -ForegroundColor Yellow
$logPath = ".\.dev_tools\backup\backup.log"
if (Test-Path $logPath) {
    Write-Host "  [OK] Backup log exists" -ForegroundColor Green
    Write-Host "  Recent entries:" -ForegroundColor Cyan
    Get-Content $logPath -Tail 10 | ForEach-Object { Write-Host "    $_" -ForegroundColor Gray }
} else {
    Write-Host "  [INFO] No backup log yet (task hasn't run)" -ForegroundColor Yellow
    Write-Host "  Expected location: $logPath" -ForegroundColor Gray
}

# Summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

if ($taskExists) {
    Write-Host "[OK] Task Scheduler is configured" -ForegroundColor Green
    Write-Host "`nNext steps:" -ForegroundColor Yellow
    Write-Host "  1. Wait 1-2 minutes for first automatic backup" -ForegroundColor White
    Write-Host "  2. Check git log: git log --oneline --grep='Auto-backup' -5" -ForegroundColor White
    Write-Host "  3. Monitor logs: Get-Content .dev_tools\backup\backup.log -Wait" -ForegroundColor White
    Write-Host "`nTo test immediately:" -ForegroundColor Yellow
    Write-Host "  schtasks /Run /TN 'ClaudeCode-AutoBackup'" -ForegroundColor White
} else {
    Write-Host "[FAIL] Task Scheduler is NOT configured" -ForegroundColor Red
    Write-Host "`nTo fix:" -ForegroundColor Yellow
    Write-Host "  .dev_tools\register-task-scheduler.bat" -ForegroundColor White
}

Write-Host "`n========================================`n" -ForegroundColor Cyan
