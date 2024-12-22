import requests

def send_ascii_heart_to_grace():
    """
    Sends an ASCII art heart via email with a cute note using the Mailgun API.
    """
    api_key = "4c066e9a7f977914c62c6be2fb1f4af2-0920befd-2f95ec89"
    domain = "sandboxccab56aeaff64c5cbd555427a7919cda.mailgun.org"
    api_url = f"https://api.mailgun.net/v3/{domain}/messages"

    sender = "sandbox@sandboxccab56aeaff64c5cbd555427a7919cda.mailgun.org"
    recipient = "grace.wesson@gmail.com"
    subject = "A Heart for Grace ❤️"

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
            <p>Hi Grace,</p>
            <p>Just sending you some love and a little ASCII art magic ❤️.</p>
            <p>- Bill and His Coding Co-Captain 🚀</p>
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
send_ascii_heart_to_grace()