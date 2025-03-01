from typing import Any
from smtplib import SMTP_SSL, SMTP, SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging

class SendMail:
    """
    MessageConfig:
    - Initialize the email service with custom SMTP settings.
    - SMTP_HOST=smtp.gmail.com  #``Change to smtp.office365.com or smtp.sendgrid.net if needed``
    - PORT=587
    - USE_TLS=True
    - USE_SSL=False
    - SENDER
    - PASSWORD
    """
    def __init__(self, config=None) -> None:
        self.config = config
        default_config = {
            "SMTP_HOST": "smtp.gmail.com",
            "SENDER": None,
            "PASSWORD": None,
            "PORT": 465,
            "USE_TLS": True,
            "USE_SSL": False
        }

        self.config = default_config.copy()
        if config:
            self.config.update(config)

        self.hostname = self.config.get("SMTP_HOST")
        self.use_tls = self.config.get("USE_TLS")
        self.use_ssl = self.config.get("USE_SSL")
        self.sender = self.config.get("SENDER")
        self.password = self.config.get("PASSWORD")

    def send_email(self, 
        recipient: list, 
        content:Any, 
        subject: str, 
        content_type:str = "plain"
        ):
        """
        Args:
            subject (str): Email subject.
            recipient (str) : recipient
            content (str): Email body.
            content_type (str): "plain" for plaintext or "html" for HTML email.
        Returns:
            bool: True if the email was sent successfully, False otherwise.
        """

        if not self.sender or not self.password:
          logging.error("❌ Sender email and password must be configured.")
          return False

        port = 465 if self.use_ssl else 587

        message = MIMEMultipart("alternative")
        message["From"] = self.sender
        message["To"] = ", ".join(recipient)
        message["Subject"] = subject
        message.attach(MIMEText(content, content_type, "utf-8"))


        try:
            logging.info(f"📧 Connecting to SMTP server {self.hostname} on port {port}...")

            if self.use_ssl:
                smtp_client = SMTP_SSL(self.hostname, port, timeout=30)
            else:
                smtp_client = SMTP(self.hostname, port, timeout=30)

            smtp_client.ehlo()

            if self.use_tls and not self.use_ssl:
                logging.info("🔒 Starting TLS...")
                smtp_client.starttls()

            logging.info(f"🔑 Logging in as {self.sender}...")
            smtp_client.login(self.sender, self.password)

            logging.info("📩 Sending email...")
            smtp_client.send_message(message)

            logging.info("✅ Email sent successfully.")
            return True

        except SMTPException:
            logging.exception("📧 SMTP error occurred")
        except Exception:
            logging.exception("❌ Failed to send email")
        finally:
            smtp_client.quit()
        return False