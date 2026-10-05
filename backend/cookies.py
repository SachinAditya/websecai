def analyze_cookies(headers):
    findings = []

    # HTTP headers can contain multiple Set-Cookie values.
    if hasattr(headers, "get_list"):
        cookies = headers.get_list("set-cookie")
    else:
        cookie_header = headers.get("set-cookie")
        cookies = [cookie_header] if cookie_header else []

    for cookie in cookies:
        if not cookie:
            continue

        cookie_name = cookie.split("=", 1)[0].strip()

        if "secure" not in cookie.lower():
            findings.append({
                "type": "Cookie Security",
                "cookie": cookie_name,
                "issue": "Missing Secure attribute",
                "severity": "Medium",
                "description": (
                    "The cookie does not include the Secure attribute."
                ),
                "recommendation": (
                    "Set the Secure attribute so the cookie is sent "
                    "only over HTTPS connections."
                )
            })

        if "httponly" not in cookie.lower():
            findings.append({
                "type": "Cookie Security",
                "cookie": cookie_name,
                "issue": "Missing HttpOnly attribute",
                "severity": "Medium",
                "description": (
                    "The cookie does not include the HttpOnly attribute."
                ),
                "recommendation": (
                    "Consider using HttpOnly for cookies that do not "
                    "need to be accessed by client-side JavaScript."
                )
            })

        if "samesite" not in cookie.lower():
            findings.append({
                "type": "Cookie Security",
                "cookie": cookie_name,
                "issue": "Missing SameSite attribute",
                "severity": "Low",
                "description": (
                    "The cookie does not explicitly define a SameSite policy."
                ),
                "recommendation": (
                    "Set an appropriate SameSite value such as Lax or Strict "
                    "according to the application's requirements."
                )
            })

    return findings
