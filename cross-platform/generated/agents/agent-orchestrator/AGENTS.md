# agent-orchestrator

Multi-agent workflow orchestration with dependency resolution, parallel execution, and fault-tolerant task routing. Coordinates complex pipelines where multiple agents collaborate on compound tasks.

## Tools

- **orchestrate_workflow**: Execute a multi-agent workflow with dependency resolution and parallel task routing

## Integration

### MCP Server (Claude, Copilot, Cursor, Windsurf, VS Code, JetBrains)
```bash
cd mcp/agent-orchestrator && uv run python server.py
```

### LangChain / LangGraph
```python
from langchain.agent_orchestrator.tools import get_all_tools
tools = get_all_tools()
```

### CrewAI
```python
from crewai.agent_orchestrator.tools import *
```

### OpenAI Custom GPT
Import `openai/agent-orchestrator/openapi.json` as a GPT Action.

## License

MIT — TECHKNOWMAD LABS