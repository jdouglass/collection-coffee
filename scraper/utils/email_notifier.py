import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.config_loader import get_env_variable
from config.logger_config import logger


class EmailNotifier:
    def __init__(self):
        self.email_address = get_env_variable('EMAIL_ADDRESS')
        self.password = get_env_variable('EMAIL_PASSWORD')
        self.server = 'smtp.gmail.com'
        self.port = 587

    def send_email(self, receiver_email, subject, body):
        message = MIMEMultipart()
        message["From"]: self.email_address
        message["To"]: receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        try:
            server = smtplib.SMTP(self.server, self.port)
            server.ehlo()
            server.starttls()
            server.login(self.email_address, self.password)
            server.sendmail(self.email_address,
                            self.email_address, message.as_string())
            server.quit()
            logger.info("Email sents successfully")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")

    def send_error_notification(self, error_message):
        subject = "Alert: An Error Occurred in Your Application"
        self.send_email(self.email_address, subject,
                        f"An error occurred: \n\n{error_message}")
