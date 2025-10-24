# E2B Claude Agent SDK - Python Example

Complete example of deploying a Claude Agent SDK application to E2B sandboxes using Python.

## Quick Start

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your API keys

# Run locally
python src/main.py

# Deploy to E2B (ephemeral)
python deploy/e2b_ephemeral.py

# Deploy to E2B (persistent)
python deploy/e2b_persistent.py
```

## Project Structure

```
.
├── src/
│   ├── agent.py           # Main agent configuration
│   ├── main.py            # Local entry point
│   └── tools/             # Custom tools (optional)
├── deploy/
│   ├── e2b_ephemeral.py   # Ephemeral deployment
│   └── e2b_persistent.py  # Persistent deployment
├── e2b.config.json        # E2B configuration
├── requirements.txt
└── .env.example
```

## Deployment Modes

### Ephemeral (Recommended for Production)
- New sandbox per request
- Automatic cleanup
- Maximum isolation
- Cost-efficient

```bash
python deploy/e2b_ephemeral.py "Your task here"
```

### Persistent (For Development)
- Long-running sandbox
- Maintains state
- Faster response times
- Higher cost

```bash
python deploy/e2b_persistent.py
```

## Configuration

### Environment Variables

Required:
- `E2B_API_KEY` - From https://e2b.dev/dashboard
- `ANTHROPIC_API_KEY` - From https://console.anthropic.com/

Optional:
- `E2B_TEMPLATE` - Custom template ID
- `E2B_TIMEOUT` - Sandbox timeout (ms)
- `E2B_MEMORY` - Memory allocation (MB)

### e2b.config.json

```json
{
  "template": "anthropic-claude-code",
  "buildCommand": "pip install -r requirements.txt",
  "startCommand": "python src/main.py",
  "env": {
    "ANTHROPIC_API_KEY": "$ANTHROPIC_API_KEY",
    "PYTHON_ENV": "production"
  },
  "timeout": 300000,
  "memory": 2048
}
```

## Monitoring

```bash
# List sandboxes
e2b sandbox list

# View logs
e2b sandbox logs <sandbox-id>

# Get sandbox details
e2b sandbox get <sandbox-id>

# Stop sandbox
e2b sandbox stop <sandbox-id>
```

## Customization

### Add Custom Tools

Edit `src/agent.py` to add MCP servers or custom tools:

```python
agent = Agent(
    # ... other config
    mcp_servers={
        "my_tool": {
            "command": "python",
            "args": ["path/to/mcp_server.py"]
        }
    }
)
```

### Modify System Prompt

Edit the system prompt in `src/agent.py`:

```python
system_prompt = "Your custom instructions here"
```

### Add Subagents

Create specialized subagents for different tasks:

```python
sub_agent = agent.create_subagent(
    name="specialized-task",
    system_prompt="Specialized instructions"
)
```

## Troubleshooting

### Sandbox Creation Fails
- Verify E2B_API_KEY is set
- Check E2B service status
- Review build command output

### Agent Initialization Errors
- Verify ANTHROPIC_API_KEY is valid
- Check SDK version compatibility
- Review agent configuration

### Timeout Issues
- Increase timeout in e2b.config.json
- Optimize agent code
- Use persistent mode for long tasks

### Memory Errors
- Increase memory allocation
- Optimize data processing
- Review resource usage in dashboard

## Production Best Practices

1. **Use ephemeral mode** for stateless tasks
2. **Set appropriate timeouts** to prevent runaway costs
3. **Implement retry logic** for transient failures
4. **Monitor sandbox usage** via E2B dashboard
5. **Clean up unused sandboxes** regularly
6. **Enable logging** for debugging
7. **Implement health checks**
8. **Use virtual environments** for dependency isolation

## Resources

- [E2B Documentation](https://e2b.dev/docs)
- [Claude Agent SDK Docs](https://docs.claude.com/en/api/agent-sdk)
- [E2B Dashboard](https://e2b.dev/dashboard)
- [Python Guide for E2B](https://e2b.dev/blog/python-guide-run-claude-code-in-an-e2b-sandbox)
