import 'dotenv/config'
import { createAgent, runAgent } from './agent.js'

async function main() {
  const apiKey = process.env.ANTHROPIC_API_KEY
  if (!apiKey) {
    throw new Error('ANTHROPIC_API_KEY environment variable is required')
  }

  console.log('Initializing Claude Agent...')
  const agent = createAgent({ apiKey })

  // Example task
  const task = process.argv[2] || 'Hello! Can you help me understand how you work?'

  console.log(`\nTask: ${task}\n`)
  console.log('Agent response:')
  console.log('---')

  const response = await runAgent(agent, task)
  console.log(response)
  console.log('---')
}

main().catch(console.error)
