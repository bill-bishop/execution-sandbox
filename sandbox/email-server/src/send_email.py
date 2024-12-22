import smtplib
from email.mime.text import MIMEText

def send_email(sender, recipient, subject, body, smtp_server="smtp.yourserver.com", smtp_port=587, username=None, password=None):
    """
    Sends an email using the provided SMTP server.

    Args:
        sender (str): The sender's email address.
        recipient (str): The recipient's email address.
        subject (str): The email subject.
        body (str): The email body content.
        smtp_server (str): The SMTP server hostname.
        smtp_port (int): The SMTP server port.
        username (str): The username for SMTP authentication.
        password (str): The password for SMTP authentication.
    """
    # Create the email content
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    # Send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        print("Starting TLS...")
        server.starttls()  # Upgrade to a secure connection
        print("TLS started.")
        if username and password:
            server.login(username, password)
        server.sendmail(sender, [recipient], msg.as_string())
    print(f"Email sent to {recipient}")