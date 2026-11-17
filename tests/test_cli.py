from unittest.mock import patch

import httpx2
import pytest
from openai import AuthenticationError

from agents_pool import cli


@pytest.fixture(autouse=True)
def no_dotenv(monkeypatch):
    monkeypatch.setattr(cli, "load_dotenv", lambda: None)
    monkeypatch.setattr(cli.sys, "argv", ["agents-pool", "hello"])


def test_missing_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(SystemExit) as exc:
        cli.main()

    assert str(exc.value) == "OPENAI_API_KEY is not set. Add it to .env or your environment."


def test_rejected_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-invalid")
    request = httpx2.Request("POST", "https://api.openai.com/v1/responses")
    error = AuthenticationError(
        "Incorrect API key", response=httpx2.Response(401, request=request), body=None
    )

    with patch.object(cli.Runner, "run_sync", side_effect=error):
        with pytest.raises(SystemExit) as exc:
            cli.main()

    assert str(exc.value) == "OPENAI_API_KEY was rejected by OpenAI. Check that the key is valid."
