import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_SERVICE_KEY"],
)


def save_scan(domain: str, email: str, name: str, results: list, score: dict) -> str:
    checks = {r["check"]: r["score"] for r in results}

    data = {
        "domain":          domain,
        "email":           email,
        "name":            name,
        "ssl_score":       checks.get("ssl", 0),
        "email_score":     checks.get("email_security", 0),
        "ports_score":     checks.get("open_ports", 0),
        "headers_score":   checks.get("security_headers", 0),
        "dns_score":       checks.get("dns_health", 0),
        "total_score":     score["total_score"],
        "status":          score["status"],
    }

    response = supabase.table("scans").insert(data).execute()
    return response.data[0]["id"]
