FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Allow skipping Playwright install for lightweight API-only images
ARG INSTALL_PLAYWRIGHT=true
RUN if [ "$INSTALL_PLAYWRIGHT" = "true" ]; then python -m playwright install chromium; fi

ENV PYTHONUNBUFFERED=1
EXPOSE 8080

# Default to running the FastAPI server; override to run crawler engine
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
