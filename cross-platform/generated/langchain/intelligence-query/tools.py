#!/usr/bin/env python3
"""
LangChain tool wrappers for intelligence-query.
Auto-generated from TECHKNOWMAD Universal Skill Manifest.
"""

import json
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool


class Query_intelligenceToolInput(BaseModel):
    query: str = Field(description="Intelligence query to execute")
    sources: list[str] = Field(default=[], description="List of sources to query")
    depth: str = Field(default="deep", description="Analysis depth level")


class Query_intelligenceTool(BaseTool):
    name: str = "query_intelligence"
    description: str = "Query knowledge base for evidence, cross-reference sources, flag contradictions"
    args_schema: type[BaseModel] = Query_intelligenceToolInput

    def _run(self, **kwargs) -> str:
        from skills.intelligence_query import execute_sync

        return json.dumps(execute_sync("query_intelligence", kwargs))

    async def _arun(self, **kwargs) -> str:
        from skills.intelligence_query import execute

        result = await execute("query_intelligence", kwargs)
        return json.dumps(result)


def get_all_tools() -> list[BaseTool]:
    """Return all tools for this skill."""
    return [Query_intelligenceTool()]
