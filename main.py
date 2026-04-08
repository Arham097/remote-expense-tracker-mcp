from fastmcp import FastMCP
import json
import random

mcp = FastMCP("Simple Calculator Server")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers.
    
    Args:
        a: The first number.
        b: The second number.

    Returns:
        The sum of the a and b.
    """
    return a + b

@mcp.tool
def random_number(min_val: int = 1, max_val: int = 100) -> int:
    """Generate a random number within the range
    
    Args:
        min_val: The minimum value of the random number (inclusive) (default: 1).
        max_val: The maximum value of the random number (inclusive) (default: 100).

    Returns:
        A random integer between min_val and max_val.
    """
    return random.randint(min_val, max_val)

@mcp.resource("info://server")
def server_info() -> dict:
    """Get information about the server.

    Returns:
        A dictionary containing information about the server.
    """
    info=  {
        "name": "Simple Calculator Server",
        "version": "1.0",
        "description": "A simple calculator server that provides basic arithmetic operations and random number generation.",
        "tools": [
            {
                "name": "add",
                "description": "Add two numbers.",
                "parameters": {
                    "a": {
                        "type": "int",
                        "description": "The first number."
                    },
                    "b": {
                        "type": "int",
                        "description": "The second number."
                    }
                },
                "returns": {
                    "type": "int",
                    "description": "The sum of the a and b."
                }
            },
            {
                "name": "random_number",
                "description": "Generate a random number within the range.",
                "parameters": {
                    "min_val": {
                        "type": "int",
                        "description": "The minimum value of the random number (inclusive) (default: 1)."
                    },
                    "max_val": {
                        "type": "int",
                        "description": "The maximum value of the random number (inclusive) (default: 100)."
                    }
                },
                "returns": {
                    "type": "int",
                    "description": "A random integer between min_val and max_val."
                }
            }
        ]
    }
    return json.dumps(info, indent=2)
    

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
