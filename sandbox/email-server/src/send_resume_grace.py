import requests

def send_resume_to_grace():
    """
    Sends the formatted resume to Grace via email using the Mailgun API.
    """
    api_key = "4c066e9a7f977914c62c6be2fb1f4af2-0920befd-2f95ec89"
    domain = "sandboxccab56aeaff64c5cbd555427a7919cda.mailgun.org"
    api_url = f"https://api.mailgun.net/v3/{domain}/messages"

    sender = "sandbox@sandboxccab56aeaff64c5cbd555427a7919cda.mailgun.org"
    recipient = "grace.wesson@gmail.com"
    subject = "Bill Bishop - Resume"

    body = """
    <html>
        <body>
            <h1>Bill Bishop</h1>
            <h2>Contact</h2>
            <ul>
                <li><b>Email:</b> YourEmailHere</li>
                <li><b>GitHub:</b> <a href='https://github.com/bill-bishop'>https://github.com/bill-bishop</a></li>
                <li><b>NPM:</b> <a href='https://npmjs.com/~william-mcmillian'>https://npmjs.com/~william-mcmillian</a></li>
                <li><b>Portfolio:</b> YourWebsiteHere</li>
            </ul>

            <h2>Summary</h2>
            <p>A passionate software engineer specializing in automation, developer tools, and artificial intelligence. With extensive experience in web development, open-source contributions, and innovative side projects, I aim to build tools that empower developers and optimize workflows. I am highly skilled in creating modular, maintainable systems and have a strong focus on user experience.</p>

            <h2>Skills</h2>
            <ul>
                <li><b>Languages:</b> JavaScript, Python, Rust, Bash, HTML/CSS</li>
                <li><b>Frameworks:</b> Vue.js, Node.js, Redux, Phaser.io</li>
                <li><b>Tools:</b> Git, Docker, Mailgun API, Selenium, Postfix</li>
                <li><b>Key Skills:</b> Automation, Developer Tools, AI Integration, Open Source</li>
            </ul>

            <h2>Open Source Projects</h2>
            <ul>
                <li><b>querydom:</b> <a href='https://github.com/bill-bishop/querydom'>Command-Line DOM Querying</a></li>
                <li><b>argvark:</b> <a href='https://github.com/bill-bishop/argvark'>Intuitive Command-Line Parsing for Node.js</a></li>
                <li><b>tetriscore:</b> <a href='https://github.com/bill-bishop/tetriscore'>Node.js Library Implementing Tetris Core Logic</a></li>
                <li><b>redux-ecosystem-links:</b> <a href='https://github.com/bill-bishop/redux-ecosystem-links'>Categorized Redux-Related Addons</a></li>
                <li><b>rust-webserver:</b> <a href='https://github.com/bill-bishop/rust-webserver'>Multi-threaded Rust Web Server</a></li>
            </ul>

            <h2>Recent Projects</h2>
            <ol>
                <li><b>Custom Email Server:</b> Python-based SMTP server integrated with Mailgun API.</li>
                <li><b>Discord Bot:</b> ChatGPT-integrated bot for task automation.</li>
                <li><b>WebDriver Automation:</b> Selenium-based DOM interaction and testing framework.</li>
                <li><b>Browser Extensions:</b> Tampermonkey scripts for repetitive task automation.</li>
            </ol>

            <h2>Education</h2>
            <p>Bachelor of Science in Computer Science (Placeholder University, Placeholder Year)</p>

            <h2>References</h2>
            <p>Available upon request.</p>
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
send_resume_to_grace()