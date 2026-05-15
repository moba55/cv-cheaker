"""
AI CV Analysis — JSON Parser & Email Sender
--------------------------------------------
Parses the structured JSON response from the AI agent and either:
  1. Prints a formatted text report (for logging/n8n)
  2. Sends it as a styled HTML email

Usage:
    python parse_result.py '{"match_score": 72, ...}'
    python parse_result.py '{"match_score": 72, ...}' --email recipient@example.com
"""

import json
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ── Email config (edit these) ────────────────────────────────────────────────
SMTP_HOST     = "smtp.gmail.com"
SMTP_PORT     = 587
SMTP_USER     = "your_email@gmail.com"       # sender email
SMTP_PASSWORD = "your_app_password_here"     # Gmail App Password
EMAIL_FROM    = "CV Checker <your_email@gmail.com>"

# ── Helpers ──────────────────────────────────────────────────────────────────

VERDICT_EMOJI = {
    "STRONG MATCH":  "🟢",
    "GOOD MATCH":    "🟡",
    "PARTIAL MATCH": "🟠",
    "WEAK MATCH":    "🔴",
}

def parse_result(raw: str) -> dict:
    """Parse the AI JSON string (handles escaped newlines from n8n)."""
    cleaned = raw.replace("\\n", "\n").replace('\\"', '"')
    # If it comes wrapped in extra quotes, strip them
    if cleaned.startswith('"') and cleaned.endswith('"'):
        cleaned = cleaned[1:-1]
    return json.loads(cleaned)


