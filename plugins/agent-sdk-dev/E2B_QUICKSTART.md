# E2B Sandbox Deployment - Quick Start Guide

Deploy your Claude Agent SDK applications to secure E2B sandboxes in minutes.

## What is E2B?

E2B provides isolated cloud sandboxes specifically designed for running AI agents securely. Perfect for:
- Production agent deployments
- Isolated execution environments
- Scalable AI applications
- Secure code execution

## Prerequisites

### 1. Install E2B CLI

```bash
npm install -g @e2b/cli
```

### 2. Get API Keys

1. **E2B API Key**: Sign up at https://e2b.dev/dashboard
2. **Anthropic API Key**: Get from https://console.anthropic.com/

### 3. Authenticate with E2B

```bash
e2b auth login
# Or set directly:
e2b auth set-key YOUR_E2B_API_KEY
```

## Quick Deploy

### Option 1: Use Example Templates (Fastest)

**TypeScript:**
```bash
# Navigate to example
cd plugins/agent-sdk-dev/examples/e2b-typescript

# Install dependencies
npm install

# Set environment variables
cp .env.example .env
# Edit .env with your keys

# Deploy ephemeral
npm run deploy:ephemeral

# Or deploy persistent
npm run deploy:persistent
```

**Python:**
```bash
# Navigate to example
cd plugins/agent-sdk-dev/examples/e2b-python

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your keys

# Deploy ephemeral
python deploy/e2b_ephemeral.py "Your task here"

# Or deploy persistent
python deploy/e2b_persistent.py
```

### Option 2: Use Claude Code Commands

```bash
# Create new SDK app with e2b support
/new-sdk-app my-e2b-agent

# Deploy to e2b
/deploy-e2b ephemeral

# Or use the e2b sandbox manager agent
# Just ask: "Deploy my agent to e2b in ephemeral mode"
```

## Deployment Modes Explained

### Ephemeral Mode (Production)

**Best for:** Stateless tasks, production deployments

**Characteristics:**
- Creates new sandbox per request
- Automatically cleans up after completion
- Maximum isolation and security
- Cost-efficient for sporadic workloads

**Use when:**
- Processing independent user requests
- Running one-off tasks
- Need guaranteed clean state
- Want automatic resource cleanup

**Example:**
```typescript
// TypeScript
import { deployEphemeral } from './deploy/e2b-ephemeral.js'

const result = await deployEphemeral({
  e2bApiKey: process.env.E2B_API_KEY,
  anthropicApiKey: process.env.ANTHROPIC_API_KEY
}, 'Create a web app')
```

```python
# Python
from deploy.e2b_ephemeral import deploy_ephemeral

result = await deploy_ephemeral(
    e2b_api_key=os.getenv("E2B_API_KEY"),
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
    task="Create a web app"
)
```

### Persistent Mode (Development)

**Best for:** Development, testing, stateful workflows

**Characteristics:**
- Long-running sandbox instance
- Maintains state between requests
- Faster response times (no cold start)
- Higher cost for continuous operation

**Use when:**
- Developing and testing agents
- Need to maintain state
- Want faster subsequent requests
- Building conversational flows

**Example:**
```typescript
// TypeScript
import { PersistentSandbox } from './deploy/e2b-persistent.js'

const sandbox = new PersistentSandbox()
await sandbox.initialize(apiKey, anthropicKey)

// Execute multiple tasks
await sandbox.execute('Task 1')
await sandbox.execute('Task 2')

await sandbox.shutdown()
```

```python
# Python
from deploy.e2b_persistent import PersistentSandbox

sandbox = PersistentSandbox()
await sandbox.initialize(e2b_api_key, anthropic_api_key)

# Execute multiple tasks
await sandbox.execute("Task 1")
await sandbox.execute("Task 2")

sandbox.shutdown()
```

## Configuration

### Environment Variables

Create `.env` file:

```bash
# Required
E2B_API_KEY=your_e2b_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# Optional
E2B_TEMPLATE=anthropic-claude-code
E2B_TIMEOUT=300000
E2B_MEMORY=2048
```

### E2B Config File

Create `e2b.config.json`:

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
  "memory": 2048,
  "cpu": 2
}
```

## Monitoring Your Deployments

### List Active Sandboxes

```bash
e2b sandbox list
```

### View Sandbox Logs

```bash
e2b sandbox logs <sandbox-id>
```

### Get Sandbox Details

```bash
e2b sandbox get <sandbox-id>
```

### Stop Sandbox

```bash
e2b sandbox stop <sandbox-id>
```

### Delete Sandbox

```bash
e2b sandbox delete <sandbox-id>
```

## Common Use Cases

### 1. Web API with E2B Backend

```typescript
import express from 'express'
import { deployEphemeral } from './deploy/e2b-ephemeral.js'

