# mindspider-connector

MindSpider social listening connector. Pulls trending topics, sentiment scores, and sample posts from a MindSpider deployment and transforms them into Cortex-native evidence structures.

## Tools

- **mindspider_extract**: Extract trending topics and sentiment data from a MindSpider deployment or demo source

## Integration

### MCP Server (Claude, Copilot, Cursor, Windsurf, VS Code, JetBrains)
```bash
cd mcp/mindspider-connector && uv run python server.py
```

### LangChain / LangGraph
```python
from langchain.mindspider_connector.tools import get_all_tools
tools = get_all_tools()
```

### CrewAI
```python
from crewai.mindspider_connector.tools import *
```

### OpenAI Custom GPT
Import `openai/mindspider-connector/openapi.json` as a GPT Action.

## License

MIT — TECHKNOWMAD LABS
