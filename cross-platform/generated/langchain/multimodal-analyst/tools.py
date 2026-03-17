#!/usr/bin/env python3
"""
LangChain tool wrappers for multimodal-analyst.
Auto-generated from TECHKNOWMAD Universal Skill Manifest.
"""

import json
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool


class Analyze_contentToolInput(BaseModel):
    content: str = Field(description="Content to analyze")
    content_types: list[str] = Field(default=[], description="List of content types to analyze")


class Analyze_contentTool(BaseTool):
    name: str = "analyze_content"
    description: str = "Analyze mixed-media content, detect types, synthesize findings"
    args_schema: type[BaseModel] = Analyze_contentToolInput

    def _run(self, **kwargs) -> str:
        from skills.multimodal_analyst import execute_sync

        return json.dumps(execute_sync("analyze_content", kwargs))

    async def _arun(self, **kwargs) -> str:
        from skills.multimodal_analyst import execute

        result = await execute("analyze_content", kwargs)
        return json.dumps(result)


def get_all_tools() -> list[BaseTool]:
    """Return all tools for this skill."""
    return [Analyze_contentTool()]
