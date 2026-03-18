# forum-intelligence

Forum thread analysis with coordination detection. Analyzes discussion threads for sentiment, key arguments, coordination patterns, and minority viewpoints.

## Tools

- **analyze_forum_threads**: Analyze forum threads for sentiment distribution, key arguments, coordination patterns, and minority viewpoints

## Integration

### MCP Server (Claude, Copilot, Cursor, Windsurf, VS Code, JetBrains)
```bash
cd mcp/forum-intelligence && uv run python server.py
```

### LangChain / LangGraph
```python
from langchain.forum_intelligence.tools import get_all_tools
tools = get_all_tools()
```

### CrewAI
```python
from crewai.forum_intelligence.tools import *
```

### OpenAI Custom GPT
Import `openai/forum-intelligence/openapi.json` as a GPT Action.

## License

MIT — TECHKNOWMAD LABS
