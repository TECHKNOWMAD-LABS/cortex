#!/usr/bin/env python3
"""
CrewAI tool wrappers for multimodal-analyst.
Auto-generated from TECHKNOWMAD Universal Skill Manifest.
"""

import json
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


class Analyze_contentToolSchema(BaseModel):
    content: str = Field(description="Content to analyze")
    content_types: list[str] = Field(default=[], description="List of content types to analyze")


class Analyze_contentTool(BaseTool):
    name: str = "analyze_content"
    description: str = "Analyze mixed-media content, detect types, synthesize findings"
    args_schema: type[BaseModel] = Analyze_contentToolSchema

    def _run(self, **kwargs) -> str:
        from skills.multimodal_analyst import execute_sync

        return json.dumps(execute_sync("analyze_content", kwargs))
