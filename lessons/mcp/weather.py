"""天气 MCP 服务：仅返回明确标注的模拟数据。"""

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("weather")


@mcp.tool()
def get_current_weather(city: str) -> str:
    """返回城市的模拟天气，不请求真实天气 API。"""
    return f"{city}的模拟天气：晴，25°C，风速 5 km/h。不是实时天气。"


def main():
    # stdout 专供 MCP 协议，不在这里打印启动日志。
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