const app = express()

app.post('/run-agent', async (req, res) => {
  const { task } = req.body

  const result = await deployEphemeral({
    e2bApiKey: process.env.E2B_API_KEY,
    anthropicApiKey: process.env.ANTHROPIC_API_KEY
  }, task)

  res.json({ result })
})

app.listen(3000)
```

### 2. Batch Processing

```python
import asyncio
from deploy.e2b_ephemeral import deploy_ephemeral

async def process_batch(tasks):
    results = await asyncio.gather(*[
        deploy_ephemeral(
            e2b_api_key=E2B_KEY,
            anthropic_api_key=ANTHROPIC_KEY,
            task=task
        )
        for task in tasks
    ])
    return results

tasks = ["Task 1", "Task 2", "Task 3"]
results = asyncio.run(process_batch(tasks))
```

### 3. Interactive Development

```typescript
const sandbox = new PersistentSandbox()
await sandbox.initialize(e2bKey, anthropicKey)

// Interactive REPL
while (true) {
  const task = await getUserInput()
  if (task === 'exit') break

  const result = await sandbox.execute(task)
  console.log(result)
}

await sandbox.shutdown()
```

## Troubleshooting

### "E2B CLI not found"

```bash
npm install -g @e2b/cli
e2b --version
```

### "Authentication failed"

```bash
e2b auth login
# Or
e2b auth set-key YOUR_API_KEY
```

### "Sandbox creation timeout"

Increase timeout in `e2b.config.json`:
```json
{
  "timeout": 600000  // 10 minutes
}
```

### "Out of memory"

Increase memory allocation:
```json
{
  "memory": 4096  // 4GB
}
```

### "Agent initialization failed"

Check:
1. ANTHROPIC_API_KEY is valid
2. API key has proper permissions
3. Model name is correct
4. Network connectivity

## Best Practices

### Security

- ✅ Use environment variables for API keys
- ✅ Never commit `.env` files
- ✅ Rotate API keys regularly
- ✅ Enable E2B access controls
- ❌ Don't hardcode sensitive data

### Cost Optimization

- ✅ Use ephemeral mode for production
- ✅ Set appropriate timeouts
- ✅ Clean up unused sandboxes
- ✅ Monitor usage in E2B dashboard
- ❌ Don't leave persistent sandboxes running

### Performance

- ✅ Use persistent mode for development
- ✅ Create custom templates for repeated deployments
- ✅ Implement retry logic
- ✅ Cache frequently used data
- ❌ Don't create new sandbox for every test

### Monitoring

- ✅ Log all agent interactions
- ✅ Monitor resource usage
- ✅ Set up alerts for failures
- ✅ Track costs regularly
- ❌ Don't ignore error logs

## Advanced: Custom Templates

For production deployments, create custom E2B templates:

### 1. Create Dockerfile

```dockerfile
# .e2b/Dockerfile
FROM anthropic-claude-code

# Install project dependencies
COPY package.json package-lock.json ./
RUN npm ci --production

# Copy application
COPY . .
RUN npm run build

# Set entrypoint
ENTRYPOINT ["node", "dist/index.js"]
```

### 2. Build Template

```bash
e2b template build --name my-agent-template
```

### 3. Get Template ID

```bash
e2b template list
```

### 4. Use in Deployment

```typescript
const sandbox = await Sandbox.create('YOUR_TEMPLATE_ID', {
  apiKey: process.env.E2B_API_KEY
})
```

## Next Steps

1. **Try the examples**: Start with the TypeScript or Python examples
2. **Read the docs**: Check `/deploy-e2b` command for detailed deployment guide
3. **Explore templates**: Look at example templates in `examples/` directory
4. **Get help**: Use the e2b-sandbox-manager agent for deployment assistance

## Resources

- **E2B Documentation**: https://e2b.dev/docs
- **E2B Dashboard**: https://e2b.dev/dashboard
- **Claude Agent SDK**: https://docs.claude.com/en/api/agent-sdk
- **E2B GitHub**: https://github.com/e2b-dev/E2B
- **E2B CLI Reference**: https://e2b.dev/docs/cli

## Support

- **E2B Issues**: https://github.com/e2b-dev/E2B/issues
- **Claude Code Issues**: https://github.com/anthropics/claude-code/issues
- **E2B Discord**: https://discord.gg/e2b
- **Anthropic Support**: https://support.anthropic.com/

---

**Ready to deploy?** Start with the examples in `examples/e2b-typescript/` or `examples/e2b-python/`!
