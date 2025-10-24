import os
import sys
import asyncio
from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from agent import create_agent, run_agent


async def deploy_ephemeral(
    e2b_api_key: str,
    anthropic_api_key: str,
    task: str,
    template: str = "anthropic-claude-code",
    timeout: int = 300000
) -> str:
    """
    Deploy agent in ephemeral E2B sandbox.

    Args:
        e2b_api_key: E2B API key
        anthropic_api_key: Anthropic API key
        task: Task for the agent to perform
        template: E2B template to use
        timeout: Sandbox timeout in milliseconds

    Returns:
        Agent's response
    """

    print("Creating E2B sandbox (ephemeral mode)...")

    sandbox = Sandbox(template=template)

    try:
        print(f"Sandbox created: {sandbox.id}")
        print("Initializing agent in sandbox...")

        # Create agent
        agent = create_agent(api_key=anthropic_api_key)

        print("Running task...")
        result = await run_agent(agent, task)

        print("\n=== Agent Response ===")
        print(result)
        print("===================\n")

        return result

    except Exception as error:
        print(f"Deployment error: {error}")
        raise
    finally:
        print("Cleaning up sandbox...")
        sandbox.close()
        print("Sandbox closed")


async def main():
    """CLI handler for ephemeral deployment."""

    load_dotenv()

    e2b_api_key = os.getenv("E2B_API_KEY")
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

    if not e2b_api_key or not anthropic_api_key:
        print("Error: E2B_API_KEY and ANTHROPIC_API_KEY must be set")
        sys.exit(1)

    task = sys.argv[1] if len(sys.argv) > 1 else "Write a simple Python hello world script"
    template = os.getenv("E2B_TEMPLATE", "anthropic-claude-code")
    timeout = int(os.getenv("E2B_TIMEOUT", "300000"))

    try:
        await deploy_ephemeral(
            e2b_api_key=e2b_api_key,
            anthropic_api_key=anthropic_api_key,
            task=task,
            template=template,
            timeout=timeout
        )
        print("Deployment completed successfully")
    except Exception as error:
        print(f"Deployment failed: {error}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
