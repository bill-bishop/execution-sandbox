import pytest
from unittest.mock import patch, MagicMock
from src.send_email import send_email

def test_send_email():
    with patch("smtplib.SMTP", autospec=True) as mock_smtp:
        # Create mock server instance
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        # Call the send_email function
        send_email(
            sender="sender@test.com",
            recipient="receiver@test.com",
            subject="Test Subject",
            body="This is a test email.",
            smtp_server="smtp.test.com",
            smtp_port=587,
            username="test_user",
            password="test_password"
        )

        # Verify SMTP lifecycle and interactions
        mock_smtp.assert_called_once_with("smtp.test.com", 587)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with("test_user", "test_password")
        mock_server.sendmail.assert_called_once_with(
            "sender@test.com",
            ["receiver@test.com"],
            """Content-Type: text/plain; charset=\"us-ascii\"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Test Subject
From: sender@test.com
To: receiver@test.com

This is a test email."""
        )