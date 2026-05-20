from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseTool(ABC):
    """
    Abstract Base Class defining the structural contract for all tools.
    Follows the Dependency Inversion Principle (DIP) and Open/Closed Principle (OCP).
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Returns the unique name of the tool recognized by the LLM."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Returns a clear description of the tool's functionality for the LLM."""
        pass

    @abstractmethod
    def get_declaration(self) -> Dict[str, Any]:
        """Returns the JSON schema declaration required for Gemini Function Calling."""
        pass

    @abstractmethod
    def execute(self, **kwargs) -> str:
        """Executes the core tool logic and guarantees a string output."""
        pass