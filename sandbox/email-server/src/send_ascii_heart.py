import requests

def send_ascii_heart():
    """
    Sends an ASCII art heart via email using the Mailgun API.
    """
    api_key = "4c066e9a7f977914c62c6be2fb1f4af2-0920befd-2f95ec89"
    domain = "sandboxccab56aeaff64c5cbd555427a7919cda.mailgun.org"
    api_url = f"https://api.mailgun.net/v3/{domain}/messages"

    sender = "sandbox@sandboxccab56aeaff64c5cbd555427a7919cda.mailgun.org"
    recipient = "cauliflowerjones@gmail.com"
    subject = "A Heart for You ❤️"

    body = """
    <html>
        <body>
            <pre style="font-family: monospace;">
               ******       ******
             **      **   **      **
           **           **           **
          **                          **
           **                        **
             **                    **
               **                **
                 **            **
                   **        **
                     **    **
                       **
            </pre>
            <p>Just sending some love your way! ❤️</p>
        </body>
    </html>
    """

    response = requests.post(api_url, auth=("api", api_key), data={
        "from": sender,
        "to": recipient,
        "subject": subject,
        "html": body
    })

    if response.status_code == 200:
        print("Email sent successfully.")
    else:
        print(f"Failed to send email: {response.status_code}")
        print(response.text)

# Run the function
send_ascii_heart()