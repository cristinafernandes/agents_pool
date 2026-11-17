# Plan

One agent (OpenAI Agents SDK) with three tools: run a Python script, send an email over SMTP, summarise a text. The agent decides which tool fits the prompt.

## Decisions

- Python 3.13, uv, `openai-agents` (latest, currently 0.24.0), `python-dotenv`, `pytest` (dev).
- Run script: runs an existing `.py` file by path with `subprocess`, using the current interpreter and a 60s timeout. Returns the exit code, stdout and stderr.
- Send email: stdlib `smtplib` with STARTTLS. Reads `SMTP_HOST`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD` and `EMAIL_FROM` from `.env`.
- Summarise: a dedicated summariser `Agent`, exposed to the main agent through `as_tool()`.
- Interface: one-shot CLI, `uv run agents-pool "prompt"`, prints the final output.
- Model: the SDK default, with no override.

## Layout

```
pyproject.toml
.python-version
.gitignore
.env.example
README.md
src/agents_pool/
  __init__.py
  tools.py      # run_python_script, send_email (plain functions + function_tool wrappers)
  agent.py      # summariser agent, main agent
  cli.py        # entry point
tests/
  test_tools.py
  test_agent.py
  test_tool_selection.py   # live model, skipped without OPENAI_API_KEY
```

## Phase 1: Scaffolding

- [x] `uv init --package` project, `.python-version` set to 3.13
- [x] Dependencies added with `uv add openai-agents python-dotenv` and `uv add --dev pytest`
- [x] `.gitignore` covers `.venv/`, `__pycache__/`, `.pytest_cache/` and `.env`
- [x] `.env.example` lists `OPENAI_API_KEY` and the SMTP variables
- [x] `uv sync` succeeds and `uv run pytest` runs (no tests yet)

## Phase 2: Tools

- [x] `run_python_script(path)` returns the exit code, stdout and stderr
- [x] `send_email(to, subject, body)` sends over SMTP with STARTTLS and login, then returns a confirmation
- [x] Each function is wrapped with `function_tool` and has a docstring the model can read
- [x] Unit tests pass:
  - a successful script returns its stdout and exit code 0
  - a failing script returns its stderr and a non-zero exit code
  - a script that times out returns a timeout message
  - a missing file returns an error message
  - for email, `smtplib.SMTP` is mocked and the test asserts the host and port, the STARTTLS and login calls, and the From, To, Subject and Body of the sent message

## Phase 3: Agent and CLI

- [x] A summariser agent is exposed as the tool `summarise_text`
- [x] The main agent has exactly three tools, `run_python_script`, `send_email` and `summarise_text`, plus instructions on when to use each
- [x] `agents-pool "prompt"` loads `.env`, runs `Runner.run_sync` and prints `final_output`
- [x] Unit tests pass: the tool names are correct and the main agent's instructions mention each tool

## Phase 4: Tool selection (live)

- [x] Integration tests call the real model, with SMTP mocked so no real mail is sent. Each test asserts the tool that was called, read from `result.new_items`:
  - "Run the script at <tmp>/hello.py" calls `run_python_script`
  - "Email bob@example.com saying the build passed" calls `send_email`
  - "Summarise this: <paragraph>" calls `summarise_text`
- [x] All of these tests pass when `OPENAI_API_KEY` is set, and they are skipped otherwise

## Phase 5: Docs

- [x] A minimal README covers setup, configuration and usage
- [x] `CLAUDE.md` is updated with the commands (sync, test, run a single test, run the CLI) and a short architecture note
- [x] Every test passes with `uv run pytest`
