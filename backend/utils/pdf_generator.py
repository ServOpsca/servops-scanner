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


class ReportPDF(FPDF):
    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"ServOps IT Health Report — Page {self.page_no()}", align="C")


def generate_pdf_report(
    domain:  str,
    name:    str,
    results: list,
    score:   dict,
) -> str:
    pdf = ReportPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_margins(0, 0, 0)

    score_color = SCORE_COLORS.get(score["status"], (55, 138, 221))

    # ── HEADER BLOCK ──────────────────────────────────────────
    pdf.set_fill_color(15, 39, 68)
    pdf.rect(0, 0, 210, 70, "F")

    # Brand label
    pdf.set_xy(14, 10)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(123, 164, 200)
    pdf.cell(0, 6, "SERVOPS IT HEALTH REPORT", ln=True)

    # Domain title
    pdf.set_x(14)
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(255, 255, 255)
    display = f"{name} — {domain}"
    pdf.cell(0, 10, display[:55], ln=True)

    # Scan date
    pdf.set_x(14)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(123, 164, 200)
    scan_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    pdf.cell(0, 6, f"Scanned on {scan_date}", ln=True)

    # Score circle (right side)
    pdf.set_xy(155, 8)
    pdf.set_font("Helvetica", "B", 42)
    pdf.set_text_color(*score_color)
    pdf.cell(40, 20, str(score["total_score"]), align="C")

    pdf.set_xy(155, 28)
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(123, 164, 200)
    pdf.cell(40, 6, "/100", align="C")

    pdf.set_xy(155, 35)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*score_color)
    pdf.cell(40, 6, score["label"].upper(), align="C")

    # ── SUMMARY TILES ─────────────────────────────────────────
    tile_y = 48
    tiles = [
        (score["critical"], "Critical issues", (226, 75, 74)),
        (score["warnings"], "Warnings",        (239, 159, 39)),
        (score["passing"],  "Passing",          (29, 158, 117)),
    ]
    tile_x = 14
    for num, label, color in tiles:
        pdf.set_fill_color(255, 255, 255, )
        pdf.set_draw_color(255, 255, 255)
        pdf.set_fill_color(30, 55, 85)
        pdf.rect(tile_x, tile_y, 55, 16, "F")
        pdf.set_xy(tile_x, tile_y + 1)
        pdf.set_font("Helvetica", "B", 18)
        pdf.set_text_color(*color)
        pdf.cell(55, 8, str(num), align="C")
        pdf.set_xy(tile_x, tile_y + 9)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(123, 164, 200)
        pdf.cell(55, 5, label, align="C")
        tile_x += 58

    pdf.set_y(76)

    # ── SUMMARY TEXT ──────────────────────────────────────────
    pdf.set_x(14)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 6, "WHAT THIS MEANS FOR YOUR BUSINESS", ln=True)
    pdf.ln(2)

    # Left accent bar
    pdf.set_fill_color(*score_color)
    pdf.rect(14, pdf.get_y(), 3, 18, "F")

    pdf.set_fill_color(249, 250, 251)
    pdf.rect(14, pdf.get_y(), 182, 18, "F")

    summary = (
        f"Your IT health score is {score['total_score']} out of 100. "
    )
    if score["status"] == "fail":
        summary += f"Your business has serious security gaps. {score['critical']} critical issue(s) need immediate attention."
    elif score["status"] == "warn":
        summary += "Your business has some security gaps that should be addressed soon."
    else:
        summary += "Your business has a healthy IT posture. Keep monitoring regularly."

    pdf.set_xy(20, pdf.get_y() + 3)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(55, 65, 81)
    pdf.multi_cell(172, 5, summary)
    pdf.ln(4)

    # ── DETAILED FINDINGS ─────────────────────────────────────
    pdf.set_x(14)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 6, "DETAILED FINDINGS", ln=True)
    pdf.ln(2)

    for r in results:
        color     = SCORE_COLORS[r["status"]]
        bg        = STATUS_BG[r["status"]]
        border    = STATUS_BORDER[r["status"]]
        card_y    = pdf.get_y()
        card_h    = 28

        # Card background
        pdf.set_fill_color(*bg)
        pdf.set_draw_color(*border)
        pdf.rect(14, card_y, 182, card_h, "FD")

        # Badge
        pdf.set_fill_color(*color)
        pdf.set_xy(17, card_y + 4)
        pdf.set_font("Helvetica", "B", 7)
        pdf.set_text_color(255, 255, 255)
        badge_text = STATUS_LABELS[r["status"]]
        pdf.cell(18, 5, badge_text, fill=True, align="C")

        # Check label
        pdf.set_xy(38, card_y + 3)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(17, 24, 39)
        pdf.cell(120, 6, r["label"])

        # Score
        pdf.set_xy(163, card_y + 3)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(*color)
        pdf.cell(30, 6, f"{r['score']}/100", align="R")

        # Plain English text
        pdf.set_xy(17, card_y + 11)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(75, 85, 99)
        pdf.multi_cell(175, 4.5, r["plain_english"])

        new_y = pdf.get_y()
        actual_h = new_y - card_y + 3
        if actual_h > card_h:
            pdf.set_fill_color(*bg)
            pdf.set_draw_color(*border)
            pdf.rect(14, card_y, 182, actual_h, "FD")
            pdf.set_xy(17, card_y + 11)
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(75, 85, 99)
            pdf.multi_cell(175, 4.5, r["plain_english"])

        pdf.set_y(card_y + actual_h + 3)

    pdf.ln(2)

    # ── SCORE BREAKDOWN ───────────────────────────────────────
    pdf.set_x(14)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 6, "SCORE BREAKDOWN", ln=True)
    pdf.ln(2)

    for r in results:
        color = SCORE_COLORS[r["status"]]
        bar_y = pdf.get_y()

        pdf.set_x(14)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(107, 114, 128)
        pdf.cell(50, 6, r["label"])

        # Bar background
        bar_x = 66
        pdf.set_fill_color(243, 244, 246)
        pdf.rect(bar_x, bar_y + 1, 120, 4, "F")

        # Bar fill
        fill_w = int(r["score"] / 100 * 120)
        if fill_w > 0:
            pdf.set_fill_color(*color)
            pdf.rect(bar_x, bar_y + 1, fill_w, 4, "F")

        # Percentage
        pdf.set_xy(190, bar_y)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*color)
        pdf.cell(16, 6, f"{r['score']}%", align="R")
        pdf.ln(7)

    pdf.ln(4)

    # ── CTA BLOCK ─────────────────────────────────────────────
    cta_y = pdf.get_y()
    pdf.set_fill_color(15, 39, 68)
    pdf.rect(0, cta_y, 210, 55, "F")

    pdf.set_xy(14, cta_y + 6)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(123, 164, 200)
    pdf.cell(0, 5, "YOUR NEXT STEP", ln=True)

    pdf.set_x(14)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 9, "Want us to fix these issues for you?", ln=True)

    pdf.set_x(14)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(123, 164, 200)
    pdf.multi_cell(182, 5,
        "ServOps can resolve all critical and warning issues within 48 hours. "
        "Book a free 15-minute call — no obligation, no technical jargon."
    )

    btn_y = pdf.get_y() + 3
    pdf.set_fill_color(24, 95, 165)
    pdf.rect(14, btn_y, 80, 10, "F")
    pdf.set_xy(14, btn_y + 2)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(80, 6, "Book a free call — servopsca@gmail.com", align="C")

    pdf.set_xy(14, btn_y + 12)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(74, 106, 138)
    pdf.cell(0, 5, "ServOps  .  Windsor, Ontario  .  servopsca.com  .  +1 (519) 992-8997")

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
