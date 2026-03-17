"""Optional SSE dashboard server for the Cortex Research Suite.

Serves static dashboard files and provides a real-time event stream
for evolution log changes.

Features:
    - Static file serving from dashboards/ directory
    - /api/status endpoint with organism state
    - /events SSE endpoint (uvicorn mode only) watching evolution_log.jsonl
    - CORS headers for cross-origin access
    - Graceful SIGINT shutdown

Usage:
    python scripts/serve_dashboard.py

Environment:
    CORTEX_DASHBOARD_PORT - Port to listen on (default: 3117)
"""

from __future__ import annotations

import json
import os
import signal
import sys
import threading
import time
from http import HTTPStatus
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DASHBOARDS_DIR = REPO_ROOT / "dashboards"
EVOLUTION_LOG = REPO_ROOT / "skill-organism" / "evolution_log.jsonl"
DEFAULT_PORT = 3117
SSE_POLL_INTERVAL = 5


def get_port() -> int:
    """Read the dashboard port from environment or use default.

    Returns:
        The port number to bind to.
    """
    raw = os.environ.get("CORTEX_DASHBOARD_PORT", "")
    if raw.isdigit():
        return int(raw)
    return DEFAULT_PORT


def build_status() -> dict[str, Any]:
    """Build the /api/status response from the evolution log.

    Returns:
        Dictionary with organism status fields.
    """
    status: dict[str, Any] = {
        "organism_generation": 0,
        "total_skills": 0,
        "last_evolution_time": "",
        "skills_improved": 0,
        "skills_regressed": 0,
    }

    if not EVOLUTION_LOG.exists():
        return status

    entries: list[dict[str, Any]] = []
    for line in EVOLUTION_LOG.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    if not entries:
        return status

    max_gen = max(e.get("generation", 0) for e in entries)
    latest_entries = [e for e in entries if e.get("generation") == max_gen]

    status["organism_generation"] = max_gen
    status["total_skills"] = len(latest_entries)
    status["last_evolution_time"] = max(
        (e.get("timestamp", "") for e in latest_entries),
        default="",
    )
    status["skills_improved"] = sum(1 for e in latest_entries if e.get("delta", 0) > 0)
    status["skills_regressed"] = sum(1 for e in latest_entries if e.get("delta", 0) < 0)

    return status


