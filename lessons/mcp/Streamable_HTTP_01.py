"""使用 Streamable HTTP 暴露一个不依赖模型的加法工具。"""

from mcp.server.fastmcp import FastMCP


mcp = FastMCP(
    "arithmetic",
    host="127.0.0.1",
    port=8000,
    streamable_http_path="/mcp",
    stateless_http=True,
    json_response=True,
)


@mcp.tool()
def add(a: int, b: int) -> int:
    """将两个整数相加。"""
    return a + b


def main():
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
