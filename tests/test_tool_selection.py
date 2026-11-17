import os
from unittest.mock import patch

import pytest
from agents import Runner
from agents.items import ToolCallItem

from agents_pool import tools
from agents_pool.agent import main_agent

pytestmark = pytest.mark.skipif(
    not os.environ.get("OPENAI_API_KEY"), reason="OPENAI_API_KEY not set"
)


def called_tools(prompt: str) -> list[str]:
    result = Runner.run_sync(main_agent, prompt)
    return [item.raw_item.name for item in result.new_items if isinstance(item, ToolCallItem)]


def test_picks_run_python_script(tmp_path):
    script = tmp_path / "hello.py"
    script.write_text("print('hello')")

    assert called_tools(f"Run the script at {script}") == ["run_python_script"]


def test_picks_send_email(monkeypatch):
    for name, value in {
        "SMTP_HOST": "smtp.example.com",
        "SMTP_PORT": "587",
        "SMTP_USERNAME": "user",
        "SMTP_PASSWORD": "secret",
        "EMAIL_FROM": "me@example.com",
    }.items():
        monkeypatch.setenv(name, value)

    with patch.object(tools.smtplib, "SMTP") as smtp_cls:
        names = called_tools("Email bob@example.com saying the build passed")

    assert names == ["send_email"]
    smtp_cls.return_value.__enter__.return_value.send_message.assert_called_once()


def test_picks_summarise_text():
    text = (
        "The city council met on Tuesday to discuss the new transport plan. "
        "After three hours of debate, members agreed to expand bus routes, add "
        "protected bike lanes on four major streets, and review parking fees "
        "next spring. Funding will come from a mix of state grants and local taxes."
    )

    assert called_tools(f"Summarise this: {text}") == ["summarise_text"]
