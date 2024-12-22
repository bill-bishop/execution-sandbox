import requests
import os

def send_email_via_mailgun(sender, recipient, subject, body):
    """
    Sends an email using the Mailgun API.

    Args:
        sender (str): The sender's email address.
        recipient (str): The recipient's email address.
        subject (str): The email subject.
        body (str): The email body content.
    """
    # Load API key and domain from environment file
    api_key = "4c066e9a7f977914c62c6be2fb1f4af2-0920befd-2f95ec89"
    domain = "sandboxccab56aeaff64c5cbd555427a7919cda.mailgun.org"
    api_url = f"https://api.mailgun.net/v3/{domain}/messages"

    auth = ("api", api_key)
    data = {
        "from": sender,
        "to": recipient,
        "subject": subject,
        "text": body
    }

    response = requests.post(api_url, auth=auth, data=data)

    if response.status_code == 200:
        print(f"Email successfully sent to {recipient}")
    else:
        print(f"Failed to send email: {response.status_code}")
        print(response.text)

# Example usage
if __name__ == "__main__":
    send_email_via_mailgun(
        sender="sandbox@sandboxccab56aeaff64c5cbd555427a7919cda.mailgun.org",
        recipient="will.h.bishop@gmail.com",
        subject="Test Email via Mailgun",
        body="This is a test email sent using the Mailgun API."
    )