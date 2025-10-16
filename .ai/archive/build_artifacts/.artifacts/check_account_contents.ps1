# Check what's in account directories
Write-Host "=== Checking Account 1 Contents ===" -ForegroundColor Cyan
Get-ChildItem "$env:USERPROFILE\.claude1" -Force | Select-Object Name, Length, LinkType | Format-Table

Write-Host "`n=== Checking Account 9 Contents (Current) ===" -ForegroundColor Cyan
Get-ChildItem "$env:USERPROFILE\.claude9" -Force | Select-Object Name, Length, LinkType | Format-Table

Write-Host "`n=== Auth File Check ===" -ForegroundColor Cyan
@("history.jsonl", "settings.json", "settings.local.json") | ForEach-Object {
    $file = $_
    Write-Host "`nChecking $file across accounts:"

    $primary = "$env:USERPROFILE\.claude\$file"
    if (Test-Path $primary) {
        $size = (Get-Item $primary).Length
        Write-Host "  Primary: $size bytes" -ForegroundColor Green
    }

    @(1, 9) | ForEach-Object {
        $accNum = $_
        $accFile = "$env:USERPROFILE\.claude$accNum\$file"
        if (Test-Path $accFile) {
            $size = (Get-Item $accFile).Length
            Write-Host "  Account ${accNum}: $size bytes" -ForegroundColor Yellow
        } else {
            Write-Host "  Account ${accNum}: MISSING" -ForegroundColor Red
        }
    }
}
