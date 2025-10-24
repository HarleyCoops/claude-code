import os
import sys
import asyncio
from dotenv import load_dotenv
from agent import create_agent, run_agent


async def main():
    """Main entry point for local agent execution."""

    # Load environment variables
    load_dotenv()

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    print("Initializing Claude Agent...")
    agent = create_agent(api_key=api_key)

    # Get task from command line or use default
    task = sys.argv[1] if len(sys.argv) > 1 else "Hello! Can you help me understand how you work?"

    print(f"\nTask: {task}\n")
    print("Agent response:")
    print("---")

    response = await run_agent(agent, task)
    print(response)
    print("---")


if __name__ == "__main__":
    asyncio.run(main())
