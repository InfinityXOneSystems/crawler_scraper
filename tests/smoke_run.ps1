param(
    [string]$VenvPath = "c:\AI\repos\.venv_crawler"
)
python -m venv $VenvPath
& "$VenvPath\Scripts\Activate.ps1"
pip install -r "c:\AI\repos\crawler_scraper\requirements.txt"
python -m playwright install chromium
python "c:\AI\repos\crawler_scraper\orchestrator.py" --seed "c:\AI\repos\crawler_scraper\crawler\seeds\business_loans.yaml"
