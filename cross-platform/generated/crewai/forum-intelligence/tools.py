#!/usr/bin/env python3
"""
CrewAI tool wrappers for forum-intelligence.
Auto-generated from TECHKNOWMAD Universal Skill Manifest.
"""

import json
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


class Analyze_threadsToolSchema(BaseModel):
    topic: str = Field(description="Topic to analyze forum threads for")
    platforms: list[str] = Field(default=[], description="List of forum platforms to analyze")
    timeframe: str = Field(default="7d", description="Timeframe for thread analysis")


class Analyze_threadsTool(BaseTool):
    name: str = "analyze_threads"
    description: str = "Analyze forum threads for viewpoints, coordination patterns, and emerging consensus"
    args_schema: type[BaseModel] = Analyze_threadsToolSchema

    def _run(self, **kwargs) -> str:
        from skills.forum_intelligence import execute_sync

        return json.dumps(execute_sync("analyze_threads", kwargs))
