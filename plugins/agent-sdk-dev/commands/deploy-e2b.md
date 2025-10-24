---
description: Deploy Claude Agent SDK application to E2B sandbox
argument-hint: [deployment-mode]
---

You are tasked with deploying a Claude Agent SDK application to an E2B sandbox. E2B provides secure, isolated cloud sandboxes for running AI agents.

## Prerequisites Check

First, verify the following:

1. **E2B CLI Installation**:
   ```bash
   npm list -g @e2b/cli
   ```
   If not installed: `npm install -g @e2b/cli`

2. **API Keys Present**:
   - E2B_API_KEY (from https://e2b.dev/dashboard)
   - ANTHROPIC_API_KEY (from https://console.anthropic.com/)

   Check if these are in `.env` or environment variables

3. **Detect Project Type**:
   - Check for `package.json` (TypeScript/JavaScript)
   - Check for `requirements.txt` or `pyproject.toml` (Python)

## Deployment Modes

Ask the user which deployment mode they want (skip if $ARGUMENTS specifies):

1. **ephemeral** - Create sandbox per request, destroy after completion
   - Best for: Stateless agents, one-off tasks
   - Resource efficient, maximum isolation

2. **persistent** - Long-running sandbox instance
   - Best for: Stateful workflows, development/testing
   - Maintains state between requests

3. **template** - Create custom E2B template for reuse
   - Best for: Production deployments, multiple instances
   - Pre-configured environment, faster spin-up

## Deployment Process

### Step 1: Create E2B Configuration

Create or update `e2b.config.json` in the project root:

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

For Python projects:
```json
{
  "template": "anthropic-claude-code",
  "buildCommand": "pip install -r requirements.txt",
  "startCommand": "python main.py",
  "env": {
    "ANTHROPIC_API_KEY": "$ANTHROPIC_API_KEY",
    "PYTHON_ENV": "production"
  },
  "timeout": 300000,
  "memory": 2048
}
```

### Step 2: Create Deployment Wrapper

Based on deployment mode, create the appropriate wrapper:

**For Ephemeral Mode (TypeScript)**:
Create `deploy/e2b-ephemeral.ts`:

```typescript
import { Sandbox } from '@e2b/code-interpreter'
import { Agent } from '@anthropic-ai/claude-agent-sdk'

interface DeploymentConfig {
  apiKey: string
  anthropicKey: string
  template?: string
}

export async function deployEphemeral(config: DeploymentConfig) {
  const sandbox = await Sandbox.create(
    config.template || 'anthropic-claude-code',
    { apiKey: config.apiKey }
  )

  try {
    // Initialize agent in sandbox context
    const agent = new Agent({
      apiKey: config.anthropicKey,
      model: 'claude-sonnet-4-5-20250929',
      systemPrompt: 'Your agent system prompt here',
      // Add your agent configuration
    })

    // Your agent logic here
    const result = await agent.run({
      userPrompt: 'Your task'
    })

    return result
  } finally {
    await sandbox.close()
  }
}

// CLI handler
if (import.meta.url === `file://${process.argv[1]}`) {
  deployEphemeral({
    apiKey: process.env.E2B_API_KEY!,
    anthropicKey: process.env.ANTHROPIC_API_KEY!
  }).then(console.log).catch(console.error)
}
```

**For Ephemeral Mode (Python)**:
Create `deploy/e2b_ephemeral.py`:

```python
import os
from e2b_code_interpreter import Sandbox
from claude_agent_sdk import Agent

def deploy_ephemeral(api_key: str, anthropic_key: str, template: str = "anthropic-claude-code"):
    """Deploy agent in ephemeral E2B sandbox"""

    sandbox = Sandbox(template=template)

    try:
        # Initialize agent
        agent = Agent(
            api_key=anthropic_key,
            model="claude-sonnet-4-5-20250929",
            system_prompt="Your agent system prompt here"
        )

        # Your agent logic here
        result = agent.run(user_prompt="Your task")

        return result

    finally:
        sandbox.close()

if __name__ == "__main__":
    result = deploy_ephemeral(
        api_key=os.environ["E2B_API_KEY"],
        anthropic_key=os.environ["ANTHROPIC_API_KEY"]
    )
    print(result)
```

**For Persistent Mode (TypeScript)**:
Create `deploy/e2b-persistent.ts`:

```typescript
import { Sandbox } from '@e2b/code-interpreter'
import { Agent } from '@anthropic-ai/claude-agent-sdk'

export class PersistentSandbox {
  private sandbox: Sandbox | null = null
  private agent: Agent | null = null

  async initialize(apiKey: string, anthropicKey: string) {
    this.sandbox = await Sandbox.create('anthropic-claude-code', {
      apiKey,
      timeout: 0 // No timeout for persistent
    })

    this.agent = new Agent({
      apiKey: anthropicKey,
      model: 'claude-sonnet-4-5-20250929',
      // Agent config
    })

    console.log(`Sandbox initialized: ${this.sandbox.id}`)
    return this.sandbox.id
  }

  async execute(task: string) {
    if (!this.agent) throw new Error('Not initialized')
    return await this.agent.run({ userPrompt: task })
  }

  async shutdown() {
    if (this.sandbox) {
      await this.sandbox.close()
      console.log('Sandbox closed')
    }
  }
}

// Example usage
const persistent = new PersistentSandbox()
await persistent.initialize(
  process.env.E2B_API_KEY!,
  process.env.ANTHROPIC_API_KEY!
)

// Keep alive and handle requests...
```

### Step 3: Install E2B Dependencies

Based on project type:

**TypeScript/JavaScript**:
```bash
npm install @e2b/code-interpreter @e2b/sdk
```

**Python**:
```bash
pip install e2b-code-interpreter e2b
```

### Step 4: Create Deployment Scripts

Add to `package.json` (TypeScript):
```json
{
  "scripts": {
    "deploy:e2b:ephemeral": "node --loader ts-node/esm deploy/e2b-ephemeral.ts",
    "deploy:e2b:persistent": "node --loader ts-node/esm deploy/e2b-persistent.ts",
    "e2b:create-template": "e2b template build"
  }
}
```

Or create `Makefile` (Python):
```makefile
.PHONY: deploy-ephemeral deploy-persistent

deploy-ephemeral:
	python deploy/e2b_ephemeral.py

deploy-persistent:
	python deploy/e2b_persistent.py

e2b-template:
	e2b template build
```

### Step 5: Test Deployment

1. **Test locally first**:
   ```bash
   # Set environment variables
   export E2B_API_KEY=your_key
   export ANTHROPIC_API_KEY=your_key

   # Run deployment
   npm run deploy:e2b:ephemeral  # or python deploy/e2b_ephemeral.py
   ```

2. **Verify sandbox creation**:
   ```bash
   e2b sandbox list
   ```

3. **Check logs**:
   - Monitor sandbox output for errors
   - Verify agent initialization
   - Test agent functionality

### Step 6: Production Considerations

Create `.e2b/README.md` with production guidelines:

```markdown
# E2B Production Deployment

## Environment Variables
- E2B_API_KEY: Get from https://e2b.dev/dashboard
- ANTHROPIC_API_KEY: Get from https://console.anthropic.com/

## Monitoring
- Use E2B dashboard for sandbox metrics
- Implement logging in agent code
- Set up alerts for failures

## Scaling
- Ephemeral: Auto-scales with requests
- Persistent: Manage instance count manually
- Template: Deploy multiple instances from template

## Cost Optimization
- Use ephemeral for short tasks
- Implement timeout policies
- Clean up unused sandboxes
- Monitor resource usage

## Security
- Never commit API keys
- Use environment variables only
- Enable E2B access controls
- Audit sandbox activity regularly
```

## Template Creation (Advanced)

For production deployments, create a custom E2B template:

1. **Create `.e2b/Dockerfile`**:
```dockerfile
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

2. **Build template**:
```bash
e2b template build --name my-agent-app
```

3. **Get template ID**:
```bash
e2b template list
```

4. **Update deployment scripts** to use custom template ID

## Verification

After deployment:

1. Test agent responds correctly
2. Verify sandbox isolation
3. Check resource usage
4. Test error handling
5. Verify cleanup on completion

## Troubleshooting

Common issues:

1. **Sandbox timeout**: Increase timeout in config
2. **Out of memory**: Increase memory allocation
3. **API rate limits**: Implement retry logic
4. **Network issues**: Check E2B status page
5. **Agent errors**: Check ANTHROPIC_API_KEY and model availability

## Next Steps

Provide the user with:

1. Deployment confirmation with sandbox ID
2. How to monitor the deployment
3. How to tear down resources
4. Links to E2B dashboard
5. Command to check sandbox status: `e2b sandbox list`

## Documentation Links

- E2B Documentation: https://e2b.dev/docs
- E2B API Reference: https://e2b.dev/docs/api
- Claude Agent SDK Hosting: https://docs.claude.com/en/api/agent-sdk/hosting
- E2B Dashboard: https://e2b.dev/dashboard
