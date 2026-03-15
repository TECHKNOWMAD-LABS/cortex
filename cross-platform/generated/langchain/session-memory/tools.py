#!/usr/bin/env python3
"""
LangChain tool wrappers for session-memory.
Auto-generated from TECHKNOWMAD Universal Skill Manifest.
"""

import json
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool

class Session_operationToolInput(BaseModel):
    operation: str = Field(description="Operation: save, load, list, clear")
    session_id: str = Field(description="Session identifier")
    data: dict = Field(description="Data to persist")


class Session_operationTool(BaseTool):
    name: str = "session_operation"
    description: str = "Store or retrieve session-scoped memory"
    args_schema: type[BaseModel] = Session_operationToolInput

    def _run(self, **kwargs) -> str:
        from skills.session_memory import execute_sync
        return json.dumps(execute_sync("session_operation", kwargs))

    async def _arun(self, **kwargs) -> str:
        from skills.session_memory import execute
        result = await execute("session_operation", kwargs)
        return json.dumps(result)


def get_all_tools() -> list[BaseTool]:
    """Return all tools for this skill."""
    return [Session_operationTool()]
