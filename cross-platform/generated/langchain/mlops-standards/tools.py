#!/usr/bin/env python3
"""
LangChain tool wrappers for mlops-standards.
Auto-generated from TECHKNOWMAD Universal Skill Manifest.
"""

import json
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool

class Audit_mlopsToolInput(BaseModel):
    project_path: str = Field(description="Path to ML project")
    standards: list = Field(description="Standards to check against")
    level: str = Field(description="Maturity level to target")


class Audit_mlopsTool(BaseTool):
    name: str = "audit_mlops"
    description: str = "Audit ML project for MLOps standards compliance"
    args_schema: type[BaseModel] = Audit_mlopsToolInput

    def _run(self, **kwargs) -> str:
        from skills.mlops_standards import execute_sync
        return json.dumps(execute_sync("audit_mlops", kwargs))

    async def _arun(self, **kwargs) -> str:
        from skills.mlops_standards import execute
        result = await execute("audit_mlops", kwargs)
        return json.dumps(result)


def get_all_tools() -> list[BaseTool]:
    """Return all tools for this skill."""
    return [Audit_mlopsTool()]
