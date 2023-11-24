import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# TODO: Set values from the configuration
sender_email: str = ""
sender_password: str = ""
recipient_email: str = ""
host_server: str = ""

host_port: int = 587  # SMTP port

# Create the email message
subject: str = "This is the subject"
body: str = "This is the body example"

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

print('E-mail was successfully sent!')
