## Homework: Agents

## Preparation

First, we'll define a function that we will use when building
our agent. 

It will generate fake weather data:

```python
import random

known_weather_data = {
    'berlin': 20.0
}

def get_weather(city: str) -> float:
    city = city.strip().lower()

    if city in known_weather_data:
        return known_weather_data[city]

    return round(random.uniform(-5, 35), 1)
```


## Q1. Define function description

We want to use it as a tool for our agent, so we need to 
describe it 

How should the description for this function look like? Fill in missing parts

```python
get_weather_tool = {
    "type": "function",
    "name": "<TODO1>",
    "description": "<TODO2>",
    "parameters": {
        "type": "object",
        "properties": {
            "<TODO3>": {
                "type": "string",
                "description": "<TODO4>"
            }
        },
        "required": [TODO5],
        "additionalProperties": False
    }
}
```

What did you put in `TODO3`?

## Answer: "city"

```python
get_weather_tool = {
    "type": "function",
    "name": "get_weather",
    "description": "Obtiene la temperatura actual para una ciudad dada. Si no hay datos guardados, devuelve un valor aleatorio entre -5 y 35 °C.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "Nombre de la ciudad cuya temperatura se desea consultar."
            }
        },
        "required": ["city"],
        "additionalProperties": False
    }
}
```

## Q2. Adding another tool

Let's add another tool - a function that can add weather data
to our database:

```python
def set_weather(city: str, temp: float) -> None:
    city = city.strip().lower()
    known_weather_data[city] = temp
    return 'OK'
```

Now let's write a description for it.

What did you write?

## Answer:
```python
set_weather_tool = {
    "type": "function",
    "name": "set_weather",
    "description": "Actualiza o añade la temperatura registrada para una ciudad dada.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "Nombre de la ciudad cuya temperatura se va a actualizar o añadir."
            },
            "temp": {
                "type": "number",
                "description": "Temperatura en grados Celsius a registrar."
            }
        },
        "required": ["city", "temp"],
        "additionalProperties": False
    }
}
```
## MCP

MCP stands for Model-Context Protocol. It allows LLMs communicate
with different tools (like Qdrant). It's function calling, but 
one step further:

* A tool can export a list of functions it has
* When we include the tool to our Agent, we just need to include the link to the MCP server

## Q3. Install FastMCP

Let's install a library for MCP - [FastMCP](https://github.com/jlowin/fastmcp):

```bash
pip install fastmcp
```

What's the version of FastMCP you installed?

## Answer: 
```python
import fastmcp
fastmcp.__version__
```
```bash
'2.10.6'
```
## Q4. Simple MCP Server 

A simple MCP server from the documentation looks like that:

```python
# weather_server.py
from fastmcp import FastMCP

mcp = FastMCP("Demo 🚀")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

if __name__ == "__main__":
    mcp.run()
```

In our case, we need to write docstrings for our functions.

Let's ask ChatGPT for help:

```python
def get_weather(city: str) -> float:
    """
    Retrieves the temperature for a specified city.

    Parameters:
        city (str): The name of the city for which to retrieve weather data.

    Returns:
        float: The temperature associated with the city.
    """
    city = city.strip().lower()

    if city in known_weather_data:
        return known_weather_data[city]

    return round(random.uniform(-5, 35), 1)


def set_weather(city: str, temp: float) -> None:
    """
    Sets the temperature for a specified city.

    Parameters:
        city (str): The name of the city for which to set the weather data.
        temp (float): The temperature to associate with the city.

    Returns:
        str: A confirmation string 'OK' indicating successful update.
    """
    city = city.strip().lower()
    known_weather_data[city] = temp
    return 'OK'
```

Let's change the example for our case and run it

What do you see in the output?

Look for a string that matches this template:

```
Starting MCP server 'Demo 🚀' with transport '<TODO>'
```

What do you have instead of `<TODO>`?

## Answer: `'stdio'`
```bash
[07/20/25 14:08:18] INFO     Starting MCP server 'Demo' with transport 'stdio'
```

## Q5. Protocol

There are different ways to communicate with an MCP server.
Ours is currently running using standart input/output, which
means that the client write something to stdin and read the
answer using stdout.

Our weather server is currently running.

This is how we start communitcating with it:

- First, we send an initialization request -- this way, we register our client with the server:
    ```json
    {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {"roots": {"listChanged": true}, "sampling": {}}, "clientInfo": {"name": "test-client", "version": "1.0.0"}}}
    ```
    We should get back something like that, which is an aknowledgement of the request:
    ```json
    {"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2024-11-05","capabilities":{"experimental":{},"prompts":{"listChanged":false},"resources":{"subscribe":false,"listChanged":false},"tools":{"listChanged":true}},"serverInfo":{"name":"Demo 🚀","version":"1.9.4"}}}
    ```
-  Next, we reply back, confirming the initialization:
    ```json
    {"jsonrpc": "2.0", "method": "notifications/initialized"}
    ```
    We don't expect to get anything in response
- Now we can ask for a list of available methods:
    ```json
    {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
    ```
- Let's ask the temperature in Berlin:
    ```json
    {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "<TODO>", "arguments": {<TODO>}}}
    ```
- What did you get in response?

## Answer:
```json
{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "get_weather", "arguments": {"city": "Berlin"}}}
```
Response:
```json
{"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text","text":"20.0"}],"structuredContent":{"result":20.0},"isError":false}}
```

## Q6. Client

We typically don't interact with the server by copy-pasting 
commands in the terminal.

In practice, we use an MCP Client. Let's implement it. 

FastMCP also supports MCP clients:

```python
from fastmcp import Client

async def main():
    async with Client(<TODO>) as mcp_client:
        # TODO
```

Use the client to get the list of available tools
of our script. How does the result look like?

If you're running this code in Jupyter, you need to pass
an instance of MCP server to the `Client`:

```python
import weather_server

async def main():
    async with Client(weather_server.mcp) as mcp_client:
        # ....
```

If you run it in a script, you will need to use asyncio:

```python
import asyncio

async def main():
    async with Client("weather_server.py") as mcp_client:
        # ...

if __name__ == "__main__":
    test = asyncio.run(main())
```

Copy the output with the available tools when
filling in the homework form.

## Answer
```python
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
```

```bash
Available tools: [Tool(name='get_weather', title=None, description='Retrieves the temperature for a specified city.\n\nParameters:\n    city (str): The name of the city for which to retrieve weather data.\n\nReturns:\n    float: The temperature associated with the city.', inputSchema={'properties': {'city': {'title': 'City', 'type': 'string'}}, 'required': ['city'], 'type': 'object'}, outputSchema={'properties': {'result': {'title': 'Result', 'type': 'number'}}, 'required': ['result'], 'title': '_WrappedResult', 'type': 'object', 'x-fastmcp-wrap-result': True}, annotations=None, meta=None), Tool(name='set_weather', title=None, description="Sets the temperature for a specified city.\n\nParameters:\n    city (str): The name of the city for which to set the weather data.\n    temp (float): The temperature to associate with the city.\n\nReturns:\n    str: A confirmation string 'OK' indicating successful update.", inputSchema={'properties': {'city': {'title': 'City', 'type': 'string'}, 'temp': {'title': 'Temp', 'type': 'number'}}, 'required': ['city', 'temp'], 'type': 'object'}, outputSchema={'properties': {'result': {'title': 'Result', 'type': 'string'}}, 'required': ['result'], 'title': '_WrappedResult', 'type': 'object', 'x-fastmcp-wrap-result': True}, annotations=None, meta=None)]

```
[Jupyter Notebook](agents.ipynb)
