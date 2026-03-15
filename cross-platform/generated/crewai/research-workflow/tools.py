#!/usr/bin/env python3
"""
CrewAI tool wrappers for research-workflow.
Auto-generated from TECHKNOWMAD Universal Skill Manifest.
"""

import json
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class Design_experimentToolSchema(BaseModel):
    topic: str = Field(description="Research topic")
    hypothesis: str = Field(description="Research hypothesis")
    methodology: str = Field(description="Preferred methodology")


class Design_experimentTool(BaseTool):
    name: str = "design_experiment"
    description: str = "Design a structured experiment with hypothesis, methodology, and evaluation criteria"
    args_schema: type[BaseModel] = Design_experimentToolSchema

    def _run(self, **kwargs) -> str:
        from skills.research_workflow import execute_sync
        return json.dumps(execute_sync("design_experiment", kwargs))
