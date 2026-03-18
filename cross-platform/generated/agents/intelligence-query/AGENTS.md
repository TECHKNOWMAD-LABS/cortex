# intelligence-query

Multi-source intelligence analysis engine. Decomposes queries into sub-queries, collects evidence from multiple sources, and synthesizes intelligence reports with confidence scoring.

## Tools

- **intelligence_query**: Execute a multi-source intelligence query with automatic decomposition, evidence collection, and synthesis

## Integration

### MCP Server (Claude, Copilot, Cursor, Windsurf, VS Code, JetBrains)
```bash
cd mcp/intelligence-query && uv run python server.py
```

### LangChain / LangGraph
```python
from langchain.intelligence_query.tools import get_all_tools
tools = get_all_tools()
```

### CrewAI
```python
from crewai.intelligence_query.tools import *
```

### OpenAI Custom GPT
Import `openai/intelligence-query/openapi.json` as a GPT Action.

## License

MIT — TECHKNOWMAD LABS
