#!/usr/bin/env python3
"""Evolution simulator — run 1000+ generations with synthetic scoring.

Uses real genetic algorithm (crossover, mutation, selection) with calibrated
noise curves that model realistic improvement trajectories.

Output: evolution_log_sim.jsonl with rich per-generation data.

Usage:
    python evolution_simulator.py                    # 1000 gens, seed 42
    python evolution_simulator.py --gens 2000        # 2000 gens
    python evolution_simulator.py --seed 137         # specific seed
    python evolution_simulator.py --llm-checkpoints  # generate LLM checkpoint prompts
"""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

SKILLS = [
    ("agent-orchestrator", "agents"),
    ("agent-output-validator", "validation"),
    ("code-review-engine", "engineering"),
    ("context-engineer", "engineering"),
    ("de-slop", "quality"),
    ("design-system-forge", "design"),
    ("dev-lifecycle-engine", "devops"),
    ("diff-generator", "engineering"),
    ("forum-intelligence", "intelligence"),
    ("github-mcp", "integration"),
    ("intelligence-query", "intelligence"),
    ("meta-skill-evolver", "meta"),
    ("mindspider-connector", "data"),
    ("mlops-standards", "mlops"),
    ("multimodal-analyst", "intelligence"),
    ("persistent-memory", "infra"),
    ("pre-package-pipeline", "packaging"),
    ("prompt-architect", "engineering"),
    ("repo-publisher", "devops"),
    ("research-workflow", "research"),
    ("scenario-simulator", "simulation"),
    ("security-audit", "security"),
    ("session-memory", "infra"),
    ("skill-test-harness", "testing"),
    ("skill-validator", "validation"),
    ("tdd-enforcer", "testing"),
    ("web-intelligence", "intelligence"),
]


@dataclass
class SkillState:
    name: str
    category: str
    fitness: float
    born: int = 0
    mutations: int = 0
    parent_a: str = ""
    parent_b: str = ""


def simulate(
    n_gens: int = 1000,
    seed: int = 42,
    mut_rate: float = 0.3,
    sel_pressure: float = 0.2,
    cat_freq: int = 25,
) -> list[dict[str, Any]]:
    """Run full evolution simulation with rich event logging."""
    rng = random.Random(seed)

    # Initialize population
    pop = [
        SkillState(
            name=name,
            category=cat,
            fitness=max(0.15, min(0.85, 0.35 + rng.gauss(0.1, 0.06))),
        )
        for name, cat in SKILLS
    ]

    log: list[dict[str, Any]] = []

    def snap() -> list[dict[str, Any]]:
        return [asdict(s) for s in pop]

    def stats() -> tuple[float, float, float]:
        fits = [s.fitness for s in pop]
        return sum(fits) / len(fits), max(fits), min(fits)

    mean, mx, mn = stats()
    log.append(
        {
            "generation": 0,
            "skills": snap(),
            "events": [],
            "mean_fitness": round(mean, 4),
            "max_fitness": round(mx, 4),
            "min_fitness": round(mn, 4),
            "top_skill": max(pop, key=lambda s: s.fitness).name,
            "bottom_skill": min(pop, key=lambda s: s.fitness).name,
        }
    )

    for gen in range(1, n_gens + 1):
        events: list[dict[str, Any]] = []
        sorted_pop = sorted(pop, key=lambda s: s.fitness, reverse=True)
        n_mut = max(1, int(len(pop) * sel_pressure))
        candidates = sorted_pop[-n_mut:]

        # Crossover (30% chance per generation)
        if rng.random() < 0.3 and len(sorted_pop) >= 2:
            p1, p2 = sorted_pop[0], sorted_pop[1]
            weakest = sorted_pop[-1]
            idx = next(i for i, s in enumerate(pop) if s.name == weakest.name)
            child_fit = max(0.1, min(0.98, p1.fitness * 0.6 + p2.fitness * 0.4 + rng.gauss(0.01, 0.008)))
            events.append(
                {
                    "type": "crossover",
                    "skill": weakest.name,
                    "parent_a": p1.name,
                    "parent_b": p2.name,
                    "fitness_before": round(weakest.fitness, 4),
                    "fitness_after": round(child_fit, 4),
                }
            )
            pop[idx].fitness = child_fit
            pop[idx].parent_a = p1.name
            pop[idx].parent_b = p2.name
            pop[idx].born = gen
            pop[idx].mutations = 0

        # Mutation
        for cand in candidates:
            idx = next(i for i, s in enumerate(pop) if s.name == cand.name)
            old = pop[idx].fitness
            imp_chance = max(0.25, 1.0 - pop[idx].fitness)
            if rng.random() < imp_chance:
                delta = rng.gauss(0.015, 0.01) * (1.0 - pop[idx].fitness) * (1 + mut_rate)
                pop[idx].fitness = max(0.1, min(0.98, pop[idx].fitness + delta))
            else:
                delta = rng.gauss(-0.008, 0.005)
                pop[idx].fitness = max(0.1, min(0.98, pop[idx].fitness + delta))
            pop[idx].mutations += 1
            d = pop[idx].fitness - old
            if abs(d) > 0.003:
                events.append(
                    {
                        "type": "mutation",
                        "skill": pop[idx].name,
                        "fitness_before": round(old, 4),
                        "fitness_after": round(pop[idx].fitness, 4),
                        "delta": round(d, 4),
                        "direction": "improved" if d > 0 else "regressed",
                    }
                )

        # Environmental shift every 10 gens
        if gen % 10 == 0:
            lucky = pop[rng.randint(0, len(pop) - 1)]
            old = lucky.fitness
            lucky.fitness = min(0.98, lucky.fitness + rng.gauss(0.03, 0.015))
            events.append(
                {
                    "type": "environment_shift",
                    "skill": lucky.name,
                    "fitness_before": round(old, 4),
                    "fitness_after": round(lucky.fitness, 4),
                }
            )

        # Catastrophe (extinction + rebirth)
        if gen % cat_freq == 0 and gen > 0:
            worst = sorted_pop[-1]
            idx = next(i for i, s in enumerate(pop) if s.name == worst.name)
            old = pop[idx].fitness
            pop[idx].fitness = max(0.1, min(0.6, 0.25 + rng.gauss(0.05, 0.03)))
            pop[idx].born = gen
            pop[idx].mutations = 0
            events.append(
                {
                    "type": "extinction_rebirth",
                    "skill": worst.name,
                    "fitness_before": round(old, 4),
                    "fitness_after": round(pop[idx].fitness, 4),
                }
            )

        mean, mx, mn = stats()
        top = max(pop, key=lambda s: s.fitness)
        bot = min(pop, key=lambda s: s.fitness)
        log.append(
            {
                "generation": gen,
                "skills": snap(),
                "events": events,
                "mean_fitness": round(mean, 4),
                "max_fitness": round(mx, 4),
                "min_fitness": round(mn, 4),
                "top_skill": top.name,
                "bottom_skill": bot.name,
            }
        )

    return log


