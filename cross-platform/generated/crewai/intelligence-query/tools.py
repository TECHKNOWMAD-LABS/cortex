#!/usr/bin/env python3
"""
CrewAI tool wrappers for intelligence-query.
Auto-generated from TECHKNOWMAD Universal Skill Manifest.
"""

import json
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


class Query_intelligenceToolSchema(BaseModel):
    query: str = Field(description="Intelligence query to execute")
    sources: list[str] = Field(default=[], description="List of sources to query")
    depth: str = Field(default="deep", description="Analysis depth level")


class Query_intelligenceTool(BaseTool):
    name: str = "query_intelligence"
    description: str = "Query knowledge base for evidence, cross-reference sources, flag contradictions"
    args_schema: type[BaseModel] = Query_intelligenceToolSchema

    def _run(self, **kwargs) -> str:
        from skills.intelligence_query import execute_sync

        return json.dumps(execute_sync("query_intelligence", kwargs))
