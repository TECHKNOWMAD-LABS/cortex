#!/usr/bin/env python3
"""
CrewAI tool wrappers for mindspider-connector.
Auto-generated from TECHKNOWMAD Universal Skill Manifest.
"""

import json
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


class Fetch_topicsToolSchema(BaseModel):
    source: str = Field(default="demo", description="Data source to use")
    platforms: list[str] = Field(default=[], description="List of social platforms to monitor")


class Fetch_topicsTool(BaseTool):
    name: str = "fetch_topics"
    description: str = "Pull trending topics from social platforms with sentiment analysis"
    args_schema: type[BaseModel] = Fetch_topicsToolSchema

    def _run(self, **kwargs) -> str:
        from skills.mindspider_connector import execute_sync

        return json.dumps(execute_sync("fetch_topics", kwargs))
