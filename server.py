from fastmcp import FastMCP

mcp = FastMCP("Teste MCP")

@mcp.tool(description="Adds two numbers together")
def add(a: int, b: int) -> int:
    return a + b

@mcp.tool(description="Subtracts two numbers")
def subtract(a: int, b: int) -> int:
    return a - b

@mcp.tool(description="Multiplies two numbers")
def multiply(a: int, b: int) -> int:
    return a * b


mcp.run(host="127.0.0.1", port=8090,transport="sse")







