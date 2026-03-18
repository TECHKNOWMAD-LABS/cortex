# web-intelligence

Web page extraction, crawling, and stealth scraping via Scrapling. Provides structured data extraction from web pages with extract, crawl, and stealth operating modes.

## Tools

- **web_extract**: Extract structured data from a web page, crawl from a seed URL, or perform stealth scraping of bot-protected pages

## Integration

### MCP Server (Claude, Copilot, Cursor, Windsurf, VS Code, JetBrains)
```bash
cd mcp/web-intelligence && uv run python server.py
```

### LangChain / LangGraph
```python
from langchain.web_intelligence.tools import get_all_tools
tools = get_all_tools()
```

### CrewAI
```python
from crewai.web_intelligence.tools import *
```

### OpenAI Custom GPT
Import `openai/web-intelligence/openapi.json` as a GPT Action.

## License

MIT — TECHKNOWMAD LABS
