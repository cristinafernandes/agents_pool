# agents_pool

An agent built on the OpenAI Agents SDK. It picks one of three tools to handle a prompt: run a Python script, send an email or summarise text.

## Setup

```
uv sync
cp .env.example .env   # fill in OPENAI_API_KEY and SMTP settings
```

## Usage

```
uv run agents-pool "Run the script at ./hello.py"
uv run agents-pool "Email bob@example.com saying the build passed"
uv run agents-pool "Summarise this: ..."
```

## Tests

```
uv run pytest
```

Without `OPENAI_API_KEY`, the tool-selection tests that call the live model are skipped.
