> **Proof of concept, not a product.** This library belongs to the earlier Python research prototype ([Socrates](https://github.com/Nireus79/Socrates)) and is not maintained as a product. The current products are listed at [nireus79.github.io](https://nireus79.github.io/). Contact: Hermes_creative@proton.me.

# Socrates AI LangGraph Integration

**Framework-agnostic Socratic AI agent integration for LangGraph**

This library provides seamless integration between Socrates AI components and LangGraph, enabling you to build sophisticated multi-agent workflows with Socratic method guidance, knowledge retrieval, and unified event management.

## Features

🤖 **LangGraph Integration** - Build workflows with Socratic agents as LangGraph nodes
📚 **Knowledge Retrieval** - Integrated RAG capabilities (optional)
🎓 **Socratic Guidance** - Ask better questions, not just provide answers
⚡ **Framework Agnostic** - Swap LangGraph for other orchestrators easily
🔄 **Event System** - Unified event handling across all agents
💾 **State Management** - Pydantic-based state with type safety

## Installation

```bash
# Core integration
pip install socrates-ai-langraph

# With agent support
pip install "socrates-ai-langraph[agents]"

# With RAG support
pip install "socrates-ai-langraph[rag]"

# Everything
pip install "socrates-ai-langraph[full]"
```

## Quick Start

```python
from langgraph.graph import StateGraph, START, END
from socrates_ai_langraph import create_socrates_langgraph_workflow, AgentState

# Create workflow
workflow = create_socrates_langgraph_workflow()
app = workflow.compile()

# Run
initial_state = AgentState(input="Help me design a REST API")
result = app.invoke(initial_state)

print(result.messages)
print(result.results)
```

## Architecture

```
LangGraph StateGraph
    ↓
├─ analyze_node         (uses CodeAnalysisAgent)
├─ retrieve_node        (uses KnowledgeRetrievalAgent)
├─ generate_node        (uses CodeGenerationAgent)
└─ synthesize_node      (aggregates results)
    ↓
Socrates Components:
├─ SocraticConfig       (unified configuration)
├─ EventEmitter         (unified events)
└─ Socratic Libraries (optional):
   ├─ socratic-agents
   ├─ socratic-rag
   └─ socratic-learning
```

## API Reference

### State Classes

#### `AgentState(BaseModel)`

```python
from socrates_ai_langraph import AgentState

state = AgentState(
    input="Your task here",
    messages=["Message 1", "Message 2"],
    results={"key": "value"},
    errors=[]
)
```

### Workflow Creation

#### `create_socrates_langgraph_workflow(config: Optional[SocratesConfig] = None) -> StateGraph`

Create a pre-configured LangGraph workflow with Socratic agents.

```python
from socrates_ai_langraph import create_socrates_langgraph_workflow

workflow = create_socrates_langgraph_workflow()
app = workflow.compile()
result = app.invoke(initial_state)
```

### Agent Classes

#### `CodeAnalysisAgent`

Analyzes code for complexity, issues, and improvements.

```python
from socrates_ai_langraph import CodeAnalysisAgent

agent = CodeAnalysisAgent()
result = agent.analyze("def example(): pass")
# Returns: {"complexity": "low", "issues": [], "suggestions": [...]}
```

#### `CodeGenerationAgent`

Generates code based on prompts.

```python
from socrates_ai_langraph import CodeGenerationAgent

agent = CodeGenerationAgent()
code = agent.generate("Create a Python function for data validation")
```

#### `KnowledgeRetrievalAgent`

Retrieves relevant knowledge (requires socratic-rag).

```python
from socrates_ai_langraph import KnowledgeRetrievalAgent

agent = KnowledgeRetrievalAgent()
docs = agent.retrieve("How to implement authentication?")
```

## Configuration

### Environment Variables

```bash
# Required for LLM features
export ANTHROPIC_API_KEY="sk-ant-..."

# Optional
export SOCRATIC_MODEL="claude-opus-4-5"
export SOCRATIC_TEMPERATURE="0.7"
```

### Programmatic Configuration

```python
from socratic_core import SocratesConfig
from socrates_ai_langraph import create_socrates_langgraph_workflow

config = SocratesConfig(
    model="claude-opus-4-5",
    temperature=0.7
)

workflow = create_socrates_langgraph_workflow(config)
```

## Advanced Usage

### Custom Workflow

```python
from langgraph.graph import StateGraph, START, END
from socrates_ai_langraph import AgentState, CodeAnalysisAgent

# Create custom workflow
workflow = StateGraph(AgentState)

# Add your nodes
def my_node(state: AgentState) -> AgentState:
    analyzer = CodeAnalysisAgent()
    state.results["analysis"] = analyzer.analyze(state.input)
    return state

workflow.add_node("analyze", my_node)
workflow.add_edge(START, "analyze")
workflow.add_edge("analyze", END)

# Compile and run
app = workflow.compile()
result = app.invoke(AgentState(input="def example(): pass"))
```

### Event Listening

```python
from socrates_core import EventType
from socrates_ai_langraph import create_socrates_langgraph_workflow, get_config

config = get_config()
workflow = create_socrates_langgraph_workflow(config)

# Listen to events
@config.emitter.on(EventType.AGENT_START)
def on_agent_start(data):
    print(f"Agent starting: {data}")

@config.emitter.on(EventType.AGENT_COMPLETE)
def on_agent_complete(data):
    print(f"Agent complete: {data}")

# Run workflow
app = workflow.compile()
result = app.invoke(initial_state)
```

## Examples

### Example 1: Code Review Workflow

```python
from socrates_ai_langraph import create_socrates_langgraph_workflow, AgentState

# Create workflow
workflow = create_socrates_langgraph_workflow()
app = workflow.compile()

# Review code
code = """
def process_data(data):
    result = []
    for item in data:
        result.append(item * 2)
    return result
"""

state = AgentState(input=code)
result = app.invoke(state)

print("Analysis:", result.results.get("analysis"))
print("Suggestions:", result.messages)
```

### Example 2: Generate and Improve

```python
from socrates_ai_langraph import CodeGenerationAgent, CodeAnalysisAgent, AgentState

# Generate code
generator = CodeGenerationAgent()
code = generator.generate("Create a fibonacci function")

# Analyze it
analyzer = CodeAnalysisAgent()
analysis = analyzer.analyze(code)

# Improve based on feedback
state = AgentState(
    input=f"Improve this code based on: {analysis['suggestions']}",
    results={"original_code": code, "analysis": analysis}
)
```

## Comparison with Other Frameworks

| Feature | LangGraph | Openclaw | CrewAI | AutoGen |
|---------|-----------|----------|--------|---------|
| **Socratic Method** | ✅ Via socrates-ai-langraph | ✅ Built-in | ❌ | ❌ |
| **RAG Support** | ✅ Optional | ✅ Built-in | ✅ | ❌ |
| **State Management** | ✅ Pydantic | ⚠️ Custom | ⚠️ Custom | ❌ |
| **Async Support** | ✅ Full | ✅ Full | ✅ Full | ⚠️ Limited |
| **Framework Agnostic** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Type Safe** | ✅ Yes | ⚠️ Partial | ❌ No | ❌ No |

## Migration

### From langgraph-socrates (if exists)

```python
# Old import
from langgraph_socrates import create_workflow

# New import (if different)
from socrates_ai_langraph import create_socrates_langgraph_workflow
```

### From Direct LangGraph (without Socratic)

```python
# Before: Custom agent implementation
class MyAgent:
    def run(self, input_data):
        # Custom implementation
        pass

# After: Use built-in Socratic agents
from socrates_ai_langraph import CodeAnalysisAgent
agent = CodeAnalysisAgent()
result = agent.analyze(input_data)
```

## Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=socrates_ai_langraph

# Specific test
pytest tests/test_agents.py -v
```

## Troubleshooting

### Import Errors

```python
# Error: ModuleNotFoundError: No module named 'langgraph'
# Solution:
pip install langgraph

# Error: ModuleNotFoundError: No module named 'socratic_core'
# Solution:
pip install socratic-core
```

### Agent Not Initialized

```python
# Error: Agent has no attribute 'run'
# Solution: Make sure to initialize config first
from socrates_ai_langraph import create_socrates_langgraph_workflow
workflow = create_socrates_langgraph_workflow()
```

### State Serialization

```python
# Use Pydantic models for all state
from socrates_ai_langraph import AgentState

# ✅ Good
state = AgentState(input="...", results={"key": "value"})

# ❌ Bad
state = {"input": "...", "results": {"key": "value"}}
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Write tests
4. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Support

- **GitHub Issues**: [Report bugs](https://github.com/Nireus79/Socrates/issues)
- **Discussions**: [Ask questions](https://github.com/Nireus79/Socrates/discussions)
- **Documentation**: [Full docs](docs/)
- **Email**: Hermes_creative@proton.me

## License

MIT License - see [LICENSE](LICENSE) file

## Acknowledgments

Built with:
- [LangGraph](https://langchain-ai.github.io/langgraph/) - Graph-based orchestration
- [socratic-core](https://pypi.org/project/socratic-core/) - Foundation framework
- [Anthropic Claude](https://anthropic.com) - LLM
- Socratic method philosophy

---

**Made with ❤️ for developers who believe in learning through questions**
