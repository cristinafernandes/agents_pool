import os
import smtplib
import subprocess
import sys
from email.message import EmailMessage

from agents import function_tool

SCRIPT_TIMEOUT_SECONDS = 60


def run_python_script(path: str) -> str:
    """Run an existing Python script file and return its exit code, stdout and stderr.

    Args:
        path: Path to the .py file to run.
    """
    try:
        result = subprocess.run(
            [sys.executable, path],
            capture_output=True,
            text=True,
            timeout=SCRIPT_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return f"Script timed out after {SCRIPT_TIMEOUT_SECONDS} seconds."
    return f"exit code: {result.returncode}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"


def send_email(to: str, subject: str, body: str) -> str:
    """Send a plain-text email.

    Args:
        to: Recipient email address.
        subject: Email subject line.
        body: Email body text.
    """
    message = EmailMessage()
    message["From"] = os.environ["EMAIL_FROM"]
    message["To"] = to
    message["Subject"] = subject
    message.set_content(body)

    with smtplib.SMTP(os.environ["SMTP_HOST"], int(os.environ["SMTP_PORT"])) as smtp:
        smtp.starttls()
        smtp.login(os.environ["SMTP_USERNAME"], os.environ["SMTP_PASSWORD"])
        smtp.send_message(message)
    return f"Email sent to {to}."


run_python_script_tool = function_tool(run_python_script)
send_email_tool = function_tool(send_email)
