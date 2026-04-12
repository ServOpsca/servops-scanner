import requests

HEADERS_TO_CHECK = {
    "Strict-Transport-Security": {
        "label": "HSTS",
        "risk": "Without HSTS, attackers can intercept traffic between your visitors and your site.",
    },
    "Content-Security-Policy": {
        "label": "CSP",
        "risk": "Without CSP, attackers can inject malicious scripts into your website.",
    },
    "X-Frame-Options": {
        "label": "X-Frame-Options",
        "risk": "Without this, your site can be embedded in a fake page to trick your visitors.",
    },
    "X-Content-Type-Options": {
        "label": "X-Content-Type-Options",
        "risk": "Without this, browsers may misinterpret files on your site in dangerous ways.",
    },
}


def check_headers(domain: str) -> dict:
    result = {
        "check": "security_headers",
        "label": "Security headers",
        "score": 0,
        "status": "fail",
        "detail": "",
        "plain_english": "",
        "headers_found": [],
        "headers_missing": [],
    }

    try:
        url = f"https://{domain}"
        response = requests.get(
            url,
            timeout=10,
            allow_redirects=True,
            headers={"User-Agent": "ServOps-Scanner/1.0"},
        )
        headers = response.headers

        found = []
        missing = []

        for header, meta in HEADERS_TO_CHECK.items():
            if header in headers:
                found.append(meta["label"])
            else:
                missing.append({
                    "header": header,
                    "label": meta["label"],
                    "risk": meta["risk"],
                })

        result["headers_found"] = found
        result["headers_missing"] = [m["label"] for m in missing]

        score = int((len(found) / len(HEADERS_TO_CHECK)) * 100)
        result["score"] = score

        if score == 100:
            result["status"] = "pass"
            result["detail"] = "All security headers present"
            result["plain_english"] = (
                "Your website has all recommended security headers in place. "
                "Visitor data is well protected at the browser level."
            )
        elif score >= 50:
            result["status"] = "warn"
            missing_labels = ", ".join([m["label"] for m in missing])
            result["detail"] = f"Missing: {missing_labels}"
            result["plain_english"] = (
                f"Your website is missing {len(missing)} security headers "
                f"({missing_labels}). These are quick fixes that significantly "
                f"improve your site's protection."
            )
        else:
            result["status"] = "fail"
            result["detail"] = f"Only {len(found)} of {len(HEADERS_TO_CHECK)} headers present"
            result["plain_english"] = (
                f"Your website is missing most security headers. "
                f"This leaves visitors vulnerable to several common attacks. "
                f"A developer can fix all of these in under an hour."
            )

    except requests.exceptions.SSLError:
        result["detail"] = "SSL error — could not fetch headers"
        result["plain_english"] = "We could not fetch your site headers due to an SSL error."
    except Exception as e:
        result["detail"] = f"Could not reach {domain}"
        result["plain_english"] = (
            f"We could not reach your website to check security headers. "
            f"Your site may be down or blocking automated requests."
        )

    return result
