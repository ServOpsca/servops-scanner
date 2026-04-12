import ssl
import socket
from datetime import datetime


def check_ssl(domain: str) -> dict:
    result = {
        "check": "ssl",
        "label": "SSL certificate",
        "score": 0,
        "status": "fail",
        "detail": "",
        "plain_english": "",
    }

    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(
            socket.socket(), server_hostname=domain
        ) as s:
            s.settimeout(10)
            s.connect((domain, 443))
            cert = s.getpeercert()

        expire_str = cert["notAfter"]
        expire_date = datetime.strptime(expire_str, "%b %d %H:%M:%S %Y %Z")
        days_left = (expire_date - datetime.utcnow()).days

        if days_left > 30:
            result["score"] = 100
            result["status"] = "pass"
            result["detail"] = f"Valid SSL — expires in {days_left} days"
            result["plain_english"] = (
                f"Your website has a valid SSL certificate. "
                f"It expires in {days_left} days. No action needed."
            )
        elif days_left > 0:
            result["score"] = 40
            result["status"] = "warn"
            result["detail"] = f"SSL expires in {days_left} days"
            result["plain_english"] = (
                f"Your SSL certificate expires in {days_left} days. "
                f"Renew it soon or your website will show a security warning to visitors."
            )
        else:
            result["score"] = 0
            result["status"] = "fail"
            result["detail"] = "SSL certificate has expired"
            result["plain_english"] = (
                "Your SSL certificate has expired. Visitors see a "
                "'Not Secure' warning and many will leave your site immediately."
            )

    except ssl.SSLError:
        result["detail"] = "No valid SSL certificate found"
        result["plain_english"] = (
            "Your website is not using SSL encryption. Browsers flag it as "
            "'Not Secure' which drives visitors away and hurts your Google ranking."
        )
    except Exception as e:
        result["detail"] = f"Could not connect to {domain} on port 443"
        result["plain_english"] = (
            "We could not reach your website securely. "
            "It may not have HTTPS enabled."
        )

    return result
