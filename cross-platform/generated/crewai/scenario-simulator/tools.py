#!/usr/bin/env python3
"""
CrewAI tool wrappers for scenario-simulator.
Auto-generated from TECHKNOWMAD Universal Skill Manifest.
"""

import json
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


class Run_scenarioToolSchema(BaseModel):
    topic: str = Field(description="Scenario topic to simulate")
    personas: int = Field(default=3, description="Number of personas to simulate")
    rounds: int = Field(default=3, description="Number of simulation rounds")


class Run_scenarioTool(BaseTool):
    name: str = "run_scenario"
    description: str = "Run multi-persona scenario simulations with counterfactual analysis"
    args_schema: type[BaseModel] = Run_scenarioToolSchema

    def _run(self, **kwargs) -> str:
        from skills.scenario_simulator import execute_sync

        return json.dumps(execute_sync("run_scenario", kwargs))
