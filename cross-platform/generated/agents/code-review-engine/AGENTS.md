# code-review-engine

Automated code review with security checks, style enforcement, and best practice validation.

## Tools

- **review_code**: Run automated code review on a target file or directory

## Integration

### MCP Server (Claude, Copilot, Cursor, Windsurf, VS Code, JetBrains)
```bash
cd mcp/code-review-engine && uv run python server.py
```

### LangChain / LangGraph
```python
from langchain.code_review_engine.tools import get_all_tools
tools = get_all_tools()
```

### CrewAI
```python
from crewai.code_review_engine.tools import *
```

### OpenAI Custom GPT
Import `openai/code-review-engine/openapi.json` as a GPT Action.

## License

MIT — TECHKNOWMAD LABS
