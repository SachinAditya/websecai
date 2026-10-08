from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from urllib.parse import urlparse

from backend.scanner.scanner import scan_url
from backend.ai.gemma import ask_gemma


app = FastAPI(
    title="WebSecAI",
    description="AI-Powered Web Security Assistant",
    version="0.2.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScanRequest(BaseModel):
    url: str


@app.get("/")
def root():
    return {
        "project": "WebSecAI",
        "message": "AI-Powered Web Security Assistant API",
        "version": "0.2.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/ai-test")
async def ai_test():
    response = await ask_gemma(
        "Say hello to WebSecAI in exactly one short sentence."
    )

    return {
        "ai_response": response
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

    if result.get("error"):
        return {
            "status": "success",
            "data": result
        }

    findings = result.get("findings", [])

    prompt = f"""
You are WebSecAI, a defensive web security assistant.

Analyze these security findings:

{findings}

For each finding, give:
- Issue
- Impact
- Fix

Use only the supplied evidence.
Do not invent vulnerabilities.
Keep the entire answer under 150 words.
"""

    ai_analysis = await ask_gemma(prompt)

    return {
        "status": "success",
        "data": {
            **result,
            "ai_analysis": ai_analysis
        }
    }
