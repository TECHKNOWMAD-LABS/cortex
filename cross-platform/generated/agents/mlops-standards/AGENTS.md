# mlops-standards

ML operations best practices enforcement covering experiment tracking, model versioning, CI/CD for ML, and deployment standards.

## Tools

- **audit_mlops**: Audit ML project for MLOps standards compliance

## Integration

### MCP Server (Claude, Copilot, Cursor, Windsurf, VS Code, JetBrains)
```bash
cd mcp/mlops-standards && uv run python server.py
```

### LangChain / LangGraph
```python
from langchain.mlops_standards.tools import get_all_tools
tools = get_all_tools()
```

### CrewAI
```python
from crewai.mlops_standards.tools import *
```

### OpenAI Custom GPT
Import `openai/mlops-standards/openapi.json` as a GPT Action.

## License

MIT — TECHKNOWMAD LABS
