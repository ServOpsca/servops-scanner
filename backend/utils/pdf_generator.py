import os
import uuid
from datetime import datetime
from fpdf import FPDF

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "temp_reports")
os.makedirs(OUTPUT_DIR, exist_ok=True)

SCORE_COLORS = {
    "pass": (29, 158, 117),
    "warn": (239, 159, 39),
    "fail": (226, 75, 74),
}

STATUS_LABELS = {
    "pass": "PASSING",
    "warn": "WARNING",
    "fail": "CRITICAL",
}

STATUS_BG = {
    "pass": (240, 253, 244),
    "warn": (255, 251, 235),
    "fail": (255, 245, 245),
}

STATUS_BORDER = {
    "pass": (187, 247, 208),
    "warn": (253, 230, 138),
    "fail": (254, 202, 202),
}

STRIPE_FIX        = "https://buy.stripe.com/4gMbJ1aJ44Hh1Jz3M34wM03"
STRIPE_MONITORING = "https://buy.stripe.com/7sYfZh6sOehRfAp2HZ4wM01"
STRIPE_MSP        = "https://buy.stripe.com/8x214n2cyehR2ND6Yf4wM02"


class ReportPDF(FPDF):
    def header(self):
        pass

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(180, 180, 180)
        self.cell(0, 6, f"ServOps IT Health Report - Page {self.page_no()}", align="C")


