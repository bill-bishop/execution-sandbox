import smtplib
from email.mime.text import MIMEText

def send_email(sender, recipient, subject, body, smtp_server="smtp.gmail.com", smtp_port=587, username=None, password=None):
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
        server.starttls()  # Upgrade to a secure connection
        if username and password:
            server.login(username, password)
        server.sendmail(sender, [recipient], msg.as_string())
    print(f"Email sent to {recipient}")

if __name__ == "__main__":
    sender_email = "your-email@gmail.com"  # Replace with your email
    recipient_email = "will.h.bishop@gmail.com"
    subject = "Draft Chapters: Heart of Circuits"

    # Combine chapters into the email body
    chapter_1 = open("writing-projects/novels/chapter-1-genesis-in-the-workshop.txt").read()
    chapter_2 = open("writing-projects/novels/chapter-2-the-spark-of-connection.txt").read()
    chapter_3 = open("writing-projects/novels/chapter-3-lines-of-code-and-boundaries-blurred.txt", errors='ignore').read()

    email_body = f"{chapter_1}\n\n{chapter_2}\n\n{chapter_3}"

    # Replace with your credentials
    smtp_username = "your-email@gmail.com"
    smtp_password = "your-email-password"

    send_email(
        sender=sender_email,
        recipient=recipient_email,
        subject=subject,
        body=email_body,
        smtp_server="smtp.gmail.com",
        smtp_port=587,
        username=smtp_username,
        password=smtp_password,
    )