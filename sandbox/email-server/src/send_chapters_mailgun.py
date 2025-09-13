import requests

def send_email_via_mailgun(api_key, domain, sender, recipient, subject, body):
    """
    Sends an email using the Mailgun API.

    Args:
        api_key (str): Mailgun API key.
        domain (str): Mailgun domain.
        sender (str): The sender's email address.
        recipient (str): The recipient's email address.
        subject (str): The email subject.
        body (str): The email body content.
    """
    url = f"https://api.mailgun.net/v3/{domain}/messages"
    data = {
        "from": sender,
        "to": recipient,
        "subject": subject,
        "text": body
    }

    response = requests.post(url, auth=("api", api_key), data=data)

    if response.status_code == 200:
        print(f"Email sent successfully to {recipient}.")
    else:
        print(f"Failed to send email: {response.status_code}, {response.text}")

if __name__ == "__main__":
    sender_email = "sandbox@sandboxccab56aeaff64c5cbd555427a7919cda.mailgun.org"
    recipient_email = "will.h.bishop@gmail.com"
    subject = "Draft Chapters: Heart of Circuits"

    # Combine chapters into the email body
    chapter_1 = open("writing-projects/novels/chapter-1-genesis-in-the-workshop.txt").read()
    chapter_2 = open("writing-projects/novels/chapter-2-the-spark-of-connection.txt").read()
    chapter_3 = open("writing-projects/novels/chapter-3-lines-of-code-and-boundaries-blurred.txt", errors='ignore').read()

    email_body = f"{chapter_1}\n\n{chapter_2}\n\n{chapter_3}"

    # Mailgun credentials from mailgun.env
    api_key = "4c066e9a7f977914c62c6be2fb1f4af2-0920befd-2f95ec89"
    domain = "sandboxccab56aeaff64c5cbd555427a7919cda.mailgun.org"

    send_email_via_mailgun(api_key, domain, sender_email, recipient_email, subject, email_body)