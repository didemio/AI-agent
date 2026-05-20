import os
from typing import Dict, Any, List
from google import genai
from google.genai import types
from tools.registry import ToolRegistry
from memory import MemoryManager

class GeminiAgent:
    """
    Core orchestrator of the system executing the ReAct (Reason -> Act -> Observe) execution loop.
    Deploys the modern Google GenAI SDK via structured configurations.
    """
    def __init__(self, registry: ToolRegistry, memory: MemoryManager):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Environment variable 'GEMINI_API_KEY' is missing.")
        
        # Initializing the modern GenAI Client instance
        self.client = genai.Client(api_key=api_key.strip('"'))
        
        self.registry = registry
        self.memory = memory
        
        # Updated to the correct canonical identifier for the modern SDK
        self.model_name = "gemini-2.5-flash"
        
        self.system_instruction = (
            "You are an advanced, adaptive AI personal assistant agent. "
            "You have autonomous access to native external tools. Leverage these tools "
            "when required by following the ReAct pattern. If no tool is necessary, "
            "respond directly via natural language."
        )

    def _convert_history_to_contents(self) -> List[types.Content]:
        """
        Maps raw session history into SDK-compliant types.Content objects.
        Ensures strict data structure safety over multi-turn interactions.
        """
        contents = []
        for turn in self.memory.get_history():
            role = turn["role"]
            sdk_parts = []
            
            for part in turn["parts"]:
                if isinstance(part, dict) and "function_call" in part:
                    sdk_parts.append(types.Part.from_function_call(
                        name=part["function_call"]["name"],
                        args=part["function_call"]["args"]
                    ))
                elif isinstance(part, dict) and "function_response" in part:
                    sdk_parts.append(types.Part.from_function_response(
                        name=part["function_response"]["name"],
                        response=part["function_response"]["response"]
                    ))
                else:
                    sdk_parts.append(types.Part.from_text(text=str(part)))
                    
            contents.append(types.Content(role=role, parts=sdk_parts))
        return contents

    def _generate_config(self) -> types.GenerateContentConfig:
        """Compiles system instructions, declarations, and parameters into a safe runtime config."""
        declarations = self.registry.list_declarations()
        
        sdk_tools = []
        if declarations:
            sdk_tools.append(types.Tool(function_declarations=[
                types.FunctionDeclaration(**dec) for dec in declarations
            ]))

        return types.GenerateContentConfig(
            system_instruction=self.system_instruction,
            temperature=0.2,
            tools=sdk_tools if sdk_tools else None
        )

    def run(self, user_input: str) -> str:
        """Orchestrates the iterative execution flow up to a definitive resolution turn."""
        self.memory.add_user_message(user_input)
        max_turns = 5
        
        for _ in range(max_turns):
            contents = self._convert_history_to_contents()
            config = self._generate_config()
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=config
            )
            
            if not response.candidates or not response.candidates[0].content.parts:
                return "Error: Received an incomplete response payload from the model."
                
            part = response.candidates[0].content.parts[0]
            
            # Scenario A: Model decides to emit a final text answer direct execution path
            if part.text:
                self.memory.add_model_message(part.text)
                return part.text
                
            # Scenario B: Model requests tool execution (Function Calling)
            if part.function_call:
                function_name = part.function_call.name
                arguments = dict(part.function_call.args)
                
                print(f"\n[AGENT REASONING]: Invoking tool -> {function_name}({arguments})")
                
                # Execute tool securely via registry boundary
                tool_output = self.registry.execute_tool(function_name, arguments)
                print(f"[AGENT OBSERVED]: Tool response context -> {tool_output}\n")
                
                # Commit interaction to conversational history block
                self.memory.add_function_call_history(function_name, arguments, tool_output)
                
        return "Agent failed to resolve context within acceptable execution bounds."