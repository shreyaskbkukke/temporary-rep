import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class SMTPClient:
    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def send_html_email(self, to_emails: list[str], subject: str, html_content: str):
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.username, self.password)

            for to_email in to_emails:
                msg = MIMEMultipart("alternative")
                msg["Subject"] = subject
                msg["From"] = self.username
                msg["To"] = to_email

                part = MIMEText(html_content, "html")
                msg.attach(part)

                server.sendmail(self.username, to_email, msg.as_string())
