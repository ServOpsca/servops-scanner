import dns.resolver


def check_email_security(domain: str) -> dict:
    result = {
        "check": "email_security",
        "label": "Email security",
        "score": 0,
        "status": "fail",
        "detail": "",
        "plain_english": "",
        "sub_checks": {
            "spf": False,
            "dkim": False,
            "dmarc": False,
        },
    }

    spf_found = False
    dkim_found = False
    dmarc_found = False

    # SPF check
    try:
        answers = dns.resolver.resolve(domain, "TXT")
        for rdata in answers:
            txt = rdata.to_text()
            if "v=spf1" in txt:
                spf_found = True
                break
    except Exception:
        pass

    # DKIM check (default selector — common default)
    try:
        dkim_domain = f"default._domainkey.{domain}"
        dns.resolver.resolve(dkim_domain, "TXT")
        dkim_found = True
    except Exception:
        # Try google selector as fallback
        try:
            dkim_domain = f"google._domainkey.{domain}"
            dns.resolver.resolve(dkim_domain, "TXT")
            dkim_found = True
        except Exception:
            pass

    # DMARC check
    try:
        dmarc_domain = f"_dmarc.{domain}"
        answers = dns.resolver.resolve(dmarc_domain, "TXT")
        for rdata in answers:
            if "v=DMARC1" in rdata.to_text():
                dmarc_found = True
                break
    except Exception:
        pass

    result["sub_checks"] = {
        "spf": spf_found,
        "dkim": dkim_found,
        "dmarc": dmarc_found,
    }

    passed = sum([spf_found, dkim_found, dmarc_found])

    if passed == 3:
        result["score"] = 100
        result["status"] = "pass"
        result["detail"] = "SPF, DKIM, and DMARC all configured"
        result["plain_english"] = (
            "Your email domain is fully protected. "
            "SPF, DKIM, and DMARC are all in place — "
            "hackers cannot send fake emails pretending to be you."
        )
    elif passed == 2:
        result["score"] = 60
        result["status"] = "warn"
        missing = [k for k, v in result["sub_checks"].items() if not v]
        result["detail"] = f"Missing: {', '.join(missing).upper()}"
        result["plain_english"] = (
            f"Your email is partially protected but {', '.join(missing).upper()} "
            f"is missing. Your emails may land in spam for some recipients."
        )
    elif passed == 1:
        result["score"] = 20
        result["status"] = "fail"
        result["detail"] = "Only 1 of 3 email security records found"
        result["plain_english"] = (
            "Your email domain has minimal protection. "
            "Without DMARC especially, anyone can send emails "
            "pretending to be from your domain — scamming your clients."
        )
    else:
        result["score"] = 0
        result["status"] = "fail"
        result["detail"] = "No SPF, DKIM, or DMARC records found"
        result["plain_english"] = (
            "Your email domain has zero protection. "
            "Hackers can send emails that look exactly like they came from you. "
            "This is one of the most common ways SMB clients get scammed."
        )

    return result
