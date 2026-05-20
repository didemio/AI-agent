import datetime
from typing import Dict, Any
from tools.base import BaseTool

class CalculatorTool(BaseTool):
    @property
    def name(self) -> str:
        return "calculator"

    @property
    def description(self) -> str:
        return "Performs basic mathematical operations: addition, subtraction, multiplication, and division."

    def get_declaration(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "operation": {
                        "type": "STRING", 
                        "description": "The math operation to perform: 'add', 'subtract', 'multiply', 'divide'"
                    },
                    "a": {"type": "NUMBER", "description": "The first number"},
                    "b": {"type": "NUMBER", "description": "The second number"}
                },
                "required": ["operation", "a", "b"]
            }
        }

    def execute(self, operation: str, a: float, b: float) -> str:
        if operation == "add":
            return str(a + b)
        elif operation == "subtract":
            return str(a - b)
        elif operation == "multiply":
            return str(a * b)
        elif operation == "divide":
            if b == 0:
                return "Error: Division by zero is undefined."
            return str(a / b)
        else:
            return f"Error: Invalid operation '{operation}'."

class CurrentTimeTool(BaseTool):
    @property
    def name(self) -> str:
        return "get_current_time"

    @property
    def description(self) -> str:
        return "Retrieves the current local system date and time."

    def get_declaration(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {"type": "OBJECT", "properties": {}}
        }

    def execute(self) -> str:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class CurrencyConverterTool(BaseTool):
    @property
    def name(self) -> str:
        return "convert_currency"

    @property
    def description(self) -> str:
        return "Converts monetary values between EUR, USD, and TRY using static exchange rates."

    def get_declaration(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "amount": {"type": "NUMBER", "description": "The amount of currency to convert"},
                    "from_currency": {"type": "STRING", "description": "Source currency code (USD, EUR, TRY)"},
                    "to_currency": {"type": "STRING", "description": "Target currency code (USD, EUR, TRY)"}
                },
                "required": ["amount", "from_currency", "to_currency"]
            }
        }

    def execute(self, amount: float, from_currency: str, to_currency: str) -> str:
        rates = {"USD": 1.0, "EUR": 0.92, "TRY": 32.50}
        src = from_currency.upper()
        tgt = to_currency.upper()
        
        if src not in rates or tgt not in rates:
            return "Error: Unsupported currency code. Supported: USD, EUR, TRY."
        
        amount_in_usd = amount / rates[src]
        converted = amount_in_usd * rates[tgt]
        return f"{amount} {src} = {converted:.2f} {tgt}"

class AdviceGeneratorTool(BaseTool):
    @property
    def name(self) -> str:
        return "get_expert_advice"

    @property
    def description(self) -> str:
        return "Generates structured expert advice for a specific category: 'software', 'motivation', or 'botany'."

    def get_declaration(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "category": {
                        "type": "STRING", 
                        "description": "Category for the advice: 'software', 'motivation', 'botany'"
                    }
                },
                "required": ["category"]
            }
        }

    def execute(self, category: str) -> str:
        cat = category.lower()
        if cat == "software":
            return "Advice: Adhere strictly to SOLID principles and write modular code to ensure system extensibility."
        elif cat == "motivation":
            return "Advice: Complex projects are completed through consistent, iterative milestones. Keep pushing forward."
        elif cat == "botany":
            return "Advice: Prevent root rot by ensuring adequate soil drainage and avoiding overwatering."
        else:
            return "Advice: Always maintain a balance between technical execution and architectural planning."