from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from urllib.parse import urlparse

from backend.scanner.scanner import scan_url


app = FastAPI(
    title="WebSecAI",
    description="AI-Powered Web Security Assistant",
    version="0.1.0"
)


class ScanRequest(BaseModel):
    url: str


@app.get("/")
def root():
    return {
        "project": "WebSecAI",
        "message": "AI-Powered Web Security Assistant API",
        "version": "0.1.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/scan")
async def scan(request: ScanRequest):

    parsed_url = urlparse(request.url)

    if parsed_url.scheme not in ["http", "https"]:
        raise HTTPException(
            status_code=400,
            detail="Please provide a valid HTTP or HTTPS URL."
        )

    if not parsed_url.netloc:
        raise HTTPException(
            status_code=400,
            detail="Invalid URL."
        )

    result = await scan_url(request.url)

    return {
        "status": "success",
        "data": result
    }
