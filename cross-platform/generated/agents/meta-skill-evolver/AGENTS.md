# meta-skill-evolver

Evolutionary skill improvement and mutation engine. Analyzes skill performance and generates improved variants.

## Tools

- **evolve_skill**: Analyze skill performance and generate improved variants through mutation

## Integration

### MCP Server (Claude, Copilot, Cursor, Windsurf, VS Code, JetBrains)
```bash
cd mcp/meta-skill-evolver && uv run python server.py
```

### LangChain / LangGraph
```python
from langchain.meta_skill_evolver.tools import get_all_tools
tools = get_all_tools()
```

### CrewAI
```python
from crewai.meta_skill_evolver.tools import *
```

### OpenAI Custom GPT
Import `openai/meta-skill-evolver/openapi.json` as a GPT Action.

## License

MIT — TECHKNOWMAD LABS
