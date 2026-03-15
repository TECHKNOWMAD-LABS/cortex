#!/usr/bin/env python3
"""
LangChain tool wrappers for diff-generator.
Auto-generated from TECHKNOWMAD Universal Skill Manifest.
"""

import json
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool

class Generate_diffToolInput(BaseModel):
    original: str = Field(description="Original content")
    modified: str = Field(description="Modified content")
    format: str = Field(description="Output format")


class Generate_diffTool(BaseTool):
    name: str = "generate_diff"
    description: str = "Generate structured diff between two versions of content"
    args_schema: type[BaseModel] = Generate_diffToolInput

    def _run(self, **kwargs) -> str:
        from skills.diff_generator import execute_sync
        return json.dumps(execute_sync("generate_diff", kwargs))

    async def _arun(self, **kwargs) -> str:
        from skills.diff_generator import execute
        result = await execute("generate_diff", kwargs)
        return json.dumps(result)


def get_all_tools() -> list[BaseTool]:
    """Return all tools for this skill."""
    return [Generate_diffTool()]
