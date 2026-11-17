# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Agents Pool Project

## Requirements

- An agent with 3 different tools: run a python script, send an email, summarise a text
- When prompted, the agent should pick the correct tool

## Technical Details

- Use the OpenAI Agents SDK (`openai-agents` package)
- Use uv for project and dependency management (`uv init`, `uv add`, `uv run`, `uv sync`); do not use pip or manual venvs

## Commands

- `uv sync` - install dependencies
- `uv run pytest` - run all tests (the live-model tests in `tests/test_tool_selection.py` are skipped without `OPENAI_API_KEY`)
- `uv run pytest tests/test_tools.py::test_send_email` - run a single test
- `uv run agents-pool "prompt"` - run the agent once (loads `.env`)

## Architecture

- `src/agents_pool/tools.py`: `run_python_script` and `send_email` are plain functions (unit-tested directly) wrapped with `function_tool`. Email uses `smtplib` with STARTTLS; config comes from the SMTP env vars in `.env.example`.
- `src/agents_pool/agent.py`: `main_agent` holds three tools. Summarising is done by a separate `summariser_agent`, exposed with `as_tool("summarise_text")`.
- `src/agents_pool/cli.py`: the one-shot entry point, which uses `Runner.run_sync`.
- Tool-selection tests read the tools that were called from `result.new_items` (`ToolCallItem.raw_item.name`) and mock SMTP.

## Strategy

1. Ask questions about any doubt you may have.
2. Write plan with success criteria for each phase to be checked off. Include project scaffolding, including .gitignore, and rigorous unit testing.
3. Ask for approval on the plan.
4. Execute the plan ensuring all criteria are met.

## Coding standards

1. Use latest stable versions of libraries and idiomatic approaches as of today
2. Keep it simple - NEVER over-engineer, ALWAYS simplify, NO unnecessary defensive programming. No extra features - focus on simplicity.
3. Be concise. Keep README minimal. IMPORTANT: no emojis ever
4. When hitting issues, always identify root cause before trying a fix. Prove with evidence, then fix the root cause.
