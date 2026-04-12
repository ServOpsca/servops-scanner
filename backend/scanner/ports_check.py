import socket


# Dangerous ports SMBs commonly leave open
DANGEROUS_PORTS = {
    21:   ("FTP", "Insecure file transfer — easily intercepted by attackers"),
    23:   ("Telnet", "Unencrypted remote access — credentials sent in plain text"),
    3389: ("RDP", "Remote Desktop — most common ransomware entry point"),
    445:  ("SMB", "Windows file sharing — exploited by WannaCry and similar attacks"),
    1433: ("MSSQL", "Database port exposed — direct access to your data"),
    3306: ("MySQL", "Database port exposed — direct access to your data"),
    5900: ("VNC", "Remote desktop exposed — attacker can view and control your screen"),
    8080: ("HTTP Alt", "Alternate web port exposed — often runs unpatched services"),
}

SCAN_TIMEOUT = 1.5


def check_ports(domain: str) -> dict:
    result = {
        "check": "open_ports",
        "label": "Open ports",
        "score": 100,
        "status": "pass",
        "detail": "",
        "plain_english": "",
        "open_ports": [],
    }

    try:
        ip = socket.gethostbyname(domain)
    except Exception:
        result["score"] = 0
        result["status"] = "fail"
        result["detail"] = "Could not resolve domain to IP"
        result["plain_english"] = "We could not resolve your domain to check open ports."
        return result

    open_dangerous = []

    for port, (service, risk) in DANGEROUS_PORTS.items():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(SCAN_TIMEOUT)
            conn = sock.connect_ex((ip, port))
            sock.close()
            if conn == 0:
                open_dangerous.append({
                    "port": port,
                    "service": service,
                    "risk": risk,
                })
        except Exception:
            pass

    result["open_ports"] = open_dangerous

    if not open_dangerous:
        result["score"] = 100
        result["status"] = "pass"
        result["detail"] = "No dangerous ports exposed"
        result["plain_english"] = (
            "No dangerous ports are exposed to the internet. "
            "Your server is not an easy target for automated attacks."
        )
    elif len(open_dangerous) == 1:
        p = open_dangerous[0]
        result["score"] = 20
        result["status"] = "fail"
        result["detail"] = f"Port {p['port']} ({p['service']}) is open"
        result["plain_english"] = (
            f"Port {p['port']} ({p['service']}) is open to the internet. "
            f"{p['risk']}. This should be closed or restricted immediately."
        )
    else:
        services = ", ".join([f"Port {p['port']} ({p['service']})" for p in open_dangerous])
        result["score"] = 0
        result["status"] = "fail"
        result["detail"] = f"{len(open_dangerous)} dangerous ports open"
        result["plain_english"] = (
            f"{len(open_dangerous)} dangerous ports are open to the internet: "
            f"{services}. Your server is highly vulnerable to automated attacks."
        )

    return result
