# research-workflow

Experiment design and research methodology for AI/ML research projects with hypothesis generation and evaluation frameworks.

## Tools

- **design_experiment**: Design a structured experiment with hypothesis, methodology, and evaluation criteria

## Integration

### MCP Server (Claude, Copilot, Cursor, Windsurf, VS Code, JetBrains)
```bash
cd mcp/research-workflow && uv run python server.py
```

### LangChain / LangGraph
```python
from langchain.research_workflow.tools import get_all_tools
tools = get_all_tools()
```

### CrewAI
```python
from crewai.research_workflow.tools import *
```

### OpenAI Custom GPT
Import `openai/research-workflow/openapi.json` as a GPT Action.

## License

MIT — TECHKNOWMAD LABS
