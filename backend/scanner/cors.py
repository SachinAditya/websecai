def analyze_cors(headers):
    findings = []

    allow_origin = headers.get("access-control-allow-origin")

    if not allow_origin:
        return findings

    allow_origin = allow_origin.strip()

    if allow_origin == "*":
        findings.append({
            "type": "CORS Security",
            "header": "Access-Control-Allow-Origin",
            "severity": "Medium",
            "description": (
                "The server allows cross-origin requests from any origin."
            ),
            "recommendation": (
                "Avoid wildcard CORS for sensitive resources. "
                "Allow only trusted origins when appropriate."
            )
        })

    elif allow_origin.lower() == "null":
        findings.append({
            "type": "CORS Security",
            "header": "Access-Control-Allow-Origin",
            "severity": "Medium",
            "description": (
                "The server allows requests from the null origin."
            ),
            "recommendation": (
                "Review whether allowing the null origin is required "
                "and restrict it if unnecessary."
            )
        })

    return findings
