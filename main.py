import asyncio
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from mcp_use import MCPAgent, MCPClient

async def main():
    load_dotenv()
    client = MCPClient.from_config_file("config.json")
    
    llm = ChatOpenAI(model="gpt-4o")
    agent = MCPAgent(llm=llm, client=client, max_steps=30)
    # async for chunk in agent.astream("add 1 2"):
    #     print(chunk.get("messages", ""), end="", flush=True)
    print(await agent.run("add 1 2"))

if __name__ == "__main__":
    asyncio.run(main())
