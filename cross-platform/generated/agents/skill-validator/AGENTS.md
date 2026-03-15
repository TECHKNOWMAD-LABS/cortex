# skill-validator

Skill structure and manifest validation ensuring compliance with the TECHKNOWMAD skill specification.

## Tools

- **validate_skill**: Validate skill structure and manifest against specification

## Integration

### MCP Server (Claude, Copilot, Cursor, Windsurf, VS Code, JetBrains)
```bash
cd mcp/skill-validator && uv run python server.py
```

### LangChain / LangGraph
```python
from langchain.skill_validator.tools import get_all_tools
tools = get_all_tools()
```

### CrewAI
```python
from crewai.skill_validator.tools import *
```

### OpenAI Custom GPT
Import `openai/skill-validator/openapi.json` as a GPT Action.

## License

MIT — TECHKNOWMAD LABS
