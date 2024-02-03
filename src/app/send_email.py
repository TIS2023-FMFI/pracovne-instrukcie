import configparser
import smtplib
import time
import logging
import re
from datetime import datetime, timedelta

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from database_manager import DBManager


def email_sender() -> None:
    logging.basicConfig(filename='email_sender.log', level=logging.INFO, format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    while True:
        if is_more_than_seven_days_ago(extract_time_from_log()):
            body: str = create_body()
            logging.info('Email was sent!')
            if body:
                print(str(datetime.now()) + ' - ' + 'Email was sent!' if send_email(body) else 'No email :(')

        time.sleep(300)


def extract_time_from_log(log_file_path: str = 'email_sender.log') -> str | None:
    timestamp_pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'

    with open(log_file_path, 'r') as log_file:
        last_line = None
        for line in log_file:
            last_line = line

        if last_line:
            timestamp_match = re.search(timestamp_pattern, last_line)
            if timestamp_match:
                return timestamp_match.group()

        return None


def is_more_than_seven_days_ago(log_timestamp_str: str | None) -> bool:
    if log_timestamp_str is None:
        return True

    log_timestamp = datetime.strptime(log_timestamp_str, '%Y-%m-%d %H:%M:%S')
    time_difference = datetime.now() - log_timestamp

    return time_difference.days >= 7


def send_email(body: str) -> bool:
    # Read configuration from file
    config: configparser = configparser.ConfigParser()
    config.read('config.ini')

    # Retrieve values from the configuration
    sender_email: str = config.get('Email', 'sender_email')
    sender_password: str = config.get('Email', 'sender_password')
    recipient_email: str = config.get('Email', 'recipient_email')
    host_server: str = config.get('Email', 'host_server')
    host_port: int = int(config.get('Email', 'host_port'))

    # Create the email message
    subject: str = 'Instructions to Validate'

    message: MIMEMultipart = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain', 'utf-8'))

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
        str(round(instruction[1])) + 'days' + '  ---  ' + str(instruction[0]) for instruction in
        DBManager().execute_query(f"SELECT name, julianday(DATE(expiration_date)) - julianday(DATE('now')) "
                                  f"FROM instructions "
                                  f"WHERE expiration_date BETWEEN date('now') AND date('now', '+31 days') "
                                  f"ORDER BY expiration_date ")
    )
