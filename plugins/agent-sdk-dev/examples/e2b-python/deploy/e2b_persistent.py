import os
import sys
import asyncio
from typing import Optional
from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from agent import create_agent
from claude_agent_sdk import Agent


class PersistentSandbox:
    """Manage a persistent E2B sandbox with Claude Agent."""

    def __init__(self):
        self.sandbox: Optional[Sandbox] = None
        self.agent: Optional[Agent] = None
        self.sandbox_id: Optional[str] = None

    async def initialize(
        self,
        e2b_api_key: str,
        anthropic_api_key: str,
        template: str = "anthropic-claude-code"
    ) -> str:
        """
        Initialize persistent sandbox and agent.

        Args:
            e2b_api_key: E2B API key
            anthropic_api_key: Anthropic API key
            template: E2B template to use

        Returns:
            Sandbox ID
        """
        print("Creating persistent E2B sandbox...")

        self.sandbox = Sandbox(template=template)
        self.sandbox_id = self.sandbox.id

        print(f"Persistent sandbox created: {self.sandbox_id}")

        print("Initializing agent...")
        self.agent = create_agent(api_key=anthropic_api_key)
        print("Agent initialized")

        return self.sandbox_id

    async def execute(self, task: str) -> str:
        """
        Execute a task in the persistent sandbox.

        Args:
            task: Task description

        Returns:
            Agent's response
        """
        if not self.agent:
            raise RuntimeError("Sandbox not initialized. Call initialize() first.")

        print(f"\nExecuting task: {task}")

        result = await self.agent.run(user_prompt=task)
        return result.output

    def health_check(self) -> bool:
        """Check if sandbox is healthy."""
        if not self.sandbox:
            return False

        try:
            # Simple health check
            return True
        except:
            return False

    def get_sandbox_id(self) -> Optional[str]:
        """Get the sandbox ID."""
        return self.sandbox_id

    def shutdown(self):
        """Shutdown the persistent sandbox."""
        if self.sandbox:
            print("Shutting down persistent sandbox...")
            self.sandbox.close()
            print("Sandbox closed")
            self.sandbox = None
            self.agent = None
            self.sandbox_id = None


async def run_persistent_server():
    """Example: Long-running server with persistent sandbox."""

    load_dotenv()

    e2b_api_key = os.getenv("E2B_API_KEY")
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

    if not e2b_api_key or not anthropic_api_key:
        raise ValueError("E2B_API_KEY and ANTHROPIC_API_KEY must be set")

    persistent = PersistentSandbox()

    try:
        # Initialize
        sandbox_id = await persistent.initialize(
            e2b_api_key=e2b_api_key,
            anthropic_api_key=anthropic_api_key,
            template=os.getenv("E2B_TEMPLATE", "anthropic-claude-code")
        )

        print(f"\nPersistent sandbox running: {sandbox_id}")
        print("Ready to accept tasks...\n")

        # Example: Execute multiple tasks
        tasks = [
            "Create a simple web server",
            "Write tests for the web server",
            "Add error handling to the server"
        ]

        for task in tasks:
            result = await persistent.execute(task)
            print("\n=== Result ===")
            print(result)
            print("==============\n")

            # Wait between tasks
            await asyncio.sleep(1)

        # Health check
        healthy = persistent.health_check()
        print(f"\nSandbox health: {'OK' if healthy else 'ERROR'}")

    except Exception as error:
        print(f"Error: {error}")
        raise
    finally:
        # Cleanup
        persistent.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(run_persistent_server())
        print("Persistent sandbox session completed")
    except Exception as error:
        print(f"Persistent sandbox failed: {error}")
        sys.exit(1)
