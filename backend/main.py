from dotenv import load_dotenv
load_dotenv()

import asyncio
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor

from scanner.ssl_check     import check_ssl
from scanner.email_check   import check_email_security
from scanner.ports_check   import check_ports
from scanner.headers_check import check_headers
from scanner.dns_check     import check_dns
from utils.scorer          import calculate_total_score
from utils.db              import save_scan
from utils.pdf_generator   import generate_pdf_report, cleanup_report
from utils.email_sender    import send_report_email

app = FastAPI(title="ServOps IT Scanner API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://vulscanner.netlify.app",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

executor = ThreadPoolExecutor(max_workers=10)


class ScanRequest(BaseModel):
    domain: str
    email:  str
    name:   str


def clean_domain(domain: str) -> str:
    domain = domain.strip().lower()
    domain = domain.replace("https://", "").replace("http://", "")
    domain = domain.split("/")[0]
    return domain


def send_report_background(
    to_email: str,
    to_name:  str,
    domain:   str,
    results:  list,
    score:    dict,
):
    pdf_path = None
    try:
        pdf_path = generate_pdf_report(
            domain  = domain,
            name    = to_name,
            results = results,
            score   = score,
        )
        send_report_email(
            to_email = to_email,
            to_name  = to_name,
            domain   = domain,
            score    = score,
            pdf_path = pdf_path,
        )
        print(f"Report emailed to {to_email} for {domain}")
    except Exception as e:
        print(f"Report email failed: {e}")
    finally:
        if pdf_path:
            cleanup_report(pdf_path)


@app.post("/scan")
async def run_scan(req: ScanRequest, background_tasks: BackgroundTasks):
    domain = clean_domain(req.domain)
    loop   = asyncio.get_event_loop()

    # Run all 5 checks in parallel
    tasks = [
        loop.run_in_executor(executor, check_ssl,            domain),
        loop.run_in_executor(executor, check_email_security, domain),
        loop.run_in_executor(executor, check_ports,          domain),
        loop.run_in_executor(executor, check_headers,        domain),
        loop.run_in_executor(executor, check_dns,            domain),
    ]

    results = list(await asyncio.gather(*tasks))
    score   = calculate_total_score(results)

    # Save to Supabase
    try:
        scan_id = save_scan(req.domain, req.email, req.name, results, score)
    except Exception as e:
        scan_id = None
        print(f"DB save failed: {e}")

    # Send PDF report in background (non-blocking)
    background_tasks.add_task(
        send_report_background,
        to_email = req.email,
        to_name  = req.name,
        domain   = domain,
        results  = results,
        score    = score,
    )

    return {
        "scan_id": scan_id,
        "domain":  domain,
        "score":   score,
        "results": results,
    }


@app.get("/health")
def health():
    return {"status": "ok", "service": "ServOps Scanner API"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://YOUR-SITE.netlify.app",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)