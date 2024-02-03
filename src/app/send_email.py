import configparser
import smtplib
import time

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from database_manager import DBManager


def email_sender() -> None:
    while True:
        body: str = create_body()
        print(repr(body))
        if body:
            print(send_email(body))

        time.sleep(60)


def send_email(body: str) -> bool:
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
    subject: str = "Instructions to Validate"
    print(body)

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


def create_body() -> str:
    return '\n'.join(
        instruction[0] for instruction in
        DBManager().execute_query(f"SELECT name "
                                  f"FROM instructions "
                                  f"WHERE expiration_date BETWEEN date('now') AND date('now', '+30 days') ")
    )
