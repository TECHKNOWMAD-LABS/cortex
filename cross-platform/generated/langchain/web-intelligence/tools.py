#!/usr/bin/env python3
"""
LangChain tool wrappers for web-intelligence.
Auto-generated from TECHKNOWMAD Universal Skill Manifest.
"""

import json
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool


class Web_sweepToolInput(BaseModel):
    topic: str = Field(description="Topic to sweep the web for")
    sources: list[str] = Field(default=[], description="List of sources to sweep")
    live: bool = Field(default=False, description="Enable live web scraping")


class Web_sweepTool(BaseTool):
    name: str = "web_sweep"
    description: str = "Run live web intelligence sweep combining social, academic, and forum signals"
    args_schema: type[BaseModel] = Web_sweepToolInput

    def _run(self, **kwargs) -> str:
        from skills.web_intelligence import execute_sync

        return json.dumps(execute_sync("web_sweep", kwargs))

    async def _arun(self, **kwargs) -> str:
        from skills.web_intelligence import execute

        result = await execute("web_sweep", kwargs)
        return json.dumps(result)


def get_all_tools() -> list[BaseTool]:
    """Return all tools for this skill."""
    return [Web_sweepTool()]
