import requests

def send_email_via_api(api_url, api_key, sender, recipient, subject, body):
    """
    Sends an email using a public email API.

    Args:
        api_url (str): The API endpoint URL for sending emails.
        api_key (str): The API key for authentication.
        sender (str): The sender's email address.
        recipient (str): The recipient's email address.
        subject (str): The email subject.
        body (str): The email body content.

    Returns:
        Response: The HTTP response object from the API call.
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "from": sender,
        "to": [recipient],
        "subject": subject,
        "text": body
    }

    response = requests.post(api_url, json=payload, headers=headers)
    return response

# Example usage
if __name__ == "__main__":
    API_URL = "https://api.mailgun.net/v3/YOUR_DOMAIN_NAME/messages"
    API_KEY = "YOUR_API_KEY"

    sender = "you@yourdomain.com"
    recipient = "will.h.bishop@gmail.com"
    subject = "Test Email from API"
    body = "This is a test email sent via a public email API."

    response = send_email_via_api(API_URL, API_KEY, sender, recipient, subject, body)

    if response.status_code == 200:
        print("Email sent successfully!")
    else:
        print("Failed to send email:", response.status_code, response.text)