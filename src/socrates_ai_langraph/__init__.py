"""
Socrates AI LangGraph Integration

Framework-agnostic Socratic AI agent integration for LangGraph.

Usage:
    from socrates_ai_langraph import create_socrates_langgraph_workflow

    workflow = create_socrates_langgraph_workflow()
    app = workflow.compile()
    result = app.invoke(initial_state)
"""

from .state import AgentState
from .workflow import create_socrates_langgraph_workflow, get_config
from .agents import CodeAnalysisAgent, CodeGenerationAgent, KnowledgeRetrievalAgent

__version__ = "0.1.0"
__all__ = [
    "AgentState",
    "create_socrates_langgraph_workflow",
    "get_config",
    "CodeAnalysisAgent",
    "CodeGenerationAgent",
    "KnowledgeRetrievalAgent",
]
