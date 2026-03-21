# socrates-ai-langraph Library Guide

## Overview

**socrates-ai-langraph** is a framework integration that provides seamless LangGraph support for building sophisticated multi-agent workflows using Socrates AI components. It combines the power of LangGraph's graph-based workflow orchestration with Socrates' Socratic method agents.

**Current Version**: 0.1.0
**Package Name**: `socrates-ai-langraph`
**Python Support**: 3.9+
**License**: MIT
**Status**: Production Ready

## What This Library Does

socrates-ai-langraph provides:

### 1. LangGraph Integration
- StateGraph-based workflow definition
- State management with Pydantic models
- Conditional routing between agents
- Node composition and sequencing
- Event-driven state transitions

### 2. Pre-Built Agents
- **CodeAnalysisAgent** - Analyzes code for issues and improvements
- **CodeGenerationAgent** - Generates code from specifications
- **KnowledgeRetrievalAgent** - Retrieves context from knowledge bases
- Extensible agent architecture for custom agents

### 3. Event System Integration
- Emit events for all workflow operations
- Track agent execution lifecycle
- Monitor state changes
- Capture errors and failures

### 4. Type-Safe Workflows
- Pydantic models for state validation
- Type hints throughout
- IDE autocomplete support
- Compile-time error detection

## Architecture

```
socrates-ai-langraph
    │
    ├── agents/          # Pre-built agents
    ├── workflow.py      # LangGraph workflow creation
    ├── state.py         # Pydantic state models
    └── __init__.py      # Public API exports
```

## Key Classes & Types

### AgentState (Pydantic Model)
```python
from socrates_ai_langraph import AgentState

# State passed between agents
state = AgentState(
    input="Analyze this code: ...",
    messages=[],
    results={"analysis": ...},
    errors=[]
)
```

### Pre-Built Agents

#### CodeAnalysisAgent
```python
from socrates_ai_langraph import CodeAnalysisAgent

agent = CodeAnalysisAgent(
    name="analyzer",
    description="Analyzes code quality"
)

# Use in workflow
result = await agent.invoke(state)
```

#### CodeGenerationAgent
```python
from socrates_ai_langraph import CodeGenerationAgent

agent = CodeGenerationAgent(
    name="generator",
    description="Generates code from specs"
)
```

#### KnowledgeRetrievalAgent
```python
from socrates_ai_langraph import KnowledgeRetrievalAgent

agent = KnowledgeRetrievalAgent(
    name="retriever",
    description="Retrieves context from knowledge base"
)
```

### Workflow Creation
```python
from socrates_ai_langraph import create_workflow
from langgraph.graph import StateGraph, START, END

workflow = create_workflow(
    agents=[agent1, agent2, agent3],
    initial_agent=agent1,
    transitions={
        agent1: [agent2, agent3],  # Conditional routing
        agent2: [END],
        agent3: [END]
    }
)
```

## Installation

```bash
# Install from PyPI
pip install socrates-ai-langraph

# Install with optional dependencies
pip install socrates-ai-langraph[agents,rag]

# Install for development
pip install socrates-ai-langraph[dev]
```

## Quick Start

### 1. Simple Workflow
```python
from socrates_ai_langraph import (
    CodeAnalysisAgent,
    CodeGenerationAgent,
    create_workflow,
    AgentState
)
from langgraph.graph import START, END

# Create agents
analyzer = CodeAnalysisAgent(name="analyzer")
generator = CodeGenerationAgent(name="generator")

# Define workflow
workflow = create_workflow(
    agents=[analyzer, generator],
    initial_agent=analyzer,
    transitions={
        analyzer: [generator],
        generator: [END]
    }
)

# Run workflow
initial_state = AgentState(
    input="Generate Python function to sort array",
    messages=[],
    results={},
    errors=[]
)

final_state = workflow.invoke(initial_state)
print(final_state.results)
```

### 2. Conditional Routing
```python
from langgraph.graph import StateGraph, START, END
from socrates_ai_langraph import AgentState

def route_decision(state: AgentState) -> str:
    """Route based on previous results"""
    if state.results.get("needs_review"):
        return "reviewer"
    return "generator"

graph = StateGraph(AgentState)
graph.add_node("analyzer", analyzer.invoke)
graph.add_node("reviewer", reviewer.invoke)
graph.add_node("generator", generator.invoke)

graph.add_edge(START, "analyzer")
graph.add_conditional_edges("analyzer", route_decision)
graph.add_edge("reviewer", "generator")
graph.add_edge("generator", END)

workflow = graph.compile()
```

