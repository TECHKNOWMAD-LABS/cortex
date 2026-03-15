#!/usr/bin/env python3
"""
LangChain tool wrappers for persistent-memory.
Auto-generated from TECHKNOWMAD Universal Skill Manifest.
"""

import json
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool

class Memory_operationToolInput(BaseModel):
    operation: str = Field(description="Operation: store, retrieve, search, delete")
    key: str = Field(description="Memory key")
    value: str = Field(description="Value to store")
    query: str = Field(description="Search query for FTS5")


class Memory_operationTool(BaseTool):
    name: str = "memory_operation"
    description: str = "Store, retrieve, or search persistent memory entries"
    args_schema: type[BaseModel] = Memory_operationToolInput

    def _run(self, **kwargs) -> str:
        from skills.persistent_memory import execute_sync
        return json.dumps(execute_sync("memory_operation", kwargs))

    async def _arun(self, **kwargs) -> str:
        from skills.persistent_memory import execute
        result = await execute("memory_operation", kwargs)
        return json.dumps(result)


def get_all_tools() -> list[BaseTool]:
    """Return all tools for this skill."""
    return [Memory_operationTool()]
