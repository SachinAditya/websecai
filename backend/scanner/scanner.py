import httpx

from .security_headers import analyze_security_headers
from .cookies import analyze_cookies
from .cors import analyze_cors


async def scan_url(url: str):
    findings = []

    try:
        async with httpx.AsyncClient(
            timeout=10.0,
            follow_redirects=True
        ) as client:

            response = await client.get(
                url,
                headers={
                    "User-Agent": "WebSecAI/0.1"
                }
            )

        # Analyze security headers
        findings.extend(
            analyze_security_headers(response.headers)
        )

        # Analyze cookie security
        findings.extend(
            analyze_cookies(response.headers)
        )

        # Analyze CORS configuration
        findings.extend(
            analyze_cors(response.headers)
        )

        return {
            "target": url,
            "status_code": response.status_code,
            "final_url": str(response.url),
            "findings": findings
        }

    except httpx.RequestError as error:
        return {
            "target": url,
            "status_code": None,
            "final_url": None,
            "findings": [],
            "error": f"Unable to retrieve the target: {error}"
        }
