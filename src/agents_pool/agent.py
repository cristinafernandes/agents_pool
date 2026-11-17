from agents import Agent, ModelSettings

from agents_pool.tools import run_python_script_tool, send_email_tool

summariser_agent = Agent(
    name="Summariser",
    instructions="Summarise the given text concisely, keeping the key points.",
)

main_agent = Agent(
    name="Assistant",
    instructions=(
        "You help the user by choosing the right tool:\n"
        "- run_python_script: run an existing Python script file by its path.\n"
        "- send_email: send an email to a recipient with a subject and body.\n"
        "- summarise_text: summarise a piece of text.\n"
        "Pick the tool that matches the request, then report the result."
    ),
    model_settings=ModelSettings(tool_choice="required"),
    tools=[
        run_python_script_tool,
        send_email_tool,
        summariser_agent.as_tool(
            tool_name="summarise_text",
            tool_description="Summarise a piece of text.",
        ),
    ],
)
