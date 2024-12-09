import asyncio
import aiosmtplib
from email.mime.text import MIMEText
from config.settings import settings
from utils.logger import app_logger


class NotificationService:
    """Asynchronous service for sending notifications."""

    def __init__(self):
        self.smtp_server = settings.EMAIL_SMTP_SERVER
        self.smtp_port = settings.EMAIL_SMTP_PORT
        self.username = settings.EMAIL_USERNAME
        self.password = settings.EMAIL_PASSWORD
        self.recipients = settings.NOTIFICATION_RECIPIENTS

    async def send_anomaly_alert(self, value: float):
        """Sends an email alert when an anomaly is detected."""
        subject = "Anomaly Detected in Sales Data"
        body = f"An anomaly was detected in sales data. Detected value: {value}"
        await self.send_email(subject, body)

    async def send_email(self, subject: str, body: str):
        """Sends an email using asynchronous SMTP."""
        message = MIMEText(body)
        message['Subject'] = subject
        message['From'] = self.username
        message['To'] = ", ".join(self.recipients)

        try:
            await aiosmtplib.send(
                message,
                hostname=self.smtp_server,
                port=self.smtp_port,
                use_tls=True,
                username=self.username,
                password=self.password,
            )
            app_logger.info("Email notification sent", subject=subject)
        except Exception as e:
            app_logger.error("Failed to send email", error=str(e))
