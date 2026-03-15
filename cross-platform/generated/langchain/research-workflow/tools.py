#!/usr/bin/env python3
"""
LangChain tool wrappers for research-workflow.
Auto-generated from TECHKNOWMAD Universal Skill Manifest.
"""

import json
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool

class Design_experimentToolInput(BaseModel):
    topic: str = Field(description="Research topic")
    hypothesis: str = Field(description="Research hypothesis")
    methodology: str = Field(description="Preferred methodology")


class Design_experimentTool(BaseTool):
    name: str = "design_experiment"
    description: str = "Design a structured experiment with hypothesis, methodology, and evaluation criteria"
    args_schema: type[BaseModel] = Design_experimentToolInput

    def _run(self, **kwargs) -> str:
        from skills.research_workflow import execute_sync
        return json.dumps(execute_sync("design_experiment", kwargs))

    async def _arun(self, **kwargs) -> str:
        from skills.research_workflow import execute
        result = await execute("design_experiment", kwargs)
        return json.dumps(result)


def get_all_tools() -> list[BaseTool]:
    """Return all tools for this skill."""
    return [Design_experimentTool()]
