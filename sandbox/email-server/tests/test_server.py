import pytest
import pytest_asyncio
import asyncio
from server import EmailHandler
from aiosmtpd.controller import Controller

@pytest_asyncio.fixture
async def smtp_server():
    handler = EmailHandler()
    controller = Controller(handler, hostname='127.0.0.1', port=8025)
    controller.start()
    await asyncio.sleep(1)  # Ensure the server is ready
    yield controller
    controller.stop()

@pytest.mark.asyncio
async def test_email_reception(smtp_server):
    # Simulate sending an email
    reader, writer = await asyncio.open_connection('127.0.0.1', 8025)

    writer.write(b"HELO test.com\r\n")
    await writer.drain()
    response = await reader.read(1024)
    assert b"250" in response

    writer.write(b"MAIL FROM:<sender@test.com>\r\n")
    await writer.drain()
    response = await reader.read(1024)
    assert b"250" in response

    writer.write(b"RCPT TO:<receiver@test.com>\r\n")
    await writer.drain()
    response = await reader.read(1024)
    assert b"250" in response

    writer.write(b"DATA\r\n")
    await writer.drain()
    response = await reader.read(1024)
    assert b"354" in response

    writer.write(b"Subject: Test\r\n\r\nThis is a test email.\r\n.\r\n")
    await writer.drain()
    response = await reader.read(1024)
    assert b"250" in response

    writer.close()
    await writer.wait_closed()

    # Verify email saved to file
    with open("/sandbox/email-server/emails/received_email.txt", "r") as f:
        content = f.read()
        assert "receiver@test.com" in content
        assert "sender@test.com" in content
        assert "This is a test email." in content