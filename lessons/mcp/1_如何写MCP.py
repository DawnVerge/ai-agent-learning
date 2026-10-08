"""最小 stdio MCP 服务；与 weather.py 对照阅读。"""

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("weather-intro")


@mcp.tool()
def get_current_weather(city: str) -> str:
    """返回城市的模拟天气。"""
    return f"{city}的模拟天气：晴，25°C。不是实时天气。"


if __name__ == "__main__":
    mcp.run(transport="stdio")
