# Adaptive AI Agent Framework (CLI)

This project implements an adaptive Personal Assistant AI agent utilizing the modern `google-genai` SDK. The architecture moves entirely away from monolithic procedural code, strictly adhering to established Software Engineering design patterns and SOLID principles.

## Software Architecture & Design Patterns

The core focus of this implementation is modularity, extensibility, and strict separation of concerns.

### 1. Strategy Pattern (GoF)

All external capabilities provided to the agent are decoupled into interchangeable algorithms. By inheriting from the abstract `BaseTool` class, each individual tool, such as `CalculatorTool` and `CurrencyConverterTool`, encapsulates its own business logic and JSON declaration schema.

The agent dynamically executes the required tool strategy at runtime based on the LLM's automated decisions.

### 2. Factory / Registry Pattern (GoF)

To prevent dirty and non-scalable `if-else` blocks inside the core execution loop, a centralized `ToolRegistry` is implemented.

Tools register themselves into a lookup dictionary at runtime. The registry exposes methods to compile all active schemas for API consumption and safely dispatches arguments to execute the respective components.

### 3. Separation of Concerns & SRP (SOLID)

The project follows the Single Responsibility Principle by separating responsibilities into dedicated components.

* **`MemoryManager`:** Holds the single responsibility of capturing, formatting, and persisting the sequential multi-turn conversation state. It is entirely decoupled from the generation logic.
* **`GeminiAgent`:** Holds the single responsibility of driving the sequential orchestration loop, generating content payloads, parsing responses, and handling fallback states.

### 4. Open/Closed Principle (OCP) & Dependency Inversion Principle (DIP)

The core `GeminiAgent` never references a concrete tool class directly. Instead, it relies strictly on the abstract `BaseTool` interface.

As a result, developers can introduce additional custom external tools to expand the agent's capabilities without modifying the orchestrator class. This supports the Open/Closed Principle by allowing extension without changing existing core logic.

---

## The Agent Loop (ReAct Pattern)

The system executes an autonomous **Reason → Act → Observe** flow up to a configurable maximum execution turn boundary.

1. **Receive:** The agent accepts natural language prompts from the user interface.
2. **Reason:** The conversational context and active tools are compiled and sent to `gemini-2.5-flash`. The model autonomously decides whether it can answer directly or requires programmatic tools.
3. **Act:** If a tool call is requested, the orchestrator triggers the specific runtime object through the registry boundary.
4. **Observe:** The execution output string is collected, formatted alongside the call parameters, and reinjected back into the session memory block.
5. **Resolve:** The loop runs iteratively until the model yields a final conclusive text response, which is then exposed to the CLI layer.

---

## Environment Setup & Installation

### 1. Install Workspace Dependencies

Ensure Python 3.10+ is running locally. Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

### 2. Configure the Gemini API Key

The agent dynamically fetches validation tokens through the operating system environment variable mapping layer.

Configure your runtime variable in your terminal before launching the program.

#### Windows Command Prompt CMD

```dos
set GEMINI_API_KEY="your_actual_api_studio_key_here"
```

#### macOS / Linux Terminal

```bash
export GEMINI_API_KEY="your_actual_api_studio_key_here"
```

> Tip: Make sure you do not include unnecessary brackets or trailing spaces around your actual API key when setting up the environment variable.

### 3. Execute the Application

Boot the interactive Command Line Interface session by launching the entrypoint module:

```bash
python main.py
```

---

## Robustness & Test Cases

The architecture implements robust error boundaries to handle runtime mutations, invalid argument shapes injected by the model, missing endpoints, or unexpected tool execution failures.

You can test the autonomous capability using the following prompt inputs inside the running CLI.

### Turn Test A: Single Direct Turn Execution

**Input:**

```text
Hello! Can you summarize what your primary system capabilities are?
```

**Expected Result:**

The agent bypasses external programmatic routes entirely and responds immediately with plain natural language.

---

### Turn Test B: Multi-Turn Composite ReAct Loop

**Input:**

```text
What is the current time and what is 542 multiplied by 13?
```

**Expected Result:**

The system triggers sequential agent reasoning steps. It calls `get_current_time`, collects the system time observation, proceeds to execute the calculator for the multiplication operation, tracks both actions inside the session history, and provides a unified conclusive summary.

---

### Turn Test C: Custom Structural Extensions

**Input:**

```text
Can you convert 100 EUR to TRY currency and generate expert software advice?
```

**Expected Result:**

This validates the integration paths of the custom modules, including `CurrencyConverterTool` and `AdviceGeneratorTool`, while handling multiple custom data payloads safely.

---

## Key Features

* Modular AI agent architecture
* CLI-based user interaction
* Gemini API integration through the modern `google-genai` SDK
* Tool-based reasoning and execution
* ReAct-inspired Reason → Act → Observe loop
* Runtime tool registry
* Multi-turn memory handling
* SOLID-oriented structure
* Easily extendable custom tools

---

## Extending the Agent

To add a new tool, create a new class that inherits from `BaseTool`.

Each tool should define:

* A unique tool name
* A JSON-compatible declaration schema
* Its own execution logic

After the tool is implemented, it can be registered inside the `ToolRegistry`. The agent can then access it dynamically without requiring changes inside the main orchestration loop.

---

## Notes

This project is designed as a clean and extendable software engineering implementation of an adaptive AI assistant. Its main goal is not only to run Gemini-based conversations, but also to demonstrate scalable architecture, design patterns, and maintainable code organization.

The system can be improved further by adding persistent storage, a graphical interface, more external APIs, authentication, logging, or advanced tool validation.
