#!/usr/bin/env python3
"""
LangChain tool wrappers for skill-validator.
Auto-generated from TECHKNOWMAD Universal Skill Manifest.
"""

import json
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool

class Validate_skillToolInput(BaseModel):
    skill_path: str = Field(description="Path to skill directory")
    strict: bool = Field(description="Enable strict validation")


class Validate_skillTool(BaseTool):
    name: str = "validate_skill"
    description: str = "Validate skill structure and manifest against specification"
    args_schema: type[BaseModel] = Validate_skillToolInput

    def _run(self, **kwargs) -> str:
        from skills.skill_validator import execute_sync
        return json.dumps(execute_sync("validate_skill", kwargs))

    async def _arun(self, **kwargs) -> str:
        from skills.skill_validator import execute
        result = await execute("validate_skill", kwargs)
        return json.dumps(result)


def get_all_tools() -> list[BaseTool]:
    """Return all tools for this skill."""
    return [Validate_skillTool()]
