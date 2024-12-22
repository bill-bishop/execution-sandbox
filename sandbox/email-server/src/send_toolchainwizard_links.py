import requests

def send_toolchainwizard_links():
    """
    Sends an email containing links to register the domain toolchainwizard.com.
    """
    api_key = "4c066e9a7f977914c62c6be2fb1f4af2-0920befd-2f95ec89"
    domain = "sandboxccab56aeaff64c5cbd555427a7919cda.mailgun.org"
    api_url = f"https://api.mailgun.net/v3/{domain}/messages"

    sender = "sandbox@sandboxccab56aeaff64c5cbd555427a7919cda.mailgun.org"
    recipient = "will.h.bishop@gmail.com"
    subject = "ToolchainWizard Domain Links"

    body = """
    <html>
        <body>
            <h1>Register ToolchainWizard.com</h1>
            <p>The domain <strong>toolchainwizard.com</strong> is available for registration. You can use the following links to purchase it:</p>
            <ul>
                <li><a href="https://www.namecheap.com/domains/registration/results/?domain=toolchainwizard.com">Register on Namecheap</a></li>
                <li><a href="https://domains.google.com">Register on Google Domains</a></li>
                <li><a href="https://www.godaddy.com">Register on GoDaddy</a></li>
            </ul>
            <p>Let me know if you'd like help setting up DNS or configuring the domain!</p>
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
send_toolchainwizard_links()