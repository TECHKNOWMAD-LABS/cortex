# multimodal-analyst

Cross-modal content analysis. Analyzes text, image, and video inputs together to produce unified analysis with per-modality and cross-modal findings.

## Tools

- **analyze_multimodal**: Perform cross-modal analysis on text, image, and video content with per-modality and synthesized findings

## Integration

### MCP Server (Claude, Copilot, Cursor, Windsurf, VS Code, JetBrains)
```bash
cd mcp/multimodal-analyst && uv run python server.py
```

### LangChain / LangGraph
```python
from langchain.multimodal_analyst.tools import get_all_tools
tools = get_all_tools()
```

### CrewAI
```python
from crewai.multimodal_analyst.tools import *
```

### OpenAI Custom GPT
Import `openai/multimodal-analyst/openapi.json` as a GPT Action.

## License

MIT — TECHKNOWMAD LABS
