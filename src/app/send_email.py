import configparser
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(names_of_instructions: list[str]) -> bool:
    # Read configuration from file
    config: configparser = configparser.ConfigParser()
    config.read('config.ini')

    # Retrieve values from the configuration
    sender_email: str = config.get('Email', 'sender_email')
    sender_password: str = config.get('Email', 'sender_password')
    recipient_email: str = config.get('Email', 'recipient_email')
    host_server: str = config.get('Email', "host_server")
    host_port: int = int(config.get('Email', "host_port"))

    # Create the email message
    subject: str = ""
    body: str = create_body(names_of_instructions)

    message: MIMEMultipart = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain", "utf-8"))

    # Connect to the SMTP server
    with smtplib.SMTP(host_server, host_port) as server:
        # Start TLS for security
        server.starttls()

        # Login to the email account
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, recipient_email, message.as_string())

    return True


def create_body(names_of_instructions: list[str]) -> str:
    body = ""
    for instruction in names_of_instructions:
        body += f'{instruction}\n'

    return body