class CortexHandler(SimpleHTTPRequestHandler):
    """HTTP handler with CORS, /api/status, and static file serving."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault("directory", str(DASHBOARDS_DIR))
        super().__init__(*args, **kwargs)

    def end_headers(self) -> None:
        """Add CORS headers to every response."""
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self) -> None:  # noqa: N802
        """Handle CORS preflight requests."""
        self.send_response(HTTPStatus.NO_CONTENT)
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        """Route GET requests."""
        if self.path == "/api/status":
            self._serve_status()
        else:
            super().do_GET()

    def _serve_status(self) -> None:
        """Serve the /api/status JSON endpoint."""
        body = json.dumps(build_status(), indent=2).encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: Any) -> None:
        """Suppress default request logging to keep output clean."""


def run_stdlib_server(port: int) -> None:
    """Run the dashboard using http.server from stdlib.

    Args:
        port: Port number to listen on.
    """
    server = HTTPServer(("0.0.0.0", port), CortexHandler)
    shutdown_event = threading.Event()

    def _handle_sigint(signum: int, frame: Any) -> None:
        print("\nShutting down dashboard server...", file=sys.stderr)
        shutdown_event.set()
        server.shutdown()

    signal.signal(signal.SIGINT, _handle_sigint)

    print(f"Cortex dashboards at http://localhost:{port}")
    print("Press Ctrl+C to stop.", file=sys.stderr)

    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    try:
        while not shutdown_event.is_set():
            shutdown_event.wait(timeout=1.0)
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()
        print("Dashboard server stopped.", file=sys.stderr)


def _try_uvicorn(port: int) -> bool:
    """Attempt to run with uvicorn for SSE support.

    Args:
        port: Port number to listen on.

    Returns:
        True if uvicorn was available and started, False otherwise.
    """
    try:
        import uvicorn  # type: ignore[import-untyped]
    except ImportError:
        return False

    import asyncio

    app = _build_asgi_app()

    print(f"Cortex dashboards at http://localhost:{port}")
    print("Running with uvicorn (SSE enabled).", file=sys.stderr)

    config = uvicorn.Config(app, host="0.0.0.0", port=port, log_level="warning")
    server = uvicorn.Server(config)

    loop = asyncio.new_event_loop()

    def _handle_sigint(signum: int, frame: Any) -> None:
        print("\nShutting down dashboard server...", file=sys.stderr)
        server.should_exit = True

    signal.signal(signal.SIGINT, _handle_sigint)

    loop.run_until_complete(server.serve())
    print("Dashboard server stopped.", file=sys.stderr)
    return True


def _build_asgi_app() -> Any:
    """Build a minimal ASGI application with SSE support.

    Returns:
        An ASGI callable.
    """
    import asyncio

    async def app(scope: dict[str, Any], receive: Any, send: Any) -> None:
        """ASGI application entry point."""
        if scope["type"] != "http":
            return

        path = scope.get("path", "/")
        method = scope.get("method", "GET")

        cors_headers = [
            (b"access-control-allow-origin", b"*"),
            (b"access-control-allow-methods", b"GET, OPTIONS"),
            (b"access-control-allow-headers", b"Content-Type"),
        ]

        if method == "OPTIONS":
            await send({"type": "http.response.start", "status": 204, "headers": cors_headers})
            await send({"type": "http.response.body", "body": b""})
            return

        if path == "/api/status":
            body = json.dumps(build_status(), indent=2).encode("utf-8")
            headers = cors_headers + [(b"content-type", b"application/json")]
            await send({"type": "http.response.start", "status": 200, "headers": headers})
            await send({"type": "http.response.body", "body": body})
            return

        if path == "/events":
            headers = cors_headers + [
                (b"content-type", b"text/event-stream"),
                (b"cache-control", b"no-cache"),
                (b"connection", b"keep-alive"),
            ]
            await send({"type": "http.response.start", "status": 200, "headers": headers})

            last_mtime: float = 0
            try:
                while True:
                    if EVOLUTION_LOG.exists():
                        current_mtime = EVOLUTION_LOG.stat().st_mtime
                        if current_mtime != last_mtime:
                            last_mtime = current_mtime
                            status = build_status()
                            event_data = f"data: {json.dumps(status)}\n\n"
                            await send(
                                {
                                    "type": "http.response.body",
                                    "body": event_data.encode("utf-8"),
                                    "more_body": True,
                                }
                            )
                    await asyncio.sleep(SSE_POLL_INTERVAL)
            except (asyncio.CancelledError, ConnectionResetError):
                return

        # Static file serving fallback
        file_path = DASHBOARDS_DIR / path.lstrip("/")
        if file_path.is_dir():
            file_path = file_path / "index.html"

        if file_path.exists() and file_path.is_file():
            body = file_path.read_bytes()
            content_type = _guess_content_type(file_path)
            headers = cors_headers + [(b"content-type", content_type.encode("utf-8"))]
            await send({"type": "http.response.start", "status": 200, "headers": headers})
            await send({"type": "http.response.body", "body": body})
        else:
            await send({"type": "http.response.start", "status": 404, "headers": cors_headers})
            await send({"type": "http.response.body", "body": b"Not Found"})

    return app


def _guess_content_type(path: Path) -> str:
    """Guess MIME type from file extension.

    Args:
        path: File path.

    Returns:
        MIME type string.
    """
    ext_map: dict[str, str] = {
        ".html": "text/html",
        ".css": "text/css",
        ".js": "application/javascript",
        ".json": "application/json",
        ".png": "image/png",
        ".svg": "image/svg+xml",
    }
    return ext_map.get(path.suffix.lower(), "application/octet-stream")


def main() -> int:
    """Entry point -- prefer uvicorn, fall back to stdlib.

    Returns:
        Exit code (0 on success).
    """
    port = get_port()

    if not DASHBOARDS_DIR.exists():
        print(f"WARNING: Dashboards directory not found at {DASHBOARDS_DIR}", file=sys.stderr)
        DASHBOARDS_DIR.mkdir(parents=True, exist_ok=True)

    if not _try_uvicorn(port):
        run_stdlib_server(port)

    return 0


if __name__ == "__main__":
    sys.exit(main())
