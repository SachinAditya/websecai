SECURITY_HEADERS = {
    "Content-Security-Policy": {
        "severity": "Medium",
        "description": "Helps control which resources browsers are allowed to load."
    },
    "Strict-Transport-Security": {
        "severity": "Medium",
        "description": "Helps enforce HTTPS connections."
    },
    "X-Content-Type-Options": {
        "severity": "Low",
        "description": "Helps prevent MIME-type sniffing."
    },
    "X-Frame-Options": {
        "severity": "Low",
        "description": "Helps reduce clickjacking risk."
    },
    "Referrer-Policy": {
        "severity": "Low",
        "description": "Controls how much referrer information is sent."
    },
    "Permissions-Policy": {
        "severity": "Low",
        "description": "Controls access to selected browser capabilities."
    }
}


def analyze_security_headers(headers):
    findings = []

    for header, details in SECURITY_HEADERS.items():
        if header.lower() not in {key.lower() for key in headers.keys()}:
            findings.append({
                "type": "Missing Security Header",
                "header": header,
                "severity": details["severity"],
                "description": details["description"],
                "recommendation": f"Consider configuring the {header} header."
            })

    return findings
