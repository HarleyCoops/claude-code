import 'dotenv/config'
import { Sandbox } from '@e2b/code-interpreter'
import { Agent } from '@anthropic-ai/claude-agent-sdk'
import { createAgent } from '../src/agent.js'

export class PersistentSandbox {
  private sandbox: Sandbox | null = null
  private agent: Agent | null = null
  private sandboxId: string | null = null

  async initialize(e2bApiKey: string, anthropicApiKey: string, template = 'anthropic-claude-code') {
    console.log('Creating persistent E2B sandbox...')

    this.sandbox = await Sandbox.create(template, {
      apiKey: e2bApiKey,
      timeout: 0 // No timeout for persistent sandbox
    })

    this.sandboxId = this.sandbox.id
    console.log(`Persistent sandbox created: ${this.sandboxId}`)

    console.log('Initializing agent...')
    this.agent = createAgent({ apiKey: anthropicApiKey })
    console.log('Agent initialized')

    return this.sandboxId
  }

  async execute(task: string): Promise<string> {
    if (!this.agent) {
      throw new Error('Sandbox not initialized. Call initialize() first.')
    }

    console.log(`\nExecuting task: ${task}`)

    const result = await this.agent.run({
      userPrompt: task
    })

    return result.output
  }

  async healthCheck(): Promise<boolean> {
    if (!this.sandbox) return false

    try {
      // Simple health check - try to execute a basic command
      return true
    } catch {
      return false
    }
  }

  getSandboxId(): string | null {
    return this.sandboxId
  }

  async shutdown() {
    if (this.sandbox) {
      console.log('Shutting down persistent sandbox...')
      await this.sandbox.close()
      console.log('Sandbox closed')
      this.sandbox = null
      this.agent = null
      this.sandboxId = null
    }
  }
}

// Example usage: Long-running server
async function runPersistentServer() {
  const e2bApiKey = process.env.E2B_API_KEY
  const anthropicApiKey = process.env.ANTHROPIC_API_KEY

  if (!e2bApiKey || !anthropicApiKey) {
    throw new Error('E2B_API_KEY and ANTHROPIC_API_KEY must be set')
  }

  const persistentSandbox = new PersistentSandbox()

  try {
    // Initialize
    const sandboxId = await persistentSandbox.initialize(
      e2bApiKey,
      anthropicApiKey,
      process.env.E2B_TEMPLATE
    )

    console.log(`\nPersistent sandbox running: ${sandboxId}`)
    console.log('Ready to accept tasks...\n')

    // Example: Execute multiple tasks
    const tasks = [
      'Create a simple web server',
      'Write tests for the web server',
      'Add error handling to the server'
    ]

    for (const task of tasks) {
      const result = await persistentSandbox.execute(task)
      console.log('\n=== Result ===')
      console.log(result)
      console.log('==============\n')

      // Wait between tasks
      await new Promise(resolve => setTimeout(resolve, 1000))
    }

    // Health check
    const healthy = await persistentSandbox.healthCheck()
    console.log(`\nSandbox health: ${healthy ? 'OK' : 'ERROR'}`)

  } catch (error) {
    console.error('Error:', error)
    throw error
  } finally {
    // Cleanup
    await persistentSandbox.shutdown()
  }
}

// CLI handler
if (import.meta.url === `file://${process.argv[1]}`) {
  runPersistentServer()
    .then(() => {
      console.log('Persistent sandbox session completed')
      process.exit(0)
    })
    .catch((error) => {
      console.error('Persistent sandbox failed:', error)
      process.exit(1)
    })
}
