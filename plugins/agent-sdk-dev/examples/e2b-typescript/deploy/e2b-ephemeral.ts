import 'dotenv/config'
import { Sandbox } from '@e2b/code-interpreter'
import { createAgent, runAgent } from '../src/agent.js'

interface DeploymentConfig {
  e2bApiKey: string
  anthropicApiKey: string
  template?: string
  timeout?: number
}

export async function deployEphemeral(
  config: DeploymentConfig,
  task: string
): Promise<string> {
  const {
    e2bApiKey,
    anthropicApiKey,
    template = 'anthropic-claude-code',
    timeout = 300000
  } = config

  console.log('Creating E2B sandbox (ephemeral mode)...')

  const sandbox = await Sandbox.create(template, {
    apiKey: e2bApiKey,
    timeout
  })

  try {
    console.log(`Sandbox created: ${sandbox.id}`)
    console.log('Initializing agent in sandbox...')

    // Create agent
    const agent = createAgent({ apiKey: anthropicApiKey })

    console.log('Running task...')
    const result = await runAgent(agent, task)

    console.log('\n=== Agent Response ===')
    console.log(result)
    console.log('===================\n')

    return result

  } catch (error) {
    console.error('Deployment error:', error)
    throw error
  } finally {
    console.log('Cleaning up sandbox...')
    await sandbox.close()
    console.log('Sandbox closed')
  }
}

// CLI handler
if (import.meta.url === `file://${process.argv[1]}`) {
  const e2bApiKey = process.env.E2B_API_KEY
  const anthropicApiKey = process.env.ANTHROPIC_API_KEY

  if (!e2bApiKey || !anthropicApiKey) {
    console.error('Error: E2B_API_KEY and ANTHROPIC_API_KEY must be set')
    process.exit(1)
  }

  const task = process.argv[2] || 'Write a simple Python hello world script'

  deployEphemeral(
    {
      e2bApiKey,
      anthropicApiKey,
      template: process.env.E2B_TEMPLATE,
      timeout: process.env.E2B_TIMEOUT ? parseInt(process.env.E2B_TIMEOUT) : undefined
    },
    task
  )
    .then(() => {
      console.log('Deployment completed successfully')
      process.exit(0)
    })
    .catch((error) => {
      console.error('Deployment failed:', error)
      process.exit(1)
    })
}
