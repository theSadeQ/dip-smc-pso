# Show ALL scheduled tasks and their details

Write-Host "=== LISTING ALL SCHEDULED TASKS ===" -ForegroundColor Yellow
Write-Host ""

$allTasks = Get-ScheduledTask | Sort-Object TaskName

Write-Host "Total tasks found: $($allTasks.Count)" -ForegroundColor Cyan
Write-Host ""
Write-Host "Tasks that run frequently (every 1-5 minutes):" -ForegroundColor Red
Write-Host ""

foreach ($task in $allTasks) {
    try {
        $info = Get-ScheduledTaskInfo -TaskName $task.TaskName -TaskPath $task.TaskPath -ErrorAction SilentlyContinue
        $triggers = $task.Triggers

        foreach ($trigger in $triggers) {
            if ($trigger.Repetition -and $trigger.Repetition.Interval) {
                $interval = $trigger.Repetition.Interval

                # Check if it's running every 1-5 minutes
                if ($interval -match "PT[1-5]M") {
                    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Red
                    Write-Host "TASK NAME: $($task.TaskName)" -ForegroundColor Red
                    Write-Host "PATH: $($task.TaskPath)" -ForegroundColor Yellow
                    Write-Host "STATE: $($task.State)" -ForegroundColor Yellow
                    Write-Host "INTERVAL: $interval" -ForegroundColor Red
                    Write-Host "COMMAND: $($task.Actions[0].Execute)" -ForegroundColor Cyan
                    Write-Host "ARGUMENTS: $($task.Actions[0].Arguments)" -ForegroundColor Cyan
                    Write-Host "WORKING DIR: $($task.Actions[0].WorkingDirectory)" -ForegroundColor Cyan
                    Write-Host "LAST RUN: $($info.LastRunTime)" -ForegroundColor Yellow
                    Write-Host "NEXT RUN: $($info.NextRunTime)" -ForegroundColor Yellow
                    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Red
                    Write-Host ""

                    # Prompt to delete
                    $response = Read-Host "Delete this task? (y/n)"
                    if ($response -eq 'y' -or $response -eq 'Y') {
                        try {
                            Unregister-ScheduledTask -TaskName $task.TaskName -TaskPath $task.TaskPath -Confirm:$false
                            Write-Host "✓ DELETED: $($task.TaskName)" -ForegroundColor Green
                        } catch {
                            Write-Host "✗ FAILED to delete: $_" -ForegroundColor Red
                        }
                    } else {
                        Write-Host "Skipped." -ForegroundColor Gray
                    }
                    Write-Host ""
                }
            }
        }
    } catch {
        # Skip
    }
}

Write-Host ""
Write-Host "=== SEARCH COMPLETE ===" -ForegroundColor Green
Write-Host ""
pause
