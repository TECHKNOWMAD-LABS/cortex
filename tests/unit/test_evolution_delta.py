"""Tests for the evolution_delta module.

Validates delta computation, direction/severity classification, and edge cases.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Make evolution_delta importable
_ORGANISM_DIR = Path(__file__).resolve().parent.parent.parent / "skill-organism"
sys.path.insert(0, str(_ORGANISM_DIR))

import evolution_delta  # noqa: E402


def _write_log(entries: list[dict], tmp_path: Path) -> Path:
    """Write entries to a temporary JSONL file."""
    log_path = tmp_path / "evolution_log.jsonl"
    log_path.write_text("\n".join(json.dumps(e) for e in entries) + "\n", encoding="utf-8")
    return log_path


SAMPLE_GEN1 = [
    {
        "generation": 1,
        "skill": "skill-a",
        "score_before": 0.50,
        "score_after": 0.70,
        "delta": 0.20,
        "mutation_type": "example_replacement",
        "status": "improved",
        "timestamp": "2026-03-15T02:00:00Z",
    },
    {
        "generation": 1,
        "skill": "skill-b",
        "score_before": 0.80,
        "score_after": 0.60,
        "delta": -0.20,
        "mutation_type": "instruction_clarity",
        "status": "neutral",
        "timestamp": "2026-03-15T02:10:00Z",
    },
]

SAMPLE_GEN2 = [
    {
        "generation": 2,
        "skill": "skill-a",
        "score_before": 0.70,
        "score_after": 0.85,
        "delta": 0.15,
        "mutation_type": "reasoning_scaffolding",
        "status": "improved",
        "timestamp": "2026-03-15T04:00:00Z",
    },
    {
        "generation": 2,
        "skill": "skill-b",
        "score_before": 0.60,
        "score_after": 0.55,
        "delta": -0.05,
        "mutation_type": "edge_case_handling",
        "status": "neutral",
        "timestamp": "2026-03-15T04:10:00Z",
    },
]


class TestLoadGenerations:
    """Test JSONL loading and grouping."""

    def test_groups_by_generation(self, tmp_path: Path) -> None:
        log = _write_log(SAMPLE_GEN1 + SAMPLE_GEN2, tmp_path)
        gens = evolution_delta.load_generations(log)
        assert set(gens.keys()) == {1, 2}
        assert "skill-a" in gens[1]
        assert "skill-b" in gens[2]

    def test_empty_log(self, tmp_path: Path) -> None:
        log = tmp_path / "evolution_log.jsonl"
        log.write_text("", encoding="utf-8")
        gens = evolution_delta.load_generations(log)
        assert gens == {}

    def test_missing_file(self, tmp_path: Path) -> None:
        log = tmp_path / "nonexistent.jsonl"
        gens = evolution_delta.load_generations(log)
        assert gens == {}


class TestComputeDelta:
    """Test delta computation between two generations."""

    def test_improved_skill(self, tmp_path: Path) -> None:
        log = _write_log(SAMPLE_GEN1 + SAMPLE_GEN2, tmp_path)
        gens = evolution_delta.load_generations(log)
        report = evolution_delta.compute_delta(gens[1], gens[2])
        improved_names = [e["skill"] for e in report["improved"]]
        assert "skill-a" in improved_names

    def test_regressed_skill(self, tmp_path: Path) -> None:
        log = _write_log(SAMPLE_GEN1 + SAMPLE_GEN2, tmp_path)
        gens = evolution_delta.load_generations(log)
        report = evolution_delta.compute_delta(gens[1], gens[2])
        # skill-b: gen1 score_after=0.60, gen2 score_after=0.55 -> delta=-0.05
        regressed_names = [e["skill"] for e in report["regressed"]]
        assert "skill-b" in regressed_names

    def test_summary_counts(self, tmp_path: Path) -> None:
        log = _write_log(SAMPLE_GEN1 + SAMPLE_GEN2, tmp_path)
        gens = evolution_delta.load_generations(log)
        report = evolution_delta.compute_delta(gens[1], gens[2])
        assert report["summary"]["total_skills"] == 2


class TestDirectionClassification:
    """Test the classify_direction function."""

    def test_improving(self) -> None:
        assert evolution_delta.classify_direction(8, 2, 10) == "improving"

    def test_degrading(self) -> None:
        assert evolution_delta.classify_direction(2, 8, 10) == "degrading"

    def test_mixed(self) -> None:
        assert evolution_delta.classify_direction(5, 5, 10) == "mixed"

    def test_zero_total(self) -> None:
        assert evolution_delta.classify_direction(0, 0, 0) == "mixed"


class TestSeverityClassification:
    """Test the classify_severity function."""

    def test_significant(self) -> None:
        assert evolution_delta.classify_severity(0.15) == "significant"

    def test_moderate(self) -> None:
        assert evolution_delta.classify_severity(0.07) == "moderate"

    def test_minor(self) -> None:
        assert evolution_delta.classify_severity(0.02) == "minor"

    def test_negative_delta(self) -> None:
        assert evolution_delta.classify_severity(-0.12) == "significant"


class TestCLI:
    """Test CLI entry point edge cases."""

    def test_single_generation_error(self, tmp_path: Path) -> None:
        log = _write_log(SAMPLE_GEN1, tmp_path)
        result = evolution_delta.main(["--log", str(log)])
        assert result == 1

    def test_missing_generation_flag(self, tmp_path: Path) -> None:
        log = _write_log(SAMPLE_GEN1 + SAMPLE_GEN2, tmp_path)
        result = evolution_delta.main(["--log", str(log)])
        assert result == 0