def generate_llm_checkpoint_prompts(log: list[dict], interval: int = 50) -> list[dict]:
    """Generate prompts for LLM-as-Judge at milestone generations."""
    checkpoints = []
    for entry in log:
        gen = entry["generation"]
        if gen % interval != 0 or gen == 0:
            continue
        top5 = sorted(entry["skills"], key=lambda s: s["fitness"], reverse=True)[:5]
        bot3 = sorted(entry["skills"], key=lambda s: s["fitness"])[:3]
        prompt = (
            f"You are evaluating AI skill evolution at generation {gen} of 1000.\n\n"
            f"Population statistics:\n"
            f"  Mean fitness: {entry['mean_fitness']:.4f}\n"
            f"  Max fitness: {entry['max_fitness']:.4f}\n"
            f"  Min fitness: {entry['min_fitness']:.4f}\n\n"
            f"Top 5 skills:\n"
            + "\n".join(
                f"  {i + 1}. {s['name']} ({s['category']}) — fitness: {s['fitness']:.4f}, mutations: {s['mutations']}, born gen {s['born']}"
                for i, s in enumerate(top5)
            )
            + f"\n\nBottom 3 skills:\n"
            + "\n".join(
                f"  {s['name']} ({s['category']}) — fitness: {s['fitness']:.4f}, mutations: {s['mutations']}"
                for s in bot3
            )
            + f"\n\nEvents this generation: {len(entry['events'])}"
            + f"\n\nRate the overall health of this evolving ecosystem on a scale of 0-1. "
            f"Consider: diversity, convergence rate, fitness distribution, and evolutionary dynamics. "
            f'Respond with ONLY a JSON object: {{"health_score": 0.XX, "assessment": "one sentence"}}'
        )
        checkpoints.append({"generation": gen, "prompt": prompt, "skills_snapshot": top5})
    return checkpoints


def main() -> int:
    parser = argparse.ArgumentParser(description="Cortex Evolution Simulator")
    parser.add_argument("--gens", type=int, default=1000, help="Number of generations")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--mut-rate", type=float, default=0.3, help="Mutation rate")
    parser.add_argument("--sel-pressure", type=float, default=0.2, help="Selection pressure")
    parser.add_argument("--cat-freq", type=int, default=25, help="Catastrophe frequency")
    parser.add_argument("--output", type=str, default="evolution_log_sim.jsonl", help="Output file")
    parser.add_argument("--llm-checkpoints", action="store_true", help="Generate LLM checkpoint prompts")
    args = parser.parse_args()

    print(f"Simulating {args.gens} generations with seed {args.seed}...")
    log = simulate(args.gens, args.seed, args.mut_rate, args.sel_pressure, args.cat_freq)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w") as f:
        for entry in log:
            f.write(json.dumps(entry) + "\n")

    final = log[-1]
    print(f"Output: {out} ({out.stat().st_size:,} bytes)")
    print(f"Final mean fitness: {final['mean_fitness']:.4f}")
    print(f"Final max fitness:  {final['max_fitness']:.4f}")
    print(f"Top skill:          {final['top_skill']}")
    print(f"Bottom skill:       {final['bottom_skill']}")

    if args.llm_checkpoints:
        checkpoints = generate_llm_checkpoint_prompts(log)
        cp_out = out.with_name("llm_checkpoints.json")
        cp_out.write_text(json.dumps(checkpoints, indent=2))
        print(f"LLM checkpoints: {cp_out} ({len(checkpoints)} prompts)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
