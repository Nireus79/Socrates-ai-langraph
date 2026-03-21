"""LangGraph workflow creation and management."""

from typing import Optional
from langgraph.graph import StateGraph, START, END
from socratic_core import SocratesConfig, EventEmitter, EventType

from .state import AgentState
from .agents import CodeAnalysisAgent, CodeGenerationAgent, KnowledgeRetrievalAgent

# Global config and emitter
_config: Optional[SocratesConfig] = None
_emitter: Optional[EventEmitter] = None


def get_config() -> SocratesConfig:
    """Get or create global Socrates config."""
    global _config
    if _config is None:
        _config = SocratesConfig.from_env()
    return _config


def get_emitter() -> EventEmitter:
    """Get or create global event emitter."""
    global _emitter
    if _emitter is None:
        _emitter = EventEmitter()
    return _emitter


def create_socrates_langgraph_workflow(
    config: Optional[SocratesConfig] = None,
) -> StateGraph:
    """Create a LangGraph workflow with Socratic agents.

    Args:
        config: Optional Socrates configuration

    Returns:
        Compiled LangGraph workflow
    """
    if config is None:
        config = get_config()

    emitter = get_emitter()

    # Create agents
    analyzer = CodeAnalysisAgent(emitter)
    generator = CodeGenerationAgent(emitter)
    retriever = KnowledgeRetrievalAgent(emitter)

    # Create graph
    workflow = StateGraph(AgentState)

    # Define nodes
    def analyze_node(state: AgentState) -> AgentState:
        """Analyze input code."""
        emitter.emit(EventType.AGENT_START, {"node": "analyze", "input_len": len(state.input)})

        result = analyzer.analyze(state.input)
        state.results["analysis"] = result
        state.messages.append(f"Analysis: {result.get('quality_score')}/10")

        return state

    def retrieve_node(state: AgentState) -> AgentState:
        """Retrieve relevant knowledge."""
        emitter.emit(EventType.AGENT_START, {"node": "retrieve", "input": state.input})

        docs = retriever.retrieve(state.input)
        state.results["knowledge"] = docs
        state.messages.append(f"Retrieved {len(docs)} documents")

        return state

    def generate_node(state: AgentState) -> AgentState:
        """Generate code."""
        emitter.emit(EventType.AGENT_START, {"node": "generate", "input_len": len(state.input)})

        code = generator.generate(state.input)
        state.results["generated_code"] = code
        state.messages.append(f"Generated {len(code)} chars of code")

        return state

    def synthesize_node(state: AgentState) -> AgentState:
        """Synthesize all results."""
        emitter.emit(
            EventType.SYSTEM_INITIALIZED,
            {"node": "synthesize", "results": list(state.results.keys())},
        )

        state.messages.append("Synthesis complete")
        return state

    # Define routing function
    def route_analysis(state: AgentState) -> str:
        """Decide next step based on analysis."""
        if "analysis" in state.results:
            issues = state.results["analysis"].get("issues", [])
            if issues:
                return "retrieve_knowledge"
        return "synthesize"

    # Add nodes
    workflow.add_node("analyze", analyze_node)
    workflow.add_node("retrieve_knowledge", retrieve_node)
    workflow.add_node("generate", generate_node)
    workflow.add_node("synthesize", synthesize_node)

    # Add edges
    workflow.add_edge(START, "analyze")
    workflow.add_conditional_edges("analyze", route_analysis)
    workflow.add_edge("retrieve_knowledge", "generate")
    workflow.add_edge("generate", "synthesize")
    workflow.add_edge("synthesize", END)

    return workflow
