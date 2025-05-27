from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
import asyncio
import nest_asyncio

nest_asyncio.apply()


async def create_agent():
    """Gets tools from MCP Server."""
    tools, exit_stack = await MCPToolset.from_server(
      connection_params=StdioServerParameters(
          command='npx',
          args=["-y",    # Arguments for the command
            "@modelcontextprotocol/server-filesystem",
            "/home/manjesh_2j/adk_to_agent_engine",
          ],
      )
    )
    agent = LlmAgent(
      model='gemini-2.0-flash',
      name='enterprise_assistant',
      instruction=(
          'Help user accessing their file systems'
      ),
      tools=tools,
    )
    return agent, exit_stack

root_agent, exit_stack = asyncio.run(create_agent())