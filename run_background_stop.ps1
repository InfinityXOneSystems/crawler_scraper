Write-Output "Stopping orchestrator background jobs (matching orchestrator.py)"
$jobs = Get-Job | Where-Object { $_.Command -match 'orchestrator.py' -or $_.ScriptBlock.ToString() -match 'orchestrator.py' }
if (-not $jobs) { Write-Output "No matching background jobs found."; exit 0 }
foreach ($j in $jobs) {
    Stop-Job -Job $j -Force
    Remove-Job -Job $j
    Write-Output "Stopped job id $($j.Id)"
}
