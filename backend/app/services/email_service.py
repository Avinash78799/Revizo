import os
import smtplib
import logging
import asyncio
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

logger = logging.getLogger("revizo.email")

class EmailService:
    """
    Transactional email delivery service for Revizo.
    Sends automated welcome emails, password reset links, and revision notices.
    Falls back gracefully to async log recording if SMTP is unconfigured in development.
    """

    SMTP_HOST = os.getenv("SMTP_HOST", "")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    SMTP_TLS = os.getenv("SMTP_TLS", "true").lower() in ("true", "1", "yes")
    EMAIL_FROM = os.getenv("EMAIL_FROM", "Revizo Medical Team <support@neetpg.pro>")

    @classmethod
    def generate_welcome_email_html(cls, full_name: Optional[str], email: str, target_year: int) -> str:
        doctor_title = f"Dr. {full_name}" if full_name and not full_name.lower().startswith("dr") else (full_name or "Doctor")
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Welcome to Revizo</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f8fafc; color: #0f172a; margin: 0; padding: 0; }}
    .container {{ max-width: 600px; margin: 30px auto; background: #ffffff; border-radius: 16px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }}
    .header {{ background: #0f172a; padding: 32px; text-align: center; }}
    .logo {{ color: #ffffff; font-size: 26px; font-weight: 900; letter-spacing: -0.5px; margin: 0; }}
    .subtitle {{ color: #38bdf8; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; margin-top: 4px; }}
    .content {{ padding: 36px 32px; }}
    h1 {{ font-size: 20px; font-weight: 800; color: #0f172a; margin-top: 0; }}
    p {{ font-size: 14px; line-height: 1.6; color: #475569; margin: 12px 0; }}
    .badge {{ display: inline-block; background: #f0fdf4; border: 1px solid #bbf7d0; color: #166534; font-size: 12px; font-weight: 700; padding: 4px 12px; border-radius: 9999px; margin-bottom: 16px; }}
    .features {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; margin: 24px 0; }}
    .feature-item {{ margin-bottom: 12px; font-size: 13px; color: #334155; }}
    .feature-item strong {{ color: #0f172a; }}
    .button-container {{ text-align: center; margin: 32px 0 16px; }}
    .cta-button {{ display: inline-block; background: #0284c7; color: #ffffff !important; text-decoration: none; font-weight: 700; font-size: 14px; padding: 14px 32px; border-radius: 10px; box-shadow: 0 2px 4px rgba(2,132,199,0.25); }}
    .footer {{ background: #f8fafc; border-top: 1px solid #e2e8f0; padding: 24px 32px; font-size: 11px; color: #94a3b8; text-align: center; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="logo">REVIZO</div>
      <div class="subtitle">NEET-PG Medical Practice & Spaced Revision</div>
    </div>
    <div class="content">
      <div class="badge">Registration Confirmed • NEET-PG {target_year}</div>
      <h1>Welcome, {doctor_title}!</h1>
      <p>Your free aspirant account on Revizo is now active. You have full, unrestricted access to our medically reviewed question bank, adaptive spaced revision scheduler, and mistake intelligence diagnostic tools.</p>
      
      <div class="features">
        <div class="feature-item">🩺 <strong>869 Medically Reviewed Questions</strong> across 19 standard medical disciplines.</div>
        <div class="feature-item">🧠 <strong>Adaptive Spaced Revision (SM-2)</strong> automatically schedules missed concepts on Day 1, 3, 7, and 14.</div>
        <div class="feature-item">⚡ <strong>Danger Zone Analytics</strong> flags high-confidence overconfidence mistakes before exam day.</div>
        <div class="feature-item">📖 <strong>Structured 4-Part Explanations</strong> with distractor refutations and high-yield takeaway pearls.</div>
      </div>

      <div class="button-container">
        <a href="https://news-modem-tropical-sharing.trycloudflare.com/dashboard" class="cta-button">Launch Practice Dashboard &rarr;</a>
      </div>

      <p style="font-size: 12px; color: #64748b; text-align: center; margin-top: 24px;">
        Registered Email: <strong>{email}</strong>
      </p>
    </div>
    <div class="footer">
      &copy; {target_year} Revizo Medical Education. Independent medical preparation platform.<br>
      Strict medical content governance with Harrison, Bailey & Love, Robbins, and Park textbook sourcing.
    </div>
  </div>
</body>
</html>"""

    @classmethod
    async def send_welcome_email(cls, to_email: str, full_name: Optional[str] = None, target_year: int = 2026):
        """
        Sends an automated welcome email asynchronously in the background.
        """
        html_body = cls.generate_welcome_email_html(full_name, to_email, target_year)
        plain_body = f"Welcome to Revizo, Dr. {full_name or 'Doctor'}!\n\nYour account has been created for NEET-PG {target_year}.\nStart your practice at https://news-modem-tropical-sharing.trycloudflare.com/dashboard"
        subject = f"Welcome to Revizo — Your NEET-PG {target_year} Preparation Starts Here"

        # Run delivery in background thread so HTTP response is instant
        asyncio.create_task(cls._send_email_async(to_email, subject, html_body, plain_body))

    @classmethod
    async def _send_email_async(cls, to_email: str, subject: str, html_content: str, text_content: str):
        try:
            if cls.SMTP_HOST and cls.SMTP_USER and cls.SMTP_PASSWORD:
                msg = MIMEMultipart("alternative")
                msg["Subject"] = subject
                msg["From"] = cls.EMAIL_FROM
                msg["To"] = to_email
                msg.attach(MIMEText(text_content, "plain"))
                msg.attach(MIMEText(html_content, "html"))

                def _deliver():
                    with smtplib.SMTP(cls.SMTP_HOST, cls.SMTP_PORT, timeout=10) as server:
                        if cls.SMTP_TLS:
                            server.starttls()
                        server.login(cls.SMTP_USER, cls.SMTP_PASSWORD)
                        server.sendmail(cls.EMAIL_FROM, [to_email], msg.as_string())

                await asyncio.to_thread(_deliver)
                logger.info(f"[EMAIL DELIVERED] Live email sent to {to_email} via {cls.SMTP_HOST}")
            else:
                logger.info(f"[EMAIL SIMULATION] Welcome email generated for {to_email} with subject: '{subject}'.")
        except Exception as e:
            logger.error(f"[EMAIL ERROR] Failed to send email to {to_email}: {e}")
