# Find and delete ALL backup-related scheduled tasks

Write-Host "=== Searching for backup-related scheduled tasks ===" -ForegroundColor Yellow
Write-Host ""

# Search patterns
$patterns = @(
    "*backup*",
    "*claude*",
    "*ClaudeCode*",
    "*Auto-Backup*",
    "*git*"
)

$tasksFound = @()

foreach ($pattern in $patterns) {
    Write-Host "Searching for tasks matching: $pattern" -ForegroundColor Cyan
    try {
        $tasks = Get-ScheduledTask | Where-Object { $_.TaskName -like $pattern }
        foreach ($task in $tasks) {
            $tasksFound += $task
            Write-Host "  FOUND: $($task.TaskName) (Path: $($task.TaskPath))" -ForegroundColor Red
        }
    } catch {
        # Ignore errors
    }
}

Write-Host ""
Write-Host "=== Total tasks found: $($tasksFound.Count) ===" -ForegroundColor Yellow
Write-Host ""

if ($tasksFound.Count -eq 0) {
    Write-Host "No backup-related tasks found. The task may already be deleted." -ForegroundColor Green
    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 0
}

Write-Host "Deleting all found tasks..." -ForegroundColor Yellow
Write-Host ""

foreach ($task in $tasksFound) {
    try {
        $taskPath = $task.TaskPath + $task.TaskName
        Write-Host "Deleting: $taskPath" -ForegroundColor Red
        Unregister-ScheduledTask -TaskName $task.TaskName -TaskPath $task.TaskPath -Confirm:$false
        Write-Host "  SUCCESS: Deleted $($task.TaskName)" -ForegroundColor Green
    } catch {
        Write-Host "  ERROR: Failed to delete $($task.TaskName) - $_" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=== DONE ===" -ForegroundColor Green
Write-Host "The CMD window should no longer appear." -ForegroundColor Green
Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
