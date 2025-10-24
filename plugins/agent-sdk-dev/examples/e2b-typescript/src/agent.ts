import { Agent } from '@anthropic-ai/claude-agent-sdk'

export interface AgentConfig {
  apiKey: string
  systemPrompt?: string
  model?: string
}

export function createAgent(config: AgentConfig): Agent {
  const {
    apiKey,
    systemPrompt = 'You are a helpful AI assistant running in a secure E2B sandbox.',
    model = 'claude-sonnet-4-5-20250929'
  } = config

  return new Agent({
    apiKey,
    model,
    systemPrompt,

    // Configure permissions for sandbox environment
    permissions: {
      bash: true,
      read: true,
      write: true,
      edit: true,
      web: false // Disable external web access by default
    },

    // Optional: Add MCP servers for custom tools
    // mcpServers: {
    //   filesystem: {
    //     command: 'node',
    //     args: ['node_modules/@anthropic-ai/mcp-server-filesystem/dist/index.js']
    //   }
    // },

    // Optional: Configure streaming
    // streaming: true,

    // Optional: Add custom context
    // additionalContext: 'Running in E2B sandbox environment'
  })
}

export async function runAgent(agent: Agent, task: string): Promise<string> {
  try {
    const result = await agent.run({
      userPrompt: task
    })

    return result.output
  } catch (error) {
    console.error('Agent execution error:', error)
    throw error
  }
}
