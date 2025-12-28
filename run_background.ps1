Param(
    [string]$VenvPath = "c:\AI\repos\.venv_crawler",
    [string]$LogDir = "c:\AI\repos\crawler_scraper\logs",
    [string]$Seed = "c:\AI\repos\crawler_scraper\crawler\seeds\business_loans.yaml"
)

if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir | Out-Null }

$stdout = Join-Path $LogDir "orchestrator.log"
$stderr = Join-Path $LogDir "orchestrator.err"

Write-Output "Starting orchestrator as background job. Logs: $stdout, $stderr"

$script = {
    param($VenvPath, $Seed, $stdout, $stderr)
    try {
        if (-not (Test-Path $VenvPath)) {
            python -m venv $VenvPath
        }
        & "$VenvPath\Scripts\Activate.ps1"
        pip install -r "c:\AI\repos\crawler_scraper\requirements.txt"
        python -m playwright install chromium
        python "c:\AI\repos\crawler_scraper\orchestrator.py" --seed $Seed
    } catch {
        $_ | Out-File -FilePath $stderr -Append
    }
}

Start-Job -ScriptBlock $script -ArgumentList $VenvPath,$Seed,$stdout,$stderr | Out-Null

Write-Output "Orchestrator job started. Use run_background_stop.ps1 to stop it."
