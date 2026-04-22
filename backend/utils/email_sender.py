import os
import smtplib
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

load_dotenv()

GMAIL_USER     = os.environ["GMAIL_USER"]
GMAIL_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]


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
          <div style="display:flex;justify-content:space-between;
                      align-items:center;">
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
            <div style="text-align:right;">
              <div style="font-size:12px;color:#E24B4A;font-weight:600;">
                {score['critical']} critical
              </div>
              <div style="font-size:12px;color:#EF9F27;font-weight:600;">
                {score['warnings']} warnings
              </div>
              <div style="font-size:12px;color:#1D9E75;font-weight:600;">
                {score['passing']} passing
              </div>
            </div>
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

    # Build email
    msg = MIMEMultipart("mixed")
    msg["From"]    = f"ServOps Reports <{GMAIL_USER}>"
    msg["To"]      = to_email
    msg["Subject"] = subject

    # HTML body
    msg.attach(MIMEText(html_body, "html"))

    # PDF attachment
    with open(pdf_path, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename=servops-report-{domain}.pdf",
        )
        msg.attach(part)

    # Send via Gmail SMTP
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(GMAIL_USER, GMAIL_PASSWORD)
        smtp.sendmail(GMAIL_USER, to_email, msg.as_string())

    print(f"Report emailed to {to_email} via Gmail SMTP")
