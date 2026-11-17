import subprocess
from unittest.mock import patch

from agents_pool import tools


def test_run_python_script_success(tmp_path):
    script = tmp_path / "ok.py"
    script.write_text("print('hello')")

    output = tools.run_python_script(str(script))

    assert "exit code: 0" in output
    assert "hello" in output


def test_run_python_script_failure(tmp_path):
    script = tmp_path / "fail.py"
    script.write_text("import sys\nsys.stderr.write('boom')\nsys.exit(3)")

    output = tools.run_python_script(str(script))

    assert "exit code: 3" in output
    assert "boom" in output


def test_run_python_script_missing_file(tmp_path):
    output = tools.run_python_script(str(tmp_path / "missing.py"))

    assert "exit code: 2" in output
    assert "No such file or directory" in output


def test_run_python_script_timeout(tmp_path):
    script = tmp_path / "slow.py"
    script.write_text("")

    with patch.object(
        tools.subprocess, "run", side_effect=subprocess.TimeoutExpired("python", 60)
    ):
        output = tools.run_python_script(str(script))

    assert output == "Script timed out after 60 seconds."


def test_send_email(monkeypatch):
    monkeypatch.setenv("SMTP_HOST", "smtp.example.com")
    monkeypatch.setenv("SMTP_PORT", "587")
    monkeypatch.setenv("SMTP_USERNAME", "user")
    monkeypatch.setenv("SMTP_PASSWORD", "secret")
    monkeypatch.setenv("EMAIL_FROM", "me@example.com")

    with patch.object(tools.smtplib, "SMTP") as smtp_cls:
        output = tools.send_email("bob@example.com", "Hi", "Hello Bob")

    smtp_cls.assert_called_once_with("smtp.example.com", 587)
    smtp = smtp_cls.return_value.__enter__.return_value
    smtp.starttls.assert_called_once()
    smtp.login.assert_called_once_with("user", "secret")
    message = smtp.send_message.call_args.args[0]
    assert message["From"] == "me@example.com"
    assert message["To"] == "bob@example.com"
    assert message["Subject"] == "Hi"
    assert message.get_content().strip() == "Hello Bob"
    assert output == "Email sent to bob@example.com."


def test_tools_are_function_tools():
    assert tools.run_python_script_tool.name == "run_python_script"
    assert tools.send_email_tool.name == "send_email"
    assert "path" in tools.run_python_script_tool.params_json_schema["properties"]
    assert set(tools.send_email_tool.params_json_schema["properties"]) == {
        "to",
        "subject",
        "body",
    }
