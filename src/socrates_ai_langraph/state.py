"""State management for LangGraph workflows."""

from typing import Any, Dict, List
from pydantic import BaseModel, Field, ConfigDict


class AgentState(BaseModel):
    """State passed between LangGraph nodes."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    input: str = Field(description="The input to the workflow")

    messages: List[str] = Field(default_factory=list, description="Messages from agents")

    results: Dict[str, Any] = Field(default_factory=dict, description="Results from agents")

    errors: List[str] = Field(default_factory=list, description="Errors encountered")
