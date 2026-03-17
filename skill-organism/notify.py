"""Send notifications on evolution events via Telegram, Discord, or console.

Reads delta reports from evolution_delta.py and dispatches formatted messages
to configured channels.

Usage:
    python notify.py --generation N [--dry-run]

Environment variables:
    TELEGRAM_BOT_TOKEN  - Telegram bot API token
    TELEGRAM_CHAT_ID    - Telegram chat/channel ID
    DISCORD_WEBHOOK_URL - Discord webhook URL
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

HTTP_TIMEOUT = 10

# Import evolution_delta from the same directory
_THIS_DIR = Path(__file__).parent
sys.path.insert(0, str(_THIS_DIR))

from evolution_delta import DEFAULT_LOG, compute_delta, load_generations  # noqa: E402


def format_message(report: dict[str, Any], generation: int) -> str:
    """Format a human-readable notification message from a delta report.

    Args:
        report: The delta report dictionary from compute_delta.
        generation: The target generation number.

    Returns:
        Formatted plain-text message.
    """
    improved_count = report["summary"]["improved_count"]
    regressed_count = report["summary"]["regressed_count"]
    total = report["summary"]["total_skills"]
    direction = report["direction"]

    lines = [
        f"Cortex Evolution - Generation {generation}",
        f"Direction: {direction.upper()}",
        f"Skills: {total} total | {improved_count} improved | {regressed_count} regressed",
        "",
    ]

    # Top performer (highest positive delta)
    all_improved = report.get("improved", [])
    if all_improved:
        top = max(all_improved, key=lambda e: e["delta"])
        lines.append(f"Top performer: {top['skill']} (+{top['delta']:.4f})")

    # Worst performer (lowest negative delta)
    all_regressed = report.get("regressed", [])
    if all_regressed:
        worst = min(all_regressed, key=lambda e: e["delta"])
        lines.append(f"Worst performer: {worst['skill']} ({worst['delta']:.4f})")

    if not all_improved and not all_regressed:
        lines.append("No significant changes detected.")

    return "\n".join(lines)


def send_telegram(message: str, token: str, chat_id: str) -> bool:
    """Send a message via Telegram Bot API using raw HTTP.

    Args:
        message: The text message to send.
        token: Telegram bot token.
        chat_id: Target chat ID.

    Returns:
        True if the message was sent successfully.
    """
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = json.dumps({"chat_id": chat_id, "text": message, "parse_mode": "HTML"}).encode("utf-8")

    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            return resp.status == 200
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
        print(f"Telegram send failed: {exc}", file=sys.stderr)
        return False


def send_discord(message: str, webhook_url: str) -> bool:
    """Send a message via Discord webhook.

    Args:
        message: The text message to send.
        webhook_url: Discord webhook URL.

    Returns:
        True if the message was sent successfully.
    """
    payload = json.dumps({"content": message}).encode("utf-8")
    req = urllib.request.Request(webhook_url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            return resp.status in (200, 204)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
        print(f"Discord send failed: {exc}", file=sys.stderr)
        return False


def send_console(message: str) -> bool:
    """Print the notification to stdout as a fallback.

    Args:
        message: The text message to display.

    Returns:
        Always True.
    """
    print("=" * 50)
    print("EVOLUTION NOTIFICATION")
    print("=" * 50)
    print(message)
    print("=" * 50)
    return True


def dispatch(message: str, dry_run: bool = False) -> list[str]:
    """Send notification to all configured channels.

    Args:
        message: The formatted notification message.
        dry_run: If True, only print to console without sending.

    Returns:
        List of channel names where the message was delivered.
    """
    delivered: list[str] = []

    if dry_run:
        send_console(message)
        delivered.append("console (dry-run)")
        return delivered

    tg_token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    tg_chat = os.environ.get("TELEGRAM_CHAT_ID", "")
    discord_url = os.environ.get("DISCORD_WEBHOOK_URL", "")

    if tg_token and tg_chat:
        if send_telegram(message, tg_token, tg_chat):
            delivered.append("telegram")

    if discord_url:
        if send_discord(message, discord_url):
            delivered.append("discord")

    # Always fall back to console if no remote channels configured or all failed
    if not delivered:
        send_console(message)
        delivered.append("console")

    return delivered


def main(argv: list[str] | None = None) -> int:
    """CLI entry point.

    Args:
        argv: Command-line arguments (defaults to sys.argv[1:]).

    Returns:
        Exit code (0 on success).
    """
    parser = argparse.ArgumentParser(description="Send evolution notifications")
    parser.add_argument("--generation", type=int, required=True, help="Target generation number")
    parser.add_argument("--dry-run", action="store_true", help="Print to console only, do not send")
    parser.add_argument("--log", type=str, default=str(DEFAULT_LOG), help="Path to evolution_log.jsonl")
    args = parser.parse_args(argv)

    log_path = Path(args.log)
    generations = load_generations(log_path)
    sorted_gens = sorted(generations.keys())

    target = args.generation
    if target not in generations:
        print(f"ERROR: Generation {target} not found.", file=sys.stderr)
        return 1

    idx = sorted_gens.index(target)
    if idx == 0:
        print(f"ERROR: No previous generation before {target}.", file=sys.stderr)
        return 1

    prev_gen = sorted_gens[idx - 1]
    report = compute_delta(generations[prev_gen], generations[target])
    message = format_message(report, target)
    channels = dispatch(message, dry_run=args.dry_run)

    print(f"Notification sent to: {', '.join(channels)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
