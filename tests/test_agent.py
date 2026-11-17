from agents_pool.agent import main_agent

TOOL_NAMES = {"run_python_script", "send_email", "summarise_text"}


def test_main_agent_has_three_tools():
    assert {tool.name for tool in main_agent.tools} == TOOL_NAMES
    assert len(main_agent.tools) == 3


def test_tool_use_is_required():
    assert main_agent.model_settings.tool_choice == "required"
    assert main_agent.reset_tool_choice


def test_instructions_mention_each_tool():
    for name in TOOL_NAMES:
        assert name in main_agent.instructions
