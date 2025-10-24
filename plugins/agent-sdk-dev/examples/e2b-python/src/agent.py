from typing import Optional
from claude_agent_sdk import Agent


def create_agent(
    api_key: str,
    system_prompt: Optional[str] = None,
    model: str = "claude-sonnet-4-5-20250929"
) -> Agent:
    """
    Create a Claude Agent configured for E2B sandbox deployment.

    Args:
        api_key: Anthropic API key
        system_prompt: Custom system prompt for the agent
        model: Claude model to use

    Returns:
        Configured Agent instance
    """

    if system_prompt is None:
        system_prompt = "You are a helpful AI assistant running in a secure E2B sandbox."

    agent = Agent(
        api_key=api_key,
        model=model,
        system_prompt=system_prompt,

        # Configure permissions for sandbox environment
        permissions={
            "bash": True,
            "read": True,
            "write": True,
            "edit": True,
            "web": False  # Disable external web access by default
        },

        # Optional: Add MCP servers for custom tools
        # mcp_servers={
        #     "filesystem": {
        #         "command": "python",
        #         "args": ["mcp_server_filesystem.py"]
        #     }
        # },

        # Optional: Enable streaming
        # streaming=True,

        # Optional: Add custom context
        # additional_context="Running in E2B sandbox environment"
    )

    return agent


async def run_agent(agent: Agent, task: str) -> str:
    """
    Run the agent with a given task.

    Args:
        agent: Configured Agent instance
        task: Task description for the agent

    Returns:
        Agent's response as string
    """
    try:
        result = await agent.run(user_prompt=task)
        return result.output
    except Exception as error:
        print(f"Agent execution error: {error}")
        raise
