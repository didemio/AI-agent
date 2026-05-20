from tools.registry import ToolRegistry
from tools.custom_tools import CalculatorTool, CurrentTimeTool, CurrencyConverterTool, AdviceGeneratorTool
from memory import MemoryManager
from agent import GeminiAgent

def main():
    print("=" * 60)
    print("  INITIALIZING ADAPTIVE AI AGENT FRAMEWORK INTERFACE (CLI)")
    print("=" * 60)
    print("Type 'exit' or 'quit' to terminate the session.\n")

    # Dependency Injection (Architectural decoupling)
    registry = ToolRegistry()
    memory = MemoryManager()

    # Runtime Component Registration (Factory Pattern implementation)
    registry.register(CalculatorTool())
    registry.register(CurrentTimeTool())
    registry.register(CurrencyConverterTool())
    registry.register(AdviceGeneratorTool())

    try:
        agent = GeminiAgent(registry=registry, memory=memory)
    except Exception as e:
        print(f"Initialization failure: {e}")
        return

    # Standard Interactive CLI Loop
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ['exit', 'quit']:
                print("Terminating agent runtime session. Goodbye.")
                break
                
            if not user_input.strip():
                continue

            print("Agent is reasoning...")
            response = agent.run(user_input)
            print(f"Agent: {response}\n")
            print("-" * 60)
            
        except KeyboardInterrupt:
            print("\nSession forcibly aborted by user action.")
            break
        except Exception as e:
            print(f"\nCritical Runtime Exception Encountered: {e}\n")

if __name__ == "__main__":
    main()