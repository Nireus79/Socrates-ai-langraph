"""State management for LangGraph workflows."""

from typing import Any, Dict, List
from pydantic import BaseModel, Field


class AgentState(BaseModel):
    """State passed between LangGraph nodes."""

    input: str = Field(
        description="The input to the workflow"
    )

    messages: List[str] = Field(
        default_factory=list,
        description="Messages from agents"
    )

    results: Dict[str, Any] = Field(
        default_factory=dict,
        description="Results from agents"
    )

    errors: List[str] = Field(
        default_factory=list,
        description="Errors encountered"
    )

    class Config:
        """Pydantic config."""
        arbitrary_types_allowed = True
