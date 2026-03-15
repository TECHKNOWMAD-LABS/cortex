# de-slop

AI-generated writing pattern detection and removal. Scans for emoji in headers, hyperbolic language, buzzword stacking, and other LLM artifacts.

## Tools

- **scan_content**: Scan content for AI-generated writing patterns and flag violations

## Integration

### MCP Server (Claude, Copilot, Cursor, Windsurf, VS Code, JetBrains)
```bash
cd mcp/de-slop && uv run python server.py
```

### LangChain / LangGraph
```python
from langchain.de_slop.tools import get_all_tools
tools = get_all_tools()
```

### CrewAI
```python
from crewai.de_slop.tools import *
```

### OpenAI Custom GPT
Import `openai/de-slop/openapi.json` as a GPT Action.

## License

MIT — TECHKNOWMAD LABS
