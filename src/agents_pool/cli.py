import sys

from agents import Runner
from dotenv import load_dotenv

from agents_pool.agent import main_agent


def main() -> None:
    load_dotenv()
    result = Runner.run_sync(main_agent, " ".join(sys.argv[1:]))
    print(result.final_output)
