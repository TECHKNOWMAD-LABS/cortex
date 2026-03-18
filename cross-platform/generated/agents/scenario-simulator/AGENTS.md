# scenario-simulator

Swarm scenario simulation with multi-agent deliberation. Generates agent personas, runs deliberation rounds, and produces counterfactual analysis for decision support.

## Tools

- **simulate_scenario**: Run a multi-agent scenario simulation with persona generation, deliberation rounds, and counterfactual analysis

## Integration

### MCP Server (Claude, Copilot, Cursor, Windsurf, VS Code, JetBrains)
```bash
cd mcp/scenario-simulator && uv run python server.py
```

### LangChain / LangGraph
```python
from langchain.scenario_simulator.tools import get_all_tools
tools = get_all_tools()
```

### CrewAI
```python
from crewai.scenario_simulator.tools import *
```

### OpenAI Custom GPT
Import `openai/scenario-simulator/openapi.json` as a GPT Action.

## License

MIT — TECHKNOWMAD LABS
