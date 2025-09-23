const nodemailer = require("nodemailer");

(async () => {
  try {
    const transporter = nodemailer.createTransport({
      host: "smtp.gmail.com",
      port: 587,
      secure: false,
      auth: {
        user: process.env.GMAIL_USER,
        pass: process.env.GMAIL_APP_PASSWORD,
      },
    });

    const info = await transporter.sendMail({
      from: process.env.GMAIL_USER,
      to: "recipient@example.com",
      subject: "CLI test",
      text: "Hello from CLI!",
      html: "<b>Hello</b> from <i>CLI</i>!",
      // Uncomment and update if you want to attach a file
      // attachments: [{ path: "/path/to/file.pdf" }],
    });

    console.log("Sent:", info.messageId);
  } catch (err) {
    console.error("Error sending mail:", err);
  }
})();