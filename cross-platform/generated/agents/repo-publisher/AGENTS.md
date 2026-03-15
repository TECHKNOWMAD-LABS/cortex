# repo-publisher

Pre-publish pipeline with security scanning, AI slop detection, structure validation, and repo metadata updates.

## Tools

- **publish_repo**: Run pre-publish checks and prepare repo for GitHub publication

## Integration

### MCP Server (Claude, Copilot, Cursor, Windsurf, VS Code, JetBrains)
```bash
cd mcp/repo-publisher && uv run python server.py
```

### LangChain / LangGraph
```python
from langchain.repo_publisher.tools import get_all_tools
tools = get_all_tools()
```

### CrewAI
```python
from crewai.repo_publisher.tools import *
```

### OpenAI Custom GPT
Import `openai/repo-publisher/openapi.json` as a GPT Action.

## License

MIT — TECHKNOWMAD LABS
