#!/usr/bin/env python3
"""
CrewAI tool wrappers for agent-output-validator.
Auto-generated from TECHKNOWMAD Universal Skill Manifest.
"""

import json
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class Validate_outputToolSchema(BaseModel):
    output: str = Field(description="Agent output to validate")
    schema: dict = Field(description="Expected output schema")
    quality_threshold: float = Field(description="Minimum quality score (0-1)")


class Validate_outputTool(BaseTool):
    name: str = "validate_output"
    description: str = "Validate agent output against quality gates and schema"
    args_schema: type[BaseModel] = Validate_outputToolSchema

    def _run(self, **kwargs) -> str:
        from skills.agent_output_validator import execute_sync
        return json.dumps(execute_sync("validate_output", kwargs))
