import os
import uuid
import pdfkit
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
OUTPUT_DIR    = os.path.join(os.path.dirname(__file__), "temp_reports")

os.makedirs(OUTPUT_DIR, exist_ok=True)

SCORE_COLORS = {
    "pass": "#1D9E75",
    "warn": "#EF9F27",
    "fail": "#E24B4A",
}

# Windows path to wkhtmltopdf
WKHTMLTOPDF_PATH = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"

PDFKIT_CONFIG = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

PDFKIT_OPTIONS = {
    "page-size":       "A4",
    "margin-top":      "0mm",
    "margin-right":    "0mm",
    "margin-bottom":   "0mm",
    "margin-left":     "0mm",
    "encoding":        "UTF-8",
    "no-outline":      None,
    "enable-local-file-access": None,
    "quiet":           "",
}


def generate_pdf_report(
    domain:  str,
    name:    str,
    results: list,
    score:   dict,
) -> str:
    env      = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template("report_template.html")

    html_content = template.render(
        domain       = domain,
        name         = name,
        scan_date    = datetime.now().strftime("%B %d, %Y at %I:%M %p"),
        total_score  = score["total_score"],
        score_label  = score["label"],
        score_status = score["status"],
        score_color  = SCORE_COLORS.get(score["status"], "#378ADD"),
        critical     = score["critical"],
        warnings     = score["warnings"],
        passing      = score["passing"],
        results      = results,
    )

    filename = f"servops-report-{uuid.uuid4().hex[:8]}.pdf"
    filepath = os.path.join(OUTPUT_DIR, filename)

    pdfkit.from_string(
        html_content,
        filepath,
        configuration = PDFKIT_CONFIG,
        options       = PDFKIT_OPTIONS,
    )

    return filepath


def cleanup_report(filepath: str):
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception:
        pass
