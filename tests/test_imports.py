"""Tests for Socrates AI LangGraph module."""

import pytest


def test_import_state():
    """Test that state module can be imported."""
    from socrates_ai_langraph.state import AgentState

    assert AgentState is not None


def test_import_agents():
    """Test that agents module can be imported."""
    from socrates_ai_langraph.agents import (
        BaseAgent,
        CodeAnalysisAgent,
        CodeGenerationAgent,
        KnowledgeRetrievalAgent,
    )

    assert BaseAgent is not None
    assert CodeAnalysisAgent is not None
    assert CodeGenerationAgent is not None
    assert KnowledgeRetrievalAgent is not None


def test_import_workflow():
    """Test that workflow module can be imported."""
    from socrates_ai_langraph.workflow import get_config, get_emitter

    assert get_config is not None
    assert get_emitter is not None
