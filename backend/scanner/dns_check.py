import dns.resolver
import requests


# Free DNS blacklist APIs to check against
BLACKLIST_ZONES = [
    "zen.spamhaus.org",
    "bl.spamcop.net",
    "dnsbl.sorbs.net",
]


def check_dns(domain: str) -> dict:
    result = {
        "check": "dns_health",
        "label": "DNS health",
        "score": 100,
        "status": "pass",
        "detail": "",
        "plain_english": "",
        "issues": [],
    }

    issues = []

    # 1. Check domain resolves
    try:
        answers = dns.resolver.resolve(domain, "A")
        ip = str(answers[0])
    except Exception:
        result["score"] = 0
        result["status"] = "fail"
        result["detail"] = "Domain does not resolve"
        result["plain_english"] = (
            "Your domain is not resolving correctly. "
            "Visitors cannot reach your website and your emails may not deliver."
        )
        return result

    # 2. Check MX records (email delivery)
    try:
        dns.resolver.resolve(domain, "MX")
    except Exception:
        issues.append("No MX records — email may not be configured")

    # 3. Check blacklists
    blacklisted_on = []
    reversed_ip = ".".join(reversed(ip.split(".")))

    for bl in BLACKLIST_ZONES:
        try:
            lookup = f"{reversed_ip}.{bl}"
            dns.resolver.resolve(lookup, "A")
            blacklisted_on.append(bl)
        except dns.resolver.NXDOMAIN:
            pass
        except Exception:
            pass

    if blacklisted_on:
        issues.append(
            f"Domain IP listed on {len(blacklisted_on)} blacklist(s): "
            + ", ".join(blacklisted_on)
        )

    # 4. Score
    if not issues:
        result["score"] = 100
        result["status"] = "pass"
        result["detail"] = "DNS resolves correctly, not blacklisted"
        result["plain_english"] = (
            "Your domain resolves correctly and is not on any spam blacklists. "
            "Emails from your domain should reach recipients' inboxes."
        )
    elif blacklisted_on:
        result["score"] = 0
        result["status"] = "fail"
        result["issues"] = issues
        result["detail"] = f"Listed on {len(blacklisted_on)} spam blacklist(s)"
        result["plain_english"] = (
            f"Your domain's IP address is on {len(blacklisted_on)} spam blacklist(s). "
            f"This means your emails are likely going straight to junk for many recipients — "
            f"every day this goes unfixed, you're losing business."
        )
    else:
        result["score"] = 60
        result["status"] = "warn"
        result["issues"] = issues
        result["detail"] = "Minor DNS issues detected"
        result["plain_english"] = (
            "Your domain resolves correctly but has some minor DNS issues. "
            "These should be reviewed to ensure reliable email delivery."
        )

    return result
