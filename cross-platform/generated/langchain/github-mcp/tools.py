#!/usr/bin/env python3
"""
LangChain tool wrappers for github-mcp.
Auto-generated from TECHKNOWMAD Universal Skill Manifest.
"""

import json
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool

class Github_operationToolInput(BaseModel):
    operation: str = Field(description="GitHub operation to perform")
    repo: str = Field(description="Repository in owner/repo format")
    params: dict = Field(description="Operation parameters")


class Github_operationTool(BaseTool):
    name: str = "github_operation"
    description: str = "Execute GitHub API operations via MCP"
    args_schema: type[BaseModel] = Github_operationToolInput

    def _run(self, **kwargs) -> str:
        from skills.github_mcp import execute_sync
        return json.dumps(execute_sync("github_operation", kwargs))

    async def _arun(self, **kwargs) -> str:
        from skills.github_mcp import execute
        result = await execute("github_operation", kwargs)
        return json.dumps(result)


def get_all_tools() -> list[BaseTool]:
    """Return all tools for this skill."""
    return [Github_operationTool()]
