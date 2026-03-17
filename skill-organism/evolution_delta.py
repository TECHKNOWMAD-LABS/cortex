"""Compute deltas between consecutive evolution generations.

Reads evolution_log.jsonl and produces a structured JSON report showing which
skills improved, regressed, crossed over, were deprecated, are new, or remained
unchanged between two generations.

Usage:
    python evolution_delta.py [--generation N] [--output FILE]
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

DEFAULT_LOG = Path(__file__).parent / "evolution_log.jsonl"


@dataclass
class SkillDelta:
    """Single skill's change between two generations."""

    skill: str
    score_before: float
    score_after: float
    delta: float
    mutation_type: str
    severity: str  # "significant" | "moderate" | "minor"
    category: str  # "improved" | "regressed" | "unchanged" | ...


def classify_severity(delta: float) -> str:
    """Classify the magnitude of a delta value.

    Args:
        delta: The absolute change in score.

    Returns:
        One of "significant", "moderate", or "minor".
    """
    abs_delta = abs(delta)
    if abs_delta > 0.1:
        return "significant"
    if abs_delta > 0.05:
        return "moderate"
    return "minor"


def classify_direction(improved: int, regressed: int, total: int) -> str:
    """Determine overall evolution direction.

    Args:
        improved: Number of skills that improved.
        regressed: Number of skills that regressed.
        total: Total skills evaluated.

    Returns:
        One of "improving", "degrading", or "mixed".
    """
    if total == 0:
        return "mixed"
    if improved / total > 0.5:
        return "improving"
    if regressed / total > 0.5:
        return "degrading"
    return "mixed"


def load_generations(log_path: Path) -> dict[int, dict[str, dict[str, Any]]]:
    """Load evolution_log.jsonl and group entries by generation.

    Args:
        log_path: Path to the JSONL log file.

    Returns:
        Mapping of generation number to {skill_name: entry_dict}.
    """
    generations: dict[int, dict[str, dict[str, Any]]] = defaultdict(dict)
    if not log_path.exists():
        return generations

    for line in log_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        entry = json.loads(line)
        gen = int(entry.get("generation", 0))
        skill = entry.get("skill", "")
        if gen and skill:
            generations[gen][skill] = entry

    return dict(generations)


def compute_delta(
    gen_before: dict[str, dict[str, Any]],
    gen_after: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Compute the full delta report between two generations.

    Args:
        gen_before: Skill entries from the earlier generation.
        gen_after: Skill entries from the later generation.

    Returns:
        Delta report with categorised skill lists, direction, and summary.
    """
    all_skills = set(gen_before) | set(gen_after)

    buckets: dict[str, list[dict[str, Any]]] = {
        "improved": [],
        "regressed": [],
        "crossed_over": [],
        "deprecated": [],
        "new": [],
        "unchanged": [],
    }

    for skill in sorted(all_skills):
        before_entry = gen_before.get(skill)
        after_entry = gen_after.get(skill)

        if before_entry and not after_entry:
            buckets["deprecated"].append(
                _make_entry(skill, before_entry.get("score_after", 0.0), 0.0, before_entry.get("mutation_type", ""))
            )
            continue

        if after_entry and not before_entry:
            buckets["new"].append(
                _make_entry(skill, 0.0, after_entry.get("score_after", 0.0), after_entry.get("mutation_type", ""))
            )
            continue

        assert before_entry is not None and after_entry is not None
        score_before = before_entry.get("score_after", 0.0)
        score_after = after_entry.get("score_after", 0.0)
        delta = round(score_after - score_before, 4)
        mutation = after_entry.get("mutation_type", "")

        entry = _make_entry(skill, score_before, score_after, mutation)

        # Crossed over: changed from improving to regressing or vice-versa
        before_delta = before_entry.get("delta", 0.0)
        after_delta = after_entry.get("delta", 0.0)
        if (before_delta > 0 and after_delta < 0) or (before_delta < 0 and after_delta > 0):
            buckets["crossed_over"].append(entry)
        elif delta > 0.001:
            buckets["improved"].append(entry)
        elif delta < -0.001:
            buckets["regressed"].append(entry)
        else:
            buckets["unchanged"].append(entry)

    total = len(all_skills)
    direction = classify_direction(len(buckets["improved"]), len(buckets["regressed"]), total)

    return {
        "improved": [asdict(e) for e in buckets["improved"]],
        "regressed": [asdict(e) for e in buckets["regressed"]],
        "crossed_over": [asdict(e) for e in buckets["crossed_over"]],
        "deprecated": [asdict(e) for e in buckets["deprecated"]],
        "new": [asdict(e) for e in buckets["new"]],
        "unchanged": [asdict(e) for e in buckets["unchanged"]],
        "direction": direction,
        "summary": {
            "total_skills": total,
            "improved_count": len(buckets["improved"]),
            "regressed_count": len(buckets["regressed"]),
            "crossed_over_count": len(buckets["crossed_over"]),
            "deprecated_count": len(buckets["deprecated"]),
            "new_count": len(buckets["new"]),
            "unchanged_count": len(buckets["unchanged"]),
        },
    }


def _make_entry(skill: str, score_before: float, score_after: float, mutation_type: str) -> SkillDelta:
    """Build a SkillDelta dataclass for a single skill."""
    delta = round(score_after - score_before, 4)
    return SkillDelta(
        skill=skill,
        score_before=round(score_before, 4),
        score_after=round(score_after, 4),
        delta=delta,
        mutation_type=mutation_type,
        severity=classify_severity(delta),
        category="improved" if delta > 0 else ("regressed" if delta < 0 else "unchanged"),
    )


def main(argv: list[str] | None = None) -> int:
    """CLI entry point.

    Args:
        argv: Command-line arguments (defaults to sys.argv[1:]).

    Returns:
        Exit code (0 on success).
    """
    parser = argparse.ArgumentParser(description="Compute evolution deltas between generations")
    parser.add_argument("--generation", type=int, default=None, help="Compare this generation with the previous one")
    parser.add_argument("--output", type=str, default=None, help="Write JSON report to this file")
    parser.add_argument("--log", type=str, default=str(DEFAULT_LOG), help="Path to evolution_log.jsonl")
    args = parser.parse_args(argv)

    log_path = Path(args.log)
    generations = load_generations(log_path)

    if len(generations) < 2:
        print("ERROR: Need at least two generations to compute deltas.", file=sys.stderr)
        return 1

    sorted_gens = sorted(generations.keys())

    if args.generation is not None:
        target = args.generation
        if target not in generations:
            print(f"ERROR: Generation {target} not found in log.", file=sys.stderr)
            return 1
        idx = sorted_gens.index(target)
        if idx == 0:
            print(f"ERROR: No previous generation before {target}.", file=sys.stderr)
            return 1
        gen_before_num = sorted_gens[idx - 1]
        gen_after_num = target
    else:
        gen_before_num = sorted_gens[-2]
        gen_after_num = sorted_gens[-1]

    report = compute_delta(generations[gen_before_num], generations[gen_after_num])
    report["generation_before"] = gen_before_num
    report["generation_after"] = gen_after_num

    output_text = json.dumps(report, indent=2) + "\n"

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(output_text, encoding="utf-8")
        print(f"Delta report written to {args.output}", file=sys.stderr)
    else:
        print(output_text)

    return 0


if __name__ == "__main__":
    sys.exit(main())
