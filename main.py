"""Entrypoint: authenticates with Gmail, connects to the MCP server, runs one pass."""

import asyncio
import json

from dotenv import load_dotenv

load_dotenv()
from langchain_mcp_adapters.client import MultiServerMCPClient

from graph import build_graph


async def main():
    with open("mcp_config.json") as f:
        server_config = json.load(f)

    client = MultiServerMCPClient(server_config)
    tools = await client.get_tools()
    tools_by_name = {t.name: t for t in tools}

    print(f"Connected. Available Gmail MCP tools: {list(tools_by_name.keys())}\n")

    app = build_graph(tools_by_name)
    result = await app.ainvoke(
        {
            "query": "",
            "raw_emails": [],
            "applications": [],
            "new_rows_written": 0,
            "summary": "",
        }
    )

    print(result["summary"])


if __name__ == "__main__":
    asyncio.run(main())
