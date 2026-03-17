#!/usr/bin/env python3
"""
LangChain tool wrappers for mindspider-connector.
Auto-generated from TECHKNOWMAD Universal Skill Manifest.
"""

import json
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool


class Fetch_topicsToolInput(BaseModel):
    source: str = Field(default="demo", description="Data source to use")
    platforms: list[str] = Field(default=[], description="List of social platforms to monitor")


class Fetch_topicsTool(BaseTool):
    name: str = "fetch_topics"
    description: str = "Pull trending topics from social platforms with sentiment analysis"
    args_schema: type[BaseModel] = Fetch_topicsToolInput

    def _run(self, **kwargs) -> str:
        from skills.mindspider_connector import execute_sync

        return json.dumps(execute_sync("fetch_topics", kwargs))

    async def _arun(self, **kwargs) -> str:
        from skills.mindspider_connector import execute

        result = await execute("fetch_topics", kwargs)
        return json.dumps(result)


def get_all_tools() -> list[BaseTool]:
    """Return all tools for this skill."""
    return [Fetch_topicsTool()]
