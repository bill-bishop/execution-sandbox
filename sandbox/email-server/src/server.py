import asyncio
import os
from aiosmtpd.controller import Controller

class EmailHandler:
    async def handle_DATA(self, server, session, envelope):
        os.makedirs("./emails", exist_ok=True)
        with open("./emails/received_email.txt", "a") as f:
            f.write(f"To: {', '.join(envelope.rcpt_tos)}\n")
            f.write(f"From: {envelope.mail_from}\n")
            f.write(f"Content:\n{envelope.content.decode('utf-8', errors='replace')}\n\n")
        return '250 OK'

if __name__ == '__main__':
    handler = EmailHandler()
    controller = Controller(handler, hostname='0.0.0.0', port=8025)  # Port 8025 for SMTP
    controller.start()
    print("SMTP server running on port 8025. Press Ctrl+C to stop.")
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        controller.stop()