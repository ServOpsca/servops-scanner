import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

BREVO_API_KEY    = os.environ["BREVO_API_KEY"]
BREVO_FROM_EMAIL = os.environ.get("BREVO_FROM_EMAIL", "servopsca@gmail.com")
BREVO_FROM_NAME  = os.environ.get("BREVO_FROM_NAME", "ServOps Reports")
BREVO_API_URL    = "https://api.brevo.com/v3/smtp/email"


def send_report_email(
    to_email:  str,
    to_name:   str,
    domain:    str,
    score:     dict,
    pdf_path:  str,
):
    score_emoji = (
        "🔴" if score["status"] == "fail" else
        "🟡" if score["status"] == "warn" else
        "🟢"
    )

    subject = (
        f"{score_emoji} Your IT Health Report - "
        f"{domain} scored {score['total_score']}/100"
    )

    html_body = f"""
    <div style="font-family:-apple-system,sans-serif;max-width:520px;
                margin:0 auto;color:#1a1a2e;">

      <div style="background:#0F2744;padding:24px 28px;
                  border-radius:10px 10px 0 0;">
        <div style="margin-bottom:4px;">
          <span style="font-size:12px;color:#7BA4C8;
                       font-weight:600;">SERVOPS</span>
        </div>
        <h1 style="font-size:20px;color:#fff;margin:0;">
          Your IT Health Report is ready
        </h1>
      </div>

      <div style="background:#f9fafb;padding:24px 28px;
                  border:1px solid #e5e7eb;border-top:none;">
        <p style="margin:0 0 16px;color:#374151;">
          Hi {to_name}, your free IT health scan for
          <strong>{domain}</strong> is complete.
        </p>

        <div style="background:#fff;border:1px solid #e5e7eb;
                    border-radius:8px;padding:16px;margin-bottom:20px;">
          <div>
            <div style="font-size:11px;color:#9CA3AF;
                        text-transform:uppercase;letter-spacing:1px;">
              Overall score
            </div>
            <div style="font-size:32px;font-weight:700;
                        color:{'#E24B4A' if score['status']=='fail'
                               else '#EF9F27' if score['status']=='warn'
                               else '#1D9E75'};">
              {score['total_score']}/100
            </div>
            <div style="font-size:12px;color:#6B7280;">
              {score['label']}
            </div>
          </div>
          <div style="margin-top:12px;">
            <span style="font-size:12px;color:#E24B4A;
                         font-weight:600;margin-right:12px;">
              {score['critical']} critical
            </span>
            <span style="font-size:12px;color:#EF9F27;
                         font-weight:600;margin-right:12px;">
              {score['warnings']} warnings
            </span>
            <span style="font-size:12px;color:#1D9E75;font-weight:600;">
              {score['passing']} passing
            </span>
          </div>
        </div>

        <p style="margin:0 0 16px;color:#374151;">
          Your full report is attached as a PDF. It includes plain-English
          explanations of every finding and exactly what needs to be fixed.
        </p>

        {'<p style="margin:0 0 20px;color:#991B1B;font-weight:500;">You have ' + str(score["critical"]) + ' critical issue' + ('s' if score["critical"] > 1 else '') + ' that require immediate attention.</p>' if score["critical"] > 0 else ''}

        <a href="mailto:servopsca@gmail.com?subject=Fix Request - {domain}"
           style="display:inline-block;background:#185FA5;color:#fff;
                  padding:12px 24px;border-radius:8px;text-decoration:none;
                  font-size:13px;font-weight:600;">
          Book a free call with ServOps
        </a>

        <p style="margin:20px 0 0;font-size:11px;color:#9CA3AF;">
          ServOps - Windsor, Ontario - servopsca.com - +1 (519) 992-8997<br/>
          You received this because you ran a free scan at vulscanner.netlify.app
        </p>
      </div>
    </div>
    """

    # Read and encode PDF as base64
    with open(pdf_path, "rb") as f:
        pdf_base64 = base64.b64encode(f.read()).decode("utf-8")

    # Brevo API payload
    payload = {
        "sender": {
            "name":  BREVO_FROM_NAME,
            "email": BREVO_FROM_EMAIL,
        },
        "to": [
            {
                "email": to_email,
                "name":  to_name,
            }
        ],
        "subject":     subject,
        "htmlContent": html_body,
        "attachment": [
            {
                "content": pdf_base64,
                "name":    f"servops-report-{domain}.pdf",
            }
        ],
    }

    headers = {
        "accept":       "application/json",
        "content-type": "application/json",
        "api-key":      BREVO_API_KEY,
    }

    response = requests.post(
        BREVO_API_URL,
        json=payload,
        headers=headers,
        timeout=30,
    )

    if response.status_code not in (200, 201):
        raise Exception(
            f"Brevo API error {response.status_code}: {response.text}"
        )

    print(f"Report emailed to {to_email} via Brevo")
    return response.json()
