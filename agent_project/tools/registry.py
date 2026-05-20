from typing import Dict, List, Any
from tools.base import BaseTool

class ToolRegistry:
    """
    Implements the Factory / Registry Pattern to dynamically manage tools.
    Prevents monolithic if-else branching within the core Agent loop.
    """
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        """Registers a new tool into the runtime environment."""
        if tool.name in self._tools:
            raise ValueError(f"Tool with name '{tool.name}' is already registered.")
        self._tools[tool.name] = tool

    def get_tool(self, name: str) -> BaseTool:
        """Retrieves a tool instance by its registered name."""
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' not found in registry.")
        return self._tools[name]

    def list_declarations(self) -> List[Dict[str, Any]]:
        """Compiles all registered tool schemas for Gemini API consumption."""
        return [tool.get_declaration() for tool in self._tools.values()]

    def execute_tool(self, name: str, argument_dict: Dict[str, Any]) -> str:
        """
        Executes a registered tool given its name and arguments.
        Implements Robust Error Handling for API and runtime execution anomalies.
        """
        try:
            tool = self.get_tool(name)
            return tool.execute(**argument_dict)
        except KeyError:
            return f"Error: Tool '{name}' is not supported by the system."
        except Exception as e:
            return f"Error executing tool '{name}': {str(e)}"