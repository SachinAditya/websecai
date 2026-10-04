from fastapi import FastAPI
from pydantic import BaseModel
from urllib.parse import urlparse

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
def scan(request: ScanRequest):
    parsed_url = urlparse(request.url)

    if parsed_url.scheme not in ["http", "https"]:
        return {
            "status": "error",
            "message": "Please provide a valid HTTP or HTTPS URL."
        }

    return {
        "status": "success",
        "target": request.url,
        "message": "Target accepted for authorized security analysis.",
        "findings": []
    }