def generate_pdf_report(
    domain:  str,
    name:    str,
    results: list,
    score:   dict,
) -> str:
    pdf = ReportPDF()
    pdf.set_auto_page_break(auto=False)
    pdf.add_page()
    pdf.set_margins(0, 0, 0)

    score_color = SCORE_COLORS.get(score["status"], (55, 138, 221))

    # ── HEADER ────────────────────────────────────────────────
    pdf.set_fill_color(15, 39, 68)
    pdf.rect(0, 0, 210, 66, "F")

    pdf.set_xy(14, 9)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(123, 164, 200)
    pdf.cell(0, 5, "SERVOPS IT HEALTH REPORT", ln=True)

    pdf.set_x(14)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(255, 255, 255)
    display = f"{name} - {domain}"
    pdf.cell(0, 9, display[:55], ln=True)

    pdf.set_x(14)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(123, 164, 200)
    scan_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    pdf.cell(0, 5, f"Scanned on {scan_date}", ln=True)

    # Score (right side)
    pdf.set_xy(152, 7)
    pdf.set_font("Helvetica", "B", 38)
    pdf.set_text_color(*score_color)
    pdf.cell(44, 18, str(score["total_score"]), align="C")

    pdf.set_xy(152, 25)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(123, 164, 200)
    pdf.cell(44, 5, "/100", align="C")

    pdf.set_xy(152, 31)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*score_color)
    pdf.cell(44, 5, score["label"].upper(), align="C")

    # Tiles
    tile_y = 46
    tiles = [
        (score["critical"], "Critical", (226, 75, 74)),
        (score["warnings"], "Warnings", (239, 159, 39)),
        (score["passing"],  "Passing",  (29, 158, 117)),
    ]
    tile_x = 14
    for num, label, color in tiles:
        pdf.set_fill_color(30, 55, 85)
        pdf.rect(tile_x, tile_y, 52, 14, "F")
        pdf.set_xy(tile_x, tile_y + 1)
        pdf.set_font("Helvetica", "B", 16)
        pdf.set_text_color(*color)
        pdf.cell(52, 7, str(num), align="C")
        pdf.set_xy(tile_x, tile_y + 8)
        pdf.set_font("Helvetica", "", 7)
        pdf.set_text_color(123, 164, 200)
        pdf.cell(52, 4, label, align="C")
        tile_x += 55

    pdf.set_y(70)

    # ── SUMMARY ───────────────────────────────────────────────
    pdf.set_x(14)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 5, "WHAT THIS MEANS FOR YOUR BUSINESS", ln=True)
    pdf.ln(1)

    sum_y = pdf.get_y()
    pdf.set_fill_color(*score_color)
    pdf.rect(14, sum_y, 3, 14, "F")
    pdf.set_fill_color(249, 250, 251)
    pdf.rect(14, sum_y, 182, 14, "F")

    summary = f"Your IT health score is {score['total_score']} out of 100. "
    if score["status"] == "fail":
        summary += f"Serious security gaps found. {score['critical']} critical issue(s) need immediate attention."
    elif score["status"] == "warn":
        summary += "Some security gaps should be addressed soon to reduce risk."
    else:
        summary += "Your IT posture looks healthy. Keep monitoring regularly."

    pdf.set_xy(20, sum_y + 2)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(55, 65, 81)
    pdf.multi_cell(172, 4.5, summary)
    pdf.ln(3)

    # ── FINDINGS ──────────────────────────────────────────────
    pdf.set_x(14)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 5, "DETAILED FINDINGS", ln=True)
    pdf.ln(1)

    for r in results:
        color  = SCORE_COLORS[r["status"]]
        bg     = STATUS_BG[r["status"]]
        border = STATUS_BORDER[r["status"]]
        card_y = pdf.get_y()

        # Estimate height needed
        text_lines = len(r["plain_english"]) // 90 + 1
        card_h = 10 + (text_lines * 4.5)

        pdf.set_fill_color(*bg)
        pdf.set_draw_color(*border)
        pdf.rect(14, card_y, 182, card_h, "FD")

        pdf.set_fill_color(*color)
        pdf.set_xy(17, card_y + 3)
        pdf.set_font("Helvetica", "B", 6)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(16, 4, STATUS_LABELS[r["status"]], fill=True, align="C")

        pdf.set_xy(36, card_y + 2)
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(17, 24, 39)
        pdf.cell(120, 5, r["label"])

        pdf.set_xy(163, card_y + 2)
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*color)
        pdf.cell(30, 5, f"{r['score']}/100", align="R")

        pdf.set_xy(17, card_y + 8)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(75, 85, 99)
        pdf.multi_cell(175, 4, r["plain_english"])

        pdf.set_y(card_y + card_h + 2)

    pdf.ln(1)

    # ── SCORE BARS ────────────────────────────────────────────
    pdf.set_x(14)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 5, "SCORE BREAKDOWN", ln=True)
    pdf.ln(1)

    for r in results:
        color = SCORE_COLORS[r["status"]]
        bar_y = pdf.get_y()

        pdf.set_x(14)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(107, 114, 128)
        pdf.cell(48, 5, r["label"])

        fill_w = int(r["score"] / 100 * 118)
        pdf.set_fill_color(243, 244, 246)
        pdf.rect(64, bar_y + 1, 118, 3.5, "F")

        if fill_w > 0:
            pdf.set_fill_color(*color)
            pdf.rect(64, bar_y + 1, fill_w, 3.5, "F")

        pdf.set_xy(186, bar_y)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(*color)
        pdf.cell(18, 5, f"{r['score']}%", align="R")
        pdf.ln(5.5)

    pdf.ln(3)

    # ── PAYMENT BUTTONS ───────────────────────────────────────
    # Check if enough space remains — if not, add new page
    remaining = 282 - pdf.get_y()
    if remaining < 55:
        pdf.add_page()
        pdf.set_y(14)

    pdf.set_x(14)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 5, "WHAT WOULD YOU LIKE TO DO NEXT?", ln=True)
    pdf.ln(2)

    btn_y = pdf.get_y()

    if score["status"] != "pass":
        # Fix it button
        pdf.set_fill_color(226, 75, 74)
        pdf.rect(14, btn_y, 88, 9, "F")
        pdf.set_xy(14, btn_y + 1)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(88, 7, "Fix it for me - $200 one-time", align="C",
                 link=STRIPE_FIX)

        # Monitoring button
        pdf.set_fill_color(24, 95, 165)
        pdf.rect(106, btn_y, 90, 9, "F")
        pdf.set_xy(106, btn_y + 1)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(90, 7, "Monthly monitoring - $97/mo", align="C",
                 link=STRIPE_MONITORING)
    else:
        pdf.set_fill_color(24, 95, 165)
        pdf.rect(14, btn_y, 130, 9, "F")
        pdf.set_xy(14, btn_y + 1)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(130, 7, "Stay protected - Monthly monitoring $97/mo",
                 align="C", link=STRIPE_MONITORING)

    pdf.ln(12)

    # Book a call link
    pdf.set_x(14)
    pdf.set_font("Helvetica", "U", 8)
    pdf.set_text_color(24, 95, 165)
    pdf.cell(0, 5,
             "Book a free 15-min call - servopsca@gmail.com",
             link="mailto:servopsca@gmail.com?subject=Free call request")
    pdf.ln(8)

    # MSP box
    msp_y = pdf.get_y()
    pdf.set_fill_color(239, 246, 255)
    pdf.set_draw_color(191, 219, 254)
    pdf.rect(14, msp_y, 182, 16, "FD")

    pdf.set_xy(17, msp_y + 2)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(29, 78, 216)
    pdf.cell(0, 4, "Are you an MSP or IT provider?", ln=True)

    pdf.set_x(17)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(55, 65, 81)
    pdf.cell(138, 4, "White-label this scanner under your own brand. $149/mo.")

    pdf.set_fill_color(29, 78, 216)
    pdf.rect(158, msp_y + 4, 34, 7, "F")
    pdf.set_xy(158, msp_y + 4)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(34, 7, "Get access", align="C", link=STRIPE_MSP)

    pdf.set_y(msp_y + 20)

    # ── CTA FOOTER ────────────────────────────────────────────
    cta_y = pdf.get_y() + 2
    pdf.set_fill_color(15, 39, 68)
    pdf.rect(0, cta_y, 210, 26, "F")

    pdf.set_xy(14, cta_y + 4)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 6, "Want us to fix these issues for you?", ln=True)

    pdf.set_x(14)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(123, 164, 200)
    pdf.cell(0, 4, "ServOps resolves all issues within 48hrs. No obligation, no jargon.", ln=True)

    pdf.set_x(14)
    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(74, 106, 138)
    pdf.cell(0, 4, "ServOps | Windsor, Ontario | servopsca.com | +1 (519) 992-8997")

    # ── SAVE ──────────────────────────────────────────────────
    filename = f"servops-report-{uuid.uuid4().hex[:8]}.pdf"
    filepath = os.path.join(OUTPUT_DIR, filename)
    pdf.output(filepath)
    return filepath


def cleanup_report(filepath: str):
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception:
        pass