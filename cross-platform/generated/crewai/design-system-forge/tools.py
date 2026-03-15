#!/usr/bin/env python3
"""
CrewAI tool wrappers for design-system-forge.
Auto-generated from TECHKNOWMAD Universal Skill Manifest.
"""

import json
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class Generate_design_systemToolSchema(BaseModel):
    brand: dict = Field(description="Brand configuration (colors, typography)")
    framework: str = Field(description="Target framework")
    output_dir: str = Field(description="Output directory for generated files")


class Generate_design_systemTool(BaseTool):
    name: str = "generate_design_system"
    description: str = "Generate a design system with tokens, components, and documentation"
    args_schema: type[BaseModel] = Generate_design_systemToolSchema

    def _run(self, **kwargs) -> str:
        from skills.design_system_forge import execute_sync
        return json.dumps(execute_sync("generate_design_system", kwargs))
