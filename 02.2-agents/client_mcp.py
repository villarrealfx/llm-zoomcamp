from fastmcp import Client
import asyncio

async def main():
   # Connect via stdio to a local script
    async with Client("weather_server.py") as mcp_client:
        tools = await mcp_client.list_tools()
        print(f"Available tools: {tools}")

        # 1. Obtener clima de una ciudad
        temperature = await mcp_client.call_tool("get_weather", {"city": "Berlin"})
        print(f"Temperatura en Berlín: {temperature}°C")

        # 2. Establecer nuevo clima
        result = await mcp_client.call_tool("set_weather", {"city": "Madrid", "temp": 25.5})
        print(f"Resultado de set_weather: {result}")
        
        # 3. Obtener el clima que acabamos de establecer
        new_temp = await mcp_client.call_tool("get_weather", {"city": "Madrid"})
        print(f"Nueva temperatura en Madrid: {new_temp}°C")


if __name__ == "__main__":
    asyncio.run(main())