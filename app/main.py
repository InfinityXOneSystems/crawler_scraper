import os

from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel, HttpUrl, Field
from app.crawler import run_crawl

app = FastAPI(title="Infinity Modular Crawler")


class RunPayload(BaseModel):
    seed_url: HttpUrl
    industry: str = Field(default="generic")
    depth: int = Field(default=1, ge=1, le=5)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/run")
async def run(payload: RunPayload):
    try:
        result = run_crawl(payload.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080))
    )
