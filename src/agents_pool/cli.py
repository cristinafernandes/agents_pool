import os
import sys

from agents import Runner
from dotenv import load_dotenv
from openai import AuthenticationError

from agents_pool.agent import main_agent


def main() -> None:
    load_dotenv()
    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("OPENAI_API_KEY is not set. Add it to .env or your environment.")
    try:
        result = Runner.run_sync(main_agent, " ".join(sys.argv[1:]))
    except AuthenticationError:
        sys.exit("OPENAI_API_KEY was rejected by OpenAI. Check that the key is valid.")
    print(result.final_output)
