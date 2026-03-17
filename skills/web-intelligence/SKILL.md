# web-intelligence

## Purpose
Web page extraction, crawling, and stealth scraping via Scrapling. Provides structured data extraction from web pages with three operating modes.

## BettaFish Engine Type
`web_extraction`

## Phase
Phase 15 — Scrapling-powered web intelligence

## Architecture
- **Extract mode**: Single URL to structured JSON (title, body text, metadata, links, images count, word count, language hint).
- **Crawl mode**: Seed URL with breadth-first traversal up to configurable page count and depth. Respects robots.txt.
- **Stealth mode**: Uses Scrapling's StealthyFetcher for JavaScript-rendered or bot-protected pages.

## CLI Usage
```bash
# Extract a single page
python scripts/web_intel.py --mode extract --url https://example.com --format json

# Crawl from a seed URL
python scripts/web_intel.py --mode crawl --url https://example.com --max-pages 10 --max-depth 2

# Stealth extraction
python scripts/web_intel.py --mode stealth --url https://example.com --output result.json
```

## Input
- `--mode`: One of `extract`, `crawl`, `stealth` (required)
- `--url`: Target URL, must be http or https (required)
- `--output`: Output file path (optional, defaults to stdout)
- `--max-pages`: Max pages to crawl, crawl mode only (default 10)
- `--max-depth`: Max link depth, crawl mode only (default 2)
- `--timeout`: Request timeout in seconds (default 15)
- `--format`: Output format, `json` or `jsonl` (default json)

## Output Schema (JSON) — Extract Mode
```json
{
  "url": "https://example.com",
  "title": "Page Title",
  "body_text": "Extracted text content...",
  "metadata": {"description": "...", "keywords": "..."},
  "links": ["https://..."],
  "images_count": 5,
  "word_count": 1234,
  "language_hint": "en",
  "extracted_at": "ISO-8601"
}
```

## Security
- URLs validated: only http/https schemes accepted.
- Page content capped at 50KB per page.
- Script and style tags stripped before text extraction.
- No `pickle`, `eval()`, or `exec()` anywhere.
- All user input sanitized and length-limited.