### 3. Custom Agents
```python
from socrates_ai_langraph import CodeAnalysisAgent
from socratic_core import get_logger

class CustomAgent(CodeAnalysisAgent):
    """Custom agent extending CodeAnalysisAgent"""

    async def invoke(self, state):
        logger = get_logger(__name__)
        logger.info(f"Custom agent processing: {state.input}")

        # Your custom logic
        result = await super().invoke(state)

        return result
```

## Integration with socratic-rag

Enhance knowledge retrieval with RAG:

```python
from socrates_ai_langraph import KnowledgeRetrievalAgent
from socratic_rag import RAGClient

# Initialize RAG
rag = RAGClient(
    provider="chromadb",
    collection="documentation"
)

# Create agent with RAG
retriever = KnowledgeRetrievalAgent(
    name="retriever",
    rag_client=rag
)

# Use in workflow
final_state = workflow.invoke(initial_state)
```

## Event Handling

### Emit Custom Events
```python
from socratic_core import EventEmitter, EventType

class CustomWorkflow:
    def __init__(self):
        self.emitter = EventEmitter()

    async def run(self, state):
        self.emitter.emit(EventType.AGENT_START, {
            "agent": "custom",
            "input": state.input
        })

        result = await self.process(state)

        self.emitter.emit(EventType.AGENT_COMPLETE, {
            "agent": "custom",
            "result": result
        })

        return result
```

### Listen to Events
```python
from socratic_core import EventEmitter, EventType

emitter = EventEmitter()

def on_agent_complete(event_data):
    print(f"Agent completed: {event_data}")

emitter.on(EventType.AGENT_COMPLETE, on_agent_complete)

# Now events will trigger listener
```

## State Management

### Pydantic State Validation
```python
from pydantic import Field, validator
from socrates_ai_langraph import AgentState

class CustomState(AgentState):
    """Extended state with additional fields"""

    priority: int = Field(default=1, ge=1, le=10)
    metadata: dict = Field(default_factory=dict)

    @validator('input')
    def input_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Input cannot be empty')
        return v

# Use custom state
state = CustomState(
    input="Your task",
    priority=5,
    metadata={"source": "api"}
)
```

## Configuration

### Environment Variables
```bash
# LangGraph configuration
LANGGRAPH_API_URL="http://localhost:2024"  # LangGraph Studio
LANGGRAPH_DEBUG=true

# Socrates configuration
ANTHROPIC_API_KEY="sk-..."
SOCRATES_DATA_DIR="/data/socrates"
LOG_LEVEL="INFO"

# RAG configuration (if using socratic-rag)
RAG_PROVIDER="chromadb"
RAG_COLLECTION="default"
```

### Programmatic Configuration
```python
from socrates_ai_langraph import create_workflow

workflow = create_workflow(
    agents=[...],
    config={
        "debug": True,
        "timeout": 300,
        "max_retries": 3,
        "emit_events": True
    }
)
```

## Advanced Usage

### Streaming Results
```python
# Stream workflow results
for state in workflow.stream(initial_state):
    print(f"Agent: {state.get('current_agent')}")
    print(f"Results: {state.get('results')}")
```

### Debugging Workflows
```python
# Enable debug mode
workflow = create_workflow(
    agents=[...],
    config={"debug": True}
)

# With LangGraph Studio
# Open http://localhost:2024 to visualize workflow
```

### Error Handling
```python
try:
    final_state = workflow.invoke(initial_state)
except Exception as e:
    logger = get_logger(__name__)
    logger.error(f"Workflow failed: {e}")

    # Access error details
    if hasattr(e, 'agent'):
        print(f"Failed in agent: {e.agent}")
```

### Timeout Handling
```python
import asyncio

# Set workflow timeout
task = workflow.invoke_async(initial_state)
try:
    result = await asyncio.wait_for(task, timeout=30)
except asyncio.TimeoutError:
    logger.error("Workflow timed out after 30 seconds")
```

## Testing

