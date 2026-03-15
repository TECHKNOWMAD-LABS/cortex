#!/usr/bin/env python3
"""
CrewAI tool wrappers for tdd-enforcer.
Auto-generated from TECHKNOWMAD Universal Skill Manifest.
"""

import json
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class Enforce_tddToolSchema(BaseModel):
    project_path: str = Field(description="Path to project")
    coverage_threshold: float = Field(description="Minimum coverage percentage")
    strict: bool = Field(description="Block commits without tests")


class Enforce_tddTool(BaseTool):
    name: str = "enforce_tdd"
    description: str = "Enforce TDD workflow with coverage tracking and cycle validation"
    args_schema: type[BaseModel] = Enforce_tddToolSchema

    def _run(self, **kwargs) -> str:
        from skills.tdd_enforcer import execute_sync
        return json.dumps(execute_sync("enforce_tdd", kwargs))
