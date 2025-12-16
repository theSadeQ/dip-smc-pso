# Phase 2 PSO Optimization Monitor (PowerShell)
# Real-time monitoring of PSO optimization progress with visual progress bars

$controllers = @('sta_smc', 'adaptive_smc', 'hybrid_adaptive_sta_smc')
$startTime = Get-Date
$maxIterations = 200  # PSO max iterations per controller

# Function to create ASCII progress bar
function Get-ProgressBar {
    param (
        [int]$Current,
        [int]$Total,
        [int]$Width = 40
    )

    $percent = if ($Total -gt 0) { [math]::Round(($Current / $Total) * 100, 1) } else { 0 }
    $filled = [math]::Floor(($Current / $Total) * $Width)
    $empty = $Width - $filled

    $bar = "[" + ("=" * $filled) + (">" * [math]::Min(1, $empty)) + (" " * [math]::Max(0, $empty - 1)) + "]"

    return @{
        Bar = $bar
        Percent = $percent
    }
}

# Function to get checkpoint info (NEW - bulletproof PSO)
function Get-CheckpointInfo {
    param ([string]$ControllerKey)

    $checkpointDir = "optimization_results/phase2_pso_checkpoints"
    $checkpoints = Get-ChildItem -Path $checkpointDir -Filter "$($ControllerKey)_iter_*.json" -ErrorAction SilentlyContinue |
                   Sort-Object { [int]($_.BaseName -split '_')[-1] } -Descending

    if ($checkpoints -and $checkpoints.Count -gt 0) {
        $latest = $checkpoints[0]
        try {
            $data = Get-Content $latest.FullName | ConvertFrom-Json
            return @{
                Iteration = $data.iteration
                TotalIterations = $data.total_iterations
                BestCost = [math]::Round($data.best_cost, 2)
                Timestamp = $data.timestamp
                Found = $true
            }
        }
        catch {
            return @{ Found = $false }
        }
    }
    return @{ Found = $false }
}

# Function to parse PSO log for current iteration (LEGACY - fallback)
function Get-CurrentIteration {
    param ([string]$LogFile)

    if (Test-Path $LogFile) {
        $content = Get-Content $LogFile -Tail 50 -ErrorAction SilentlyContinue
        foreach ($line in $content[-1..-50]) {
            if ($line -match "pyswarms\.single\.global_best.*INFO.*iteration\s+(\d+)") {
                return [int]$matches[1]
            }
            if ($line -match "Iteration\s+(\d+)/") {
                return [int]$matches[1]
            }
        }
    }
    return 0
}

# Function to extract cost from logs (LEGACY - fallback)
function Get-CurrentCost {
    param ([string]$LogFile)

    if (Test-Path $LogFile) {
        $content = Get-Content $LogFile -Tail 20 -ErrorAction SilentlyContinue
        foreach ($line in $content[-1..-20]) {
            if ($line -match "best_cost\s*=\s*([0-9.]+)") {
                return [math]::Round([double]$matches[1], 2)
            }
            if ($line -match "Best Cost:\s*([0-9.]+)") {
                return [math]::Round([double]$matches[1], 2)
            }
        }
    }
    return $null
}

