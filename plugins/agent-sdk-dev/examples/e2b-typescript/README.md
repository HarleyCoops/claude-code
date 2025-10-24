# E2B Claude Agent SDK - TypeScript Example

Complete example of deploying a Claude Agent SDK application to E2B sandboxes.

## Quick Start

```bash
# Install dependencies
npm install

# Set environment variables
cp .env.example .env
# Edit .env with your API keys

# Run locally
npm start

# Deploy to E2B (ephemeral)
npm run deploy:ephemeral

# Deploy to E2B (persistent)
npm run deploy:persistent

# Build E2B template
npm run e2b:build-template
```

## Project Structure

```
.
├── src/
│   ├── agent.ts           # Main agent configuration
│   ├── index.ts           # Local entry point
│   └── tools/             # Custom tools (optional)
├── deploy/
│   ├── e2b-ephemeral.ts   # Ephemeral deployment
│   ├── e2b-persistent.ts  # Persistent deployment
│   └── e2b-template.ts    # Template builder
├── e2b.config.json        # E2B configuration
├── .e2b/
│   └── Dockerfile         # Custom template (optional)
├── package.json
├── tsconfig.json
└── .env.example
```

## Deployment Modes

### Ephemeral (Recommended for Production)
- New sandbox per request
- Automatic cleanup
- Maximum isolation
- Cost-efficient

```bash
npm run deploy:ephemeral
```

### Persistent (For Development)
- Long-running sandbox
- Maintains state
- Faster response times
- Higher cost

```bash
npm run deploy:persistent
```

### Custom Template (Advanced)
- Pre-built environment
- Fastest startup
- Reusable across deployments

```bash
npm run e2b:build-template
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
  "buildCommand": "npm install && npm run build",
  "startCommand": "node dist/index.js",
  "env": {
    "ANTHROPIC_API_KEY": "$ANTHROPIC_API_KEY",
    "NODE_ENV": "production"
  },
  "timeout": 300000,
  "memory": 2048
}
```

## Monitoring

```bash
# List sandboxes
npx e2b sandbox list

# View logs
npx e2b sandbox logs <sandbox-id>

# Get sandbox details
npx e2b sandbox get <sandbox-id>

# Stop sandbox
npx e2b sandbox stop <sandbox-id>
```

## Customization

### Add Custom Tools

Edit `src/agent.ts` to add MCP servers or custom tools:

```typescript
const agent = new Agent({
  // ... other config
  mcpServers: {
    myTool: {
      command: 'node',
      args: ['path/to/mcp-server.js']
    }
  }
})
```

### Modify System Prompt

Edit the system prompt in `src/agent.ts`:

```typescript
systemPrompt: `Your custom instructions here`
```

### Add Subagents

Create specialized subagents for different tasks:

```typescript
const subAgent = agent.createSubagent({
  name: 'specialized-task',
  systemPrompt: 'Specialized instructions'
})
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
6. **Use templates** for consistent deployments
7. **Enable logging** for debugging
8. **Implement health checks**

## Resources

- [E2B Documentation](https://e2b.dev/docs)
- [Claude Agent SDK Docs](https://docs.claude.com/en/api/agent-sdk)
- [E2B Dashboard](https://e2b.dev/dashboard)
- [Example Agents](https://github.com/anthropics/agent-sdk-examples)
