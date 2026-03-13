#!/usr/bin/env python3
"""
CrewAI tool wrappers for persistent-memory.
Auto-generated from TECHKNOWMAD Universal Skill Manifest.
"""

import json
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class MemoryOperationToolSchema(BaseModel):
    action: str = Field(description="Memory operation")
    key: str = Field(description="Memory key")
    value: dict = Field(description="Value to store")
    query: str = Field(description="Search query")
    tags: list = Field(description="Tags for filtering")
    ttl: int = Field(description="Time-to-live in seconds")


class MemoryOperationTool(BaseTool):
    name: str = "memory_operation"
    description: str = "Store, retrieve, search, or manage persistent memory entries"
    args_schema: type[BaseModel] = MemoryOperationToolSchema

    def _run(self, **kwargs) -> str:
        from skills.persistent_memory import execute_sync
        return json.dumps(execute_sync("memory_operation", kwargs))