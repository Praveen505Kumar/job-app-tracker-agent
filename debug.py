# # debug_tools.py
# import asyncio
# import json

# from dotenv import load_dotenv

# load_dotenv()
# from langchain_mcp_adapters.client import MultiServerMCPClient

# from auth.gmail_oauth import get_access_token


# async def main():
#     access_token = get_access_token()
#     server_config = {
#         "gmail": {
#             "url": "https://gmailmcp.googleapis.com/mcp/v1",
#             "transport": "streamable_http",
#             "headers": {"Authorization": f"Bearer {access_token}"},
#         }
#     }
#     client = MultiServerMCPClient(server_config)
#     tools = await client.get_tools()

#     for t in tools:
#         if t.name == "search_threads":
#             print("Description:", t.description)
#             print("Args schema:")
#             print(json.dumps(t.args_schema, indent=2, default=str))


# if __name__ == "__main__":
#     asyncio.run(main())
