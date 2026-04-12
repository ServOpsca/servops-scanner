WEIGHTS = {
    "ssl":              0.20,
    "email_security":   0.25,
    "open_ports":       0.25,
    "security_headers": 0.15,
    "dns_health":       0.15,
}

SCORE_LABELS = {
    "pass": "Passing",
    "warn": "Needs attention",
    "fail": "At risk",
}


def calculate_total_score(results: list[dict]) -> dict:
    total = 0.0

    for r in results:
        check_key = r.get("check")
        weight = WEIGHTS.get(check_key, 0)
        total += r.get("score", 0) * weight

    total_score = round(total)

    if total_score >= 80:
        label = "Healthy"
        status = "pass"
    elif total_score >= 50:
        label = "Needs attention"
        status = "warn"
    else:
        label = "At risk"
        status = "fail"

    critical = sum(1 for r in results if r.get("status") == "fail")
    warnings  = sum(1 for r in results if r.get("status") == "warn")
    passing   = sum(1 for r in results if r.get("status") == "pass")

    return {
        "total_score": total_score,
        "label": label,
        "status": status,
        "critical": critical,
        "warnings": warnings,
        "passing": passing,
    }
