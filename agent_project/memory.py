from typing import List, Dict, Any

class MemoryManager:
    """
    Manages conversational context history.
    Ensures Separation of Concerns (SRP) by decoupling state management from the Agent loop.
    """
    def __init__(self):
        self._history: List[Dict[str, Any]] = []

    def add_user_message(self, text: str) -> None:
        """Appends a standard user textual message to history."""
        self._history.append({"role": "user", "parts": [text]})

    def add_model_message(self, text: str) -> None:
        """Appends a standard model textual response to history."""
        self._history.append({"role": "model", "parts": [text]})

    def add_function_call_history(self, function_name: str, args: Dict[str, Any], tool_result: str) -> None:
        """
        Appends consecutive turns representing an LLM function call event 
        and the respective programmatic system response to maintain ReAct sequence integrity.
        """
        self._history.append({
            "role": "model",
            "parts": [{
                "function_call": {
                    "name": function_name,
                    "args": args
                }
            }]
        })
        self._history.append({
            "role": "user",
            "parts": [{
                "function_response": {
                    "name": function_name,
                    "response": {"result": tool_result}
                }
            }]
        })

    def get_history(self) -> List[Dict[str, Any]]:
        """Returns the conversational state payload."""
        return self._history

    def clear(self) -> None:
        """Flushes the stored conversational history."""
        self._history.clear()