# Claude Agent SDK Development Plugin

Complete toolkit for developing, testing, and deploying Claude Agent SDK applications.

## Features

### 🚀 Quick Setup
- **`/new-sdk-app`** - Create new Agent SDK applications (TypeScript/Python)
- Automatic dependency installation
- Pre-configured project structure
- Example code and best practices

### 🔍 Code Verification
- **`agent-sdk-verifier-ts`** - Validate TypeScript SDK applications
- **`agent-sdk-verifier-py`** - Validate Python SDK applications
- Check SDK usage patterns
- Ensure best practices
- Verify configuration

### ☁️ E2B Sandbox Deployment (NEW!)
- **`/deploy-e2b`** - Deploy agents to E2B sandboxes
- **`e2b-sandbox-manager`** - Manage E2B deployments
- Ephemeral and persistent deployment modes
- Complete TypeScript and Python examples
- Production-ready templates

## Quick Start

### Create a New Agent

```bash
/new-sdk-app my-agent
```

Follow the prompts to:
1. Choose language (TypeScript or Python)
2. Name your project
3. Select agent type
4. Pick starting point

### Verify Your Agent

The setup automatically runs verification. Or manually:

**TypeScript:**
```bash
npm run typecheck
```

**Python:**
```bash
python -m py_compile src/main.py
```

### Deploy to E2B

```bash
/deploy-e2b ephemeral
```

See [E2B Quick Start Guide](./E2B_QUICKSTART.md) for detailed deployment instructions.

## Commands

### `/new-sdk-app [project-name]`

Create a new Claude Agent SDK application.

**Interactive prompts:**
1. Language (TypeScript/Python)
2. Project name
3. Agent type/purpose
4. Starting point (minimal/feature-rich)
5. Tooling preferences

**What it creates:**
- Project structure
- Configuration files (`tsconfig.json`, `package.json`, etc.)
- Agent implementation
- Environment setup (`.env.example`)
- Example code
- Verification scripts

**Example:**
```bash
/new-sdk-app my-coding-agent
# Creates a fully configured agent project
```

### `/deploy-e2b [deployment-mode]`

Deploy your Agent SDK application to E2B sandbox.

**Deployment modes:**
- `ephemeral` - Create sandbox per request (production)
- `persistent` - Long-running sandbox (development)
- `template` - Build custom template (advanced)