def format_text_report(data: dict) -> str:
    """Format the analysis as a readable plain-text report."""
    verdict  = data.get("verdict", "N/A")
    emoji    = VERDICT_EMOJI.get(verdict, "⚪")
    score    = data.get("match_score", 0)
    bar      = ("█" * (score // 10)).ljust(10, "░")

    lines = [
        "=" * 55,
        "   CV MATCH ANALYSIS REPORT",
        "=" * 55,
        f"  Score   : [{bar}] {score}/100",
        f"  Verdict : {emoji} {verdict}",
        "",
        "  SUMMARY",
        "  " + "-" * 40,
        f"  {data.get('summary', '')}",
        "",
        "  ✅ STRENGTHS",
        "  " + "-" * 40,
    ]
    for s in data.get("strengths", []):
        lines.append(f"   • {s}")

    lines += [
        "",
        "  ❌ GAPS",
        "  " + "-" * 40,
    ]
    for g in data.get("gaps", []):
        lines.append(f"   • {g}")

    lines += [
        "",
        "  💡 RECOMMENDATIONS",
        "  " + "-" * 40,
        f"  {data.get('recommendations', '')}",
        "",
        "  🔑 KEYWORDS MATCHED",
        f"  {', '.join(data.get('keywords_matched', []))}",
        "",
        "  ❓ KEYWORDS MISSING",
        f"  {', '.join(data.get('keywords_missing', []))}",
        "=" * 55,
    ]
    return "\n".join(lines)


def format_html_email(data: dict, candidate_name: str = "Candidate") -> str:
    """Generate a styled HTML email body."""
    verdict = data.get("verdict", "N/A")
    score   = data.get("match_score", 0)
    emoji   = VERDICT_EMOJI.get(verdict, "⚪")

    score_color = (
        "#22c55e" if score >= 70 else
        "#f59e0b" if score >= 45 else
        "#ef4444"
    )

    strengths_html = "".join(
        f'<li style="margin:6px 0; color:#d1fae5;">✅ {s}</li>'
        for s in data.get("strengths", [])
    )
    gaps_html = "".join(
        f'<li style="margin:6px 0; color:#fecaca;">❌ {g}</li>'
        for g in data.get("gaps", [])
    )
    matched_html = " ".join(
        f'<span style="background:#1e3a2f;color:#4ade80;padding:3px 10px;border-radius:20px;font-size:13px;">{k}</span>'
        for k in data.get("keywords_matched", [])
    )
    missing_html = " ".join(
        f'<span style="background:#3b1111;color:#f87171;padding:3px 10px;border-radius:20px;font-size:13px;">{k}</span>'
        for k in data.get("keywords_missing", [])
    )

    return f"""
<!DOCTYPE html>
<html>
<body style="margin:0;padding:0;background:#0f1117;font-family:Inter,Arial,sans-serif;">
  <div style="max-width:600px;margin:32px auto;background:#181c27;border:1px solid #2a2f45;border-radius:16px;overflow:hidden;">

    <!-- Header -->
    <div style="background:linear-gradient(135deg,#6366f1,#818cf8);padding:28px 32px;text-align:center;">
      <h1 style="margin:0;color:#fff;font-size:22px;font-weight:700;">CV Match Analysis</h1>
      <p style="margin:6px 0 0;color:rgba(255,255,255,.8);font-size:14px;">for {candidate_name}</p>
    </div>

    <!-- Score -->
    <div style="text-align:center;padding:32px 32px 20px;">
      <div style="display:inline-block;width:100px;height:100px;border-radius:50%;
                  border:6px solid {score_color};line-height:88px;
                  font-size:32px;font-weight:700;color:{score_color};">
        {score}
      </div>
      <p style="margin:12px 0 0;font-size:18px;font-weight:600;color:#e2e8f0;">{emoji} {verdict}</p>
    </div>

    <!-- Summary -->
    <div style="padding:0 32px 24px;">
      <p style="color:#94a3b8;font-size:14px;line-height:1.7;margin:0;">{data.get('summary','')}</p>
    </div>

    <!-- Strengths -->
    <div style="margin:0 32px 20px;background:#0d2318;border:1px solid #166534;border-radius:10px;padding:18px 20px;">
      <h3 style="margin:0 0 10px;color:#4ade80;font-size:14px;text-transform:uppercase;letter-spacing:.06em;">Strengths</h3>
      <ul style="margin:0;padding-left:18px;">{strengths_html}</ul>
    </div>

    <!-- Gaps -->
    <div style="margin:0 32px 20px;background:#1f0d10;border:1px solid #7f1d1d;border-radius:10px;padding:18px 20px;">
      <h3 style="margin:0 0 10px;color:#f87171;font-size:14px;text-transform:uppercase;letter-spacing:.06em;">Gaps</h3>
      <ul style="margin:0;padding-left:18px;">{gaps_html}</ul>
    </div>

    <!-- Recommendations -->
    <div style="margin:0 32px 20px;background:#1e1b35;border:1px solid #4338ca;border-radius:10px;padding:18px 20px;">
      <h3 style="margin:0 0 10px;color:#818cf8;font-size:14px;text-transform:uppercase;letter-spacing:.06em;">Recommendations</h3>
      <p style="margin:0;color:#c7d2fe;font-size:14px;line-height:1.7;">{data.get('recommendations','')}</p>
    </div>

    <!-- Keywords -->
    <div style="padding:0 32px 32px;">
      <p style="color:#64748b;font-size:12px;text-transform:uppercase;letter-spacing:.08em;margin:0 0 8px;">Matched Keywords</p>
      <div style="margin-bottom:14px;">{matched_html}</div>
      <p style="color:#64748b;font-size:12px;text-transform:uppercase;letter-spacing:.08em;margin:0 0 8px;">Missing Keywords</p>
      <div>{missing_html}</div>
    </div>

  </div>
</body>
</html>
"""


def send_email(to_address: str, subject: str, html_body: str, text_body: str):
    """Send the analysis as an HTML email."""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = EMAIL_FROM
    msg["To"]      = to_address

    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, to_address, msg.as_string())
    print(f"✅ Email sent to {to_address}")


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_result.py '<json_string>' [--email recipient@example.com]")
        sys.exit(1)

    raw_json = sys.argv[1]
    data     = parse_result(raw_json)
    report   = format_text_report(data)

    print(report)

    # Optional: send email
    if "--email" in sys.argv:
        idx        = sys.argv.index("--email")
        to_address = sys.argv[idx + 1]
        html_body  = format_html_email(data, candidate_name="Candidate")
        verdict    = data.get("verdict", "Result")
        score      = data.get("match_score", 0)
        send_email(
            to_address=to_address,
            subject=f"CV Analysis: {verdict} ({score}/100)",
            html_body=html_body,
            text_body=report,
        )
