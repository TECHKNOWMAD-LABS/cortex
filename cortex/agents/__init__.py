"""Multi-Agent Runtime — Orchestration, debate, and research automation.

Provides agent pipelines, multi-agent debate for improved reasoning,
task graph execution, and automated research workflows.
"""

from cortex.agents.base_agent import AgentResponse, BaseAgent
from cortex.agents.debate import DebateArena
from cortex.agents.orchestrator import AgentOrchestrator
from cortex.agents.research_engine import ResearchEngine
from cortex.agents.task_graph import TaskGraph, TaskNode

__all__ = [
    "BaseAgent",
    "AgentResponse",
    "AgentOrchestrator",
    "DebateArena",
    "TaskGraph",
    "TaskNode",
    "ResearchEngine",
]