while ($true) {
    Clear-Host

    Write-Host ""
    Write-Host ("="*80) -ForegroundColor Cyan
    Write-Host "  PHASE 2 PSO OPTIMIZATION MONITOR - REAL-TIME PROGRESS" -ForegroundColor White
    Write-Host ("="*80) -ForegroundColor Cyan

    $elapsed = (Get-Date) - $startTime
    $runtime = "{0:hh\:mm\:ss}" -f $elapsed

    Write-Host ""
    Write-Host " Current Time: " -NoNewline -ForegroundColor Gray
    Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Yellow
    Write-Host " Monitor Uptime: " -NoNewline -ForegroundColor Gray
    Write-Host "$runtime" -ForegroundColor Yellow
    Write-Host ("-"*80) -ForegroundColor Gray

    # Monitor each controller
    $ctrlIndex = 0
    foreach ($ctrl in $controllers) {
        $ctrlIndex++
        $jsonPath = "optimization_results/phase2_pso_results/$($ctrl)_gains.json"
        $logPath = "optimization_results/phase2_pso_results/$($ctrl)_optimization.log"

        Write-Host ""
        Write-Host " [$ctrlIndex/3] " -NoNewline -ForegroundColor Cyan
        Write-Host "$($ctrl.ToUpper())" -ForegroundColor White

        if (Test-Path $jsonPath) {
            # Controller completed
            try {
                $data = Get-Content $jsonPath | ConvertFrom-Json
                $cost = [math]::Round($data.cost, 6)
                $gains = ($data.gains | ForEach-Object { [math]::Round($_, 3) }) -join ", "

                $progress = Get-ProgressBar -Current $maxIterations -Total $maxIterations -Width 50

                Write-Host "  $($progress.Bar) " -NoNewline -ForegroundColor Green
                Write-Host "100%" -ForegroundColor Green
                Write-Host "  Status: " -NoNewline -ForegroundColor Gray
                Write-Host "COMPLETE" -ForegroundColor Green -BackgroundColor DarkGreen
                Write-Host "  Final Cost: " -NoNewline -ForegroundColor Gray
                Write-Host "$cost" -ForegroundColor Green
                Write-Host "  Gains: " -NoNewline -ForegroundColor Gray
                Write-Host "[$gains]" -ForegroundColor White
            }
            catch {
                Write-Host "  Error: $_" -ForegroundColor Red
            }
        }
        else {
            # Controller still running or pending - check checkpoint first (NEW)
            $checkpointInfo = Get-CheckpointInfo -ControllerKey $ctrl

            if ($checkpointInfo.Found) {
                # Have checkpoint data - use it!
                $currentIter = $checkpointInfo.Iteration
                $totalIters = $checkpointInfo.TotalIterations
                $currentCost = $checkpointInfo.BestCost

                $progress = Get-ProgressBar -Current $currentIter -Total $totalIters -Width 50
                $eta = if ($currentIter -gt 0 -and $elapsed.TotalSeconds -gt 0) {
                    $timePerIter = $elapsed.TotalSeconds / $currentIter
                    $remainingIters = $totalIters - $currentIter
                    $etaSeconds = $timePerIter * $remainingIters
                    $etaTime = [TimeSpan]::FromSeconds($etaSeconds)
                    "{0:hh\:mm\:ss}" -f $etaTime
                } else { "calculating..." }

                Write-Host "  $($progress.Bar) " -NoNewline -ForegroundColor Yellow
                Write-Host "$($progress.Percent)%" -ForegroundColor Yellow
                Write-Host "  Status: " -NoNewline -ForegroundColor Gray
                Write-Host "OPTIMIZING" -ForegroundColor Yellow -BackgroundColor DarkYellow
                Write-Host "  Iteration: " -NoNewline -ForegroundColor Gray
                Write-Host "$currentIter/$totalIters" -ForegroundColor White
                Write-Host "  Current Cost: " -NoNewline -ForegroundColor Gray
                Write-Host "$currentCost" -ForegroundColor Cyan
                Write-Host "  ETA: " -NoNewline -ForegroundColor Gray
                Write-Host "$eta" -ForegroundColor Magenta
                Write-Host "  Checkpoint: " -NoNewline -ForegroundColor Gray
                Write-Host "ACTIVE (saves every 20 iters)" -ForegroundColor Green
            }
            else {
                # Fallback to log parsing (legacy)
                $currentIter = Get-CurrentIteration -LogFile $logPath
                $currentCost = Get-CurrentCost -LogFile $logPath

                if ($currentIter -gt 0) {
                    # Active optimization
                    $progress = Get-ProgressBar -Current $currentIter -Total $maxIterations -Width 50
                    $eta = if ($currentIter -gt 0) {
                        $timePerIter = $elapsed.TotalSeconds / $currentIter
                        $remainingIters = $maxIterations - $currentIter
                        $etaSeconds = $timePerIter * $remainingIters
                        $etaTime = [TimeSpan]::FromSeconds($etaSeconds)
                        "{0:hh\:mm\:ss}" -f $etaTime
                    } else { "calculating..." }

                    Write-Host "  $($progress.Bar) " -NoNewline -ForegroundColor Yellow
                    Write-Host "$($progress.Percent)%" -ForegroundColor Yellow
                    Write-Host "  Status: " -NoNewline -ForegroundColor Gray
                    Write-Host "OPTIMIZING" -ForegroundColor Yellow -BackgroundColor DarkYellow
                    Write-Host "  Iteration: " -NoNewline -ForegroundColor Gray
                    Write-Host "$currentIter/$maxIterations" -ForegroundColor White

                    if ($currentCost) {
                        Write-Host "  Current Cost: " -NoNewline -ForegroundColor Gray
                        Write-Host "$currentCost" -ForegroundColor Cyan
                    }

                    Write-Host "  ETA: " -NoNewline -ForegroundColor Gray
                    Write-Host "$eta" -ForegroundColor Magenta
                }
                else {
                    # Pending or just started
                    $progress = Get-ProgressBar -Current 0 -Total $maxIterations -Width 50
                    Write-Host "  $($progress.Bar) " -NoNewline -ForegroundColor DarkGray
                    Write-Host "0%" -ForegroundColor DarkGray
                    Write-Host "  Status: " -NoNewline -ForegroundColor Gray
                    Write-Host "PENDING" -ForegroundColor DarkGray
                    Write-Host "  Waiting for optimization to start..." -ForegroundColor DarkGray
                }
            }
        }
    }

    # Overall Progress Summary
    Write-Host ""
    Write-Host ("-"*80) -ForegroundColor Gray
    Write-Host " OVERALL PROGRESS SUMMARY" -ForegroundColor Cyan

    $completedCount = 0
    $optimizingCount = 0
    $pendingCount = 0

    foreach ($ctrl in $controllers) {
        $jsonPath = "optimization_results/phase2_pso_results/$($ctrl)_gains.json"
        $checkpointInfo = Get-CheckpointInfo -ControllerKey $ctrl

        if (Test-Path $jsonPath) {
            $completedCount++
        }
        elseif ($checkpointInfo.Found) {
            $optimizingCount++
        }
        else {
            $pendingCount++
        }
    }

    $totalProgress = [math]::Round(($completedCount / $controllers.Count) * 100, 1)
    $overallBar = Get-ProgressBar -Current $completedCount -Total $controllers.Count -Width 50

    Write-Host ""
    Write-Host "  Controllers: " -NoNewline -ForegroundColor Gray
    Write-Host "$completedCount " -NoNewline -ForegroundColor Green
    Write-Host "Complete | " -NoNewline -ForegroundColor Gray
    Write-Host "$optimizingCount " -NoNewline -ForegroundColor Yellow
    Write-Host "Optimizing | " -NoNewline -ForegroundColor Gray
    Write-Host "$pendingCount " -NoNewline -ForegroundColor DarkGray
    Write-Host "Pending" -ForegroundColor Gray

    Write-Host ""
    Write-Host "  Overall: " -NoNewline -ForegroundColor Gray
    Write-Host "$($overallBar.Bar) " -NoNewline -ForegroundColor $(if ($totalProgress -eq 100) { "Green" } elseif ($totalProgress -gt 0) { "Yellow" } else { "DarkGray" })
    Write-Host "$totalProgress%" -ForegroundColor $(if ($totalProgress -eq 100) { "Green" } elseif ($totalProgress -gt 0) { "Yellow" } else { "DarkGray" })

    # Show running Python processes
    Write-Host ""
    Write-Host ("-"*80) -ForegroundColor Gray
    Write-Host " PYTHON PROCESSES" -ForegroundColor Cyan

    $pythonProcs = Get-Process python -ErrorAction SilentlyContinue
    if ($pythonProcs) {
        Write-Host ""
        $pythonProcs | Select-Object @{
            Name='  CPU(s)'; Expression={[math]::Round($_.CPU, 1)}
        }, @{
            Name='Memory(MB)'; Expression={[math]::Round($_.WorkingSet / 1MB, 0)}
        }, @{
            Name='Runtime'; Expression={
                $procTime = (Get-Date) - $_.StartTime
                "{0:hh\:mm\:ss}" -f $procTime
            }
        }, @{
            Name='PID'; Expression={$_.Id}
        } | Format-Table -AutoSize
    }
    else {
        Write-Host ""
        Write-Host "  No Python processes found" -ForegroundColor Red
        Write-Host "  (PSO may have completed or not started)" -ForegroundColor DarkGray
    }

    Write-Host ("-"*80) -ForegroundColor Gray
    Write-Host " Press Ctrl+C to exit | Auto-refreshing every 30 seconds..." -ForegroundColor DarkGray
    Write-Host ("="*80) -ForegroundColor Cyan
    Write-Host ""

    Start-Sleep -Seconds 30
}