**Prerequisites:**
- E2B CLI installed (`npm install -g @e2b/cli`)
- E2B API key (https://e2b.dev/dashboard)
- Anthropic API key
- E2B authentication (`e2b auth login`)

**Example:**
```bash
# Quick ephemeral deployment
/deploy-e2b ephemeral

# Or persistent for development
/deploy-e2b persistent
```

See [deploy-e2b command docs](./commands/deploy-e2b.md) for full details.

## Agents

### `agent-sdk-verifier-ts`

Validates TypeScript Agent SDK applications.

**Checks:**
- SDK installation and version
- Package configuration (`type: "module"`)
- Correct imports from `@anthropic-ai/claude-agent-sdk`
- Agent initialization patterns
- Type safety
- Error handling
- Security (no hardcoded keys)

**Usage:** Automatically invoked after `/new-sdk-app` or manually:
```bash
# Just ask Claude:
"Verify my TypeScript agent setup"
```

### `agent-sdk-verifier-py`

Validates Python Agent SDK applications.

**Checks:**
- SDK installation and version
- Correct imports from `claude_agent_sdk`
- Agent initialization patterns
- Python best practices
- Error handling
- Security (no hardcoded keys)

**Usage:** Automatically invoked after `/new-sdk-app` or manually:
```bash
# Just ask Claude:
"Verify my Python agent setup"
```

### `e2b-sandbox-manager` (NEW!)

Manages E2B sandbox deployments.

**Capabilities:**
- Deploy agents to E2B
- Monitor sandbox status
- Review logs and metrics
- Troubleshoot issues
- Optimize resource usage
- Implement best practices

**Usage:**
```bash
# Just ask Claude:
"Deploy my agent to e2b"
"Show me my e2b sandboxes"
"Check logs for sandbox xyz"
"Optimize my e2b deployment"
```

## Examples

### TypeScript Example

Complete TypeScript example with E2B deployment:

```
examples/e2b-typescript/
├── src/
│   ├── agent.ts          # Agent configuration
│   └── index.ts          # Entry point
├── deploy/
│   ├── e2b-ephemeral.ts  # Ephemeral deployment
│   └── e2b-persistent.ts # Persistent deployment
├── package.json
├── tsconfig.json
├── e2b.config.json
└── .env.example
```

**Try it:**
```bash
cd plugins/agent-sdk-dev/examples/e2b-typescript
npm install
npm run deploy:ephemeral
```

See [TypeScript example README](./examples/e2b-typescript/README.md)

### Python Example

Complete Python example with E2B deployment:

```
examples/e2b-python/
├── src/
│   ├── agent.py         # Agent configuration
│   └── main.py          # Entry point
├── deploy/
│   ├── e2b_ephemeral.py  # Ephemeral deployment
│   └── e2b_persistent.py # Persistent deployment
├── requirements.txt
├── e2b.config.json
└── .env.example
```

**Try it:**
```bash
cd plugins/agent-sdk-dev/examples/e2b-python
pip install -r requirements.txt
python deploy/e2b_ephemeral.py
```

See [Python example README](./examples/e2b-python/README.md)

## E2B Deployment Guide

### Quick Deploy

1. **Install E2B CLI:**
   ```bash
   npm install -g @e2b/cli
   ```

2. **Authenticate:**
   ```bash
   e2b auth login
   ```

3. **Set Environment Variables:**
   ```bash
   export E2B_API_KEY=your_key
   export ANTHROPIC_API_KEY=your_key
   ```

4. **Deploy:**
   ```bash
   /deploy-e2b ephemeral
   ```

### Deployment Modes

**Ephemeral (Production):**
- New sandbox per request
- Automatic cleanup
- Cost-efficient
- Maximum isolation

**Persistent (Development):**
- Long-running sandbox
- Maintains state
- Faster responses
- Higher cost

### Monitoring

```bash
# List sandboxes
e2b sandbox list

# View logs
e2b sandbox logs <sandbox-id>

# Get details
e2b sandbox get <sandbox-id>
```

### Full Documentation

See [E2B_QUICKSTART.md](./E2B_QUICKSTART.md) for comprehensive guide.

## Best Practices

### Development

1. **Start local**: Test agents locally before deploying
2. **Use verification**: Run verifier agents before deployment
3. **Check types**: Always run type checking (TypeScript)
4. **Test thoroughly**: Verify all functionality works
5. **Review logs**: Monitor agent behavior

### Deployment

1. **Use ephemeral**: For production stateless workloads
2. **Use persistent**: For development and testing
3. **Set timeouts**: Prevent runaway costs
4. **Monitor usage**: Check E2B dashboard regularly
5. **Clean up**: Remove unused sandboxes

### Security

1. **Use .env**: Never hardcode API keys
2. **Add .gitignore**: Exclude `.env` from version control
3. **Rotate keys**: Change API keys regularly
4. **Limit permissions**: Use minimal required permissions
5. **Audit logs**: Review sandbox activity

## Troubleshooting

### Agent Creation Issues

**Problem:** Type errors in TypeScript
- Run: `npm run typecheck`
- Fix all type errors
- Re-run verification

**Problem:** Import errors in Python
- Check SDK installed: `pip show claude-agent-sdk`
- Verify Python version: `python --version` (≥3.10)
- Reinstall if needed: `pip install --upgrade claude-agent-sdk`

### E2B Deployment Issues

**Problem:** "E2B CLI not found"
```bash
npm install -g @e2b/cli
```

**Problem:** "Authentication failed"
```bash
e2b auth login
```

**Problem:** "Sandbox creation timeout"
- Increase timeout in `e2b.config.json`
- Check E2B service status
- Verify network connectivity

**Problem:** "Out of memory"
- Increase memory in `e2b.config.json`
- Optimize agent code
- Review resource usage

### API Issues

**Problem:** "Invalid API key"
- Verify key in `.env`
- Check key hasn't expired
- Get new key if needed

**Problem:** "Rate limit exceeded"
- Implement retry with backoff
- Reduce request frequency
- Upgrade API tier if needed

## Resources

### Documentation
- [Claude Agent SDK Docs](https://docs.claude.com/en/api/agent-sdk)
- [E2B Documentation](https://e2b.dev/docs)
- [E2B CLI Reference](https://e2b.dev/docs/cli)

### Dashboards
- [Anthropic Console](https://console.anthropic.com/)
- [E2B Dashboard](https://e2b.dev/dashboard)

### Examples
- [TypeScript Example](./examples/e2b-typescript)
- [Python Example](./examples/e2b-python)
- [Official SDK Examples](https://github.com/anthropics/agent-sdk-examples)

### Support
- [Claude Code Issues](https://github.com/anthropics/claude-code/issues)
- [E2B Issues](https://github.com/e2b-dev/E2B/issues)
- [E2B Discord](https://discord.gg/e2b)

## Contributing

Want to improve this plugin? Here's how:

1. **Report issues**: Open issues for bugs or feature requests
2. **Submit PRs**: Contribute improvements
3. **Share examples**: Add your agent examples
4. **Improve docs**: Help make documentation better

## License

See the main Claude Code repository for license information.

---

**Get Started:** Run `/new-sdk-app` to create your first agent!

**Deploy to E2B:** See [E2B_QUICKSTART.md](./E2B_QUICKSTART.md) for deployment guide.