### Unit Testing Agents
```python
import pytest
from socrates_ai_langraph import CodeAnalysisAgent, AgentState

@pytest.fixture
def analyzer():
    return CodeAnalysisAgent(name="test_analyzer")

@pytest.mark.asyncio
async def test_code_analysis(analyzer):
    state = AgentState(
        input="def foo(): pass",
        messages=[],
        results={},
        errors=[]
    )

    result = await analyzer.invoke(state)

    assert result.results is not None
    assert len(result.errors) == 0
```

### Integration Testing Workflows
```python
import pytest
from socrates_ai_langraph import create_workflow

@pytest.mark.asyncio
async def test_workflow():
    workflow = create_workflow(agents=[...])

    state = AgentState(input="Test input")
    final_state = workflow.invoke(state)

    assert "output" in final_state.results
```

## Performance Optimization

### Parallel Agent Execution
```python
from langgraph.graph import StateGraph, START, END

graph = StateGraph(AgentState)

# Add multiple agents at same level for parallel execution
graph.add_node("agent1", agent1.invoke)
graph.add_node("agent2", agent2.invoke)

graph.add_edge(START, "agent1")
graph.add_edge(START, "agent2")
graph.add_edge("agent1", END)
graph.add_edge("agent2", END)

workflow = graph.compile()
```

### Caching State
```python
# Results are cached between agent calls
# Clear cache if needed
workflow.cache.clear()

# Check cache hit rate
hit_rate = workflow.cache.hit_rate()
print(f"Cache hit rate: {hit_rate:.2%}")
```

## Deployment

### As a Microservice
```python
from fastapi import FastAPI
from socrates_ai_langraph import create_workflow

app = FastAPI()
workflow = create_workflow(agents=[...])

@app.post("/workflow")
async def run_workflow(input_data: dict):
    state = AgentState(input=input_data["prompt"])
    result = workflow.invoke(state)
    return result.model_dump()
```

### With Docker
```dockerfile
FROM python:3.11

WORKDIR /app
COPY . .

RUN pip install -e .

CMD ["python", "-m", "socrates_ai_langraph.server"]
```

### With Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: socrates-langraph
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: workflow
        image: socrates-ai-langraph:latest
        env:
        - name: ANTHROPIC_API_KEY
          valueFrom:
            secretKeyRef:
              name: socrates-secrets
              key: api-key
```

## Troubleshooting

### Workflow Not Routing Correctly
```python
def debug_route(state):
    """Debug routing decision"""
    print(f"State results: {state.results}")
    print(f"State errors: {state.errors}")

    decision = "next_agent" if condition else "other_agent"
    print(f"Routing to: {decision}")
    return decision

# Use debug_route in conditional edges
```

### Agent Timeout
```python
# Increase timeout
workflow = create_workflow(
    agents=[...],
    config={"timeout": 600}  # 10 minutes
)

# Or per-agent
agent.config = {"timeout": 300}
```

### Memory Issues with Large States
```python
# Clear unnecessary data
state.messages = []  # Clear message history
state.results = {}   # Clear intermediate results

# Or limit state size
workflow.config["max_state_size"] = 10_000_000  # 10MB
```

## Version History

### v0.1.0 (Current)
- LangGraph integration
- Pre-built agents (CodeAnalysis, CodeGeneration, KnowledgeRetrieval)
- State management with Pydantic
- Event system integration
- Conditional routing
- Type-safe workflows

## Contributing

When extending socrates-ai-langraph:
1. Create new agents extending base Agent class
2. Add tests for new agents
3. Update state models if needed
4. Document new functionality
5. Maintain backward compatibility

## Related Documentation

- [Socrates Ecosystem Architecture](../../docs/SOCRATES_ECOSYSTEM_ARCHITECTURE.md)
- [LangGraph Documentation](https://python.langchain.com/docs/langgraph/)
- [Socratic Agents Guide](https://github.com/Nireus79/Socrates/tree/main/docs)

## Support

For issues or questions:
- GitHub Issues: https://github.com/Nireus79/Socrates-ai-langraph/issues
- Documentation: https://github.com/Nireus79/Socrates-ai-langraph/tree/main/docs
- Discussions: https://github.com/Nireus79/Socrates-ai-langraph/discussions
