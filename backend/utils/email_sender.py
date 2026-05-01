import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

BREVO_API_KEY    = os.environ["BREVO_API_KEY"]
BREVO_FROM_EMAIL = os.environ.get("BREVO_FROM_EMAIL", "servopsca@gmail.com")
BREVO_FROM_NAME  = os.environ.get("BREVO_FROM_NAME", "ServOps Reports")
BREVO_API_URL    = "https://api.brevo.com/v3/smtp/email"

STRIPE_FIX        = "https://buy.stripe.com/4gMbJ1aJ44Hh1Jz3M34wM03"
STRIPE_MONITORING = "https://buy.stripe.com/7sYfZh6sOehRfAp2HZ4wM01"
STRIPE_MSP        = "https://buy.stripe.com/8x214n2cyehR2ND6Yf4wM02"


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

    # Payment buttons — show Fix it only if issues exist
    fix_button = ""
    if score["status"] != "pass":
        fix_button = f"""
        <a href="{STRIPE_FIX}"
           style="display:block;background:#E24B4A;color:#fff;
                  padding:13px 24px;border-radius:8px;text-decoration:none;
                  font-size:14px;font-weight:600;text-align:center;
                  margin-bottom:10px;">
          Fix it for me — $200 one-time →
        </a>
        """

    html_body = f"""
    <div style="font-family:-apple-system,sans-serif;max-width:540px;
                margin:0 auto;color:#1a1a2e;">

      <!-- HEADER -->
      <div style="background:#0F2744;padding:24px 28px;
                  border-radius:10px 10px 0 0;">
        <span style="font-size:12px;color:#7BA4C8;
                     font-weight:600;letter-spacing:1px;">SERVOPS</span>
        <h1 style="font-size:20px;color:#fff;margin:8px 0 0;">
          Your IT Health Report is ready
        </h1>
      </div>

      <!-- BODY -->
      <div style="background:#f9fafb;padding:24px 28px;
                  border:1px solid #e5e7eb;border-top:none;
                  border-radius:0 0 10px 10px;">

        <p style="margin:0 0 16px;color:#374151;font-size:14px;">
          Hi {to_name}, your free IT health scan for
          <strong>{domain}</strong> is complete.
        </p>

        <!-- SCORE CARD -->
        <div style="background:#fff;border:1px solid #e5e7eb;
                    border-radius:10px;padding:20px;margin-bottom:20px;">
          <div style="display:flex;justify-content:space-between;
                      align-items:center;flex-wrap:wrap;gap:12px;">
            <div>
              <div style="font-size:11px;color:#9CA3AF;
                          text-transform:uppercase;letter-spacing:1px;">
                Overall score
              </div>
              <div style="font-size:36px;font-weight:700;
                          color:{'#E24B4A' if score['status']=='fail'
                                 else '#EF9F27' if score['status']=='warn'
                                 else '#1D9E75'};">
                {score['total_score']}/100
              </div>
              <div style="font-size:13px;color:#6B7280;">
                {score['label']}
              </div>
            </div>
            <div style="display:flex;gap:16px;">
              <div style="text-align:center;">
                <div style="font-size:22px;font-weight:700;color:#E24B4A;">
                  {score['critical']}
                </div>
                <div style="font-size:11px;color:#9CA3AF;">Critical</div>
              </div>
              <div style="text-align:center;">
                <div style="font-size:22px;font-weight:700;color:#EF9F27;">
                  {score['warnings']}
                </div>
                <div style="font-size:11px;color:#9CA3AF;">Warnings</div>
              </div>
              <div style="text-align:center;">
                <div style="font-size:22px;font-weight:700;color:#1D9E75;">
                  {score['passing']}
                </div>
                <div style="font-size:11px;color:#9CA3AF;">Passing</div>
              </div>
            </div>
          </div>
        </div>

        <p style="margin:0 0 20px;color:#374151;font-size:14px;">
          Your full report is attached as a PDF with plain-English
          explanations of every finding and exactly what needs to be fixed.
        </p>

        {'<p style="margin:0 0 16px;color:#991B1B;font-weight:600;font-size:14px;">You have ' + str(score["critical"]) + ' critical issue' + ('s' if score["critical"] > 1 else '') + ' that require immediate attention.</p>' if score["critical"] > 0 else ''}

        <!-- PAYMENT BUTTONS -->
        <div style="margin-bottom:20px;">
          <div style="font-size:12px;color:#9CA3AF;
                      text-transform:uppercase;letter-spacing:1px;
                      margin-bottom:12px;">
            What would you like to do next?
          </div>

          {fix_button}

          <a href="{STRIPE_MONITORING}"
             style="display:block;background:#185FA5;color:#fff;
                    padding:13px 24px;border-radius:8px;text-decoration:none;
                    font-size:14px;font-weight:600;text-align:center;
                    margin-bottom:10px;">
            Monthly monitoring — $97/mo →
          </a>

          <a href="mailto:servopsca@gmail.com?subject=Free call - {domain}"
             style="display:block;background:#fff;color:#374151;
                    padding:12px 24px;border-radius:8px;text-decoration:none;
                    font-size:13px;text-align:center;
                    border:1px solid #e5e7eb;">
            Book a free 15-min call instead
          </a>
        </div>

        <!-- MSP CALLOUT -->
        <div style="background:#EFF6FF;border:1px solid #BFDBFE;
                    border-radius:8px;padding:14px 16px;margin-bottom:20px;">
          <div style="font-size:12px;font-weight:600;color:#1D4ED8;
                      margin-bottom:4px;">
            Are you an MSP or IT provider?
          </div>
          <div style="font-size:12px;color:#374151;margin-bottom:10px;">
            White-label this scanner under your own brand and offer it
            to all your clients. $149/mo.
          </div>
          <a href="{STRIPE_MSP}"
             style="display:inline-block;background:#1D4ED8;color:#fff;
                    padding:8px 16px;border-radius:6px;text-decoration:none;
                    font-size:12px;font-weight:600;">
            Get MSP access →
          </a>
        </div>

        <p style="margin:0;font-size:11px;color:#9CA3AF;line-height:1.6;">
          ServOps - Windsor, Ontario - servopsca.com - +1 (519) 992-8997<br/>
          You received this because you ran a free scan at vulscanner.netlify.app
        </p>
      </div>
    </div>
    """

    # Read and encode PDF
    with open(pdf_path, "rb") as f:
        pdf_base64 = base64.b64encode(f.read()).decode("utf-8")

    payload = {
        "sender": {
            "name":  BREVO_FROM_NAME,
            "email": BREVO_FROM_EMAIL,
        },
        "to": [{"email": to_email, "name": to_name}],
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
