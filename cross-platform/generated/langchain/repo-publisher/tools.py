#!/usr/bin/env python3
"""
LangChain tool wrappers for repo-publisher.
Auto-generated from TECHKNOWMAD Universal Skill Manifest.
"""

import json
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool

class Publish_repoToolInput(BaseModel):
    repo_path: str = Field(description="Path to repository")
    target: str = Field(description="GitHub target (owner/repo)")
    dry_run: bool = Field(description="Run checks without publishing")


class Publish_repoTool(BaseTool):
    name: str = "publish_repo"
    description: str = "Run pre-publish checks and prepare repo for GitHub publication"
    args_schema: type[BaseModel] = Publish_repoToolInput

    def _run(self, **kwargs) -> str:
        from skills.repo_publisher import execute_sync
        return json.dumps(execute_sync("publish_repo", kwargs))

    async def _arun(self, **kwargs) -> str:
        from skills.repo_publisher import execute
        result = await execute("publish_repo", kwargs)
        return json.dumps(result)


def get_all_tools() -> list[BaseTool]:
    """Return all tools for this skill."""
    return [Publish_repoTool()]
