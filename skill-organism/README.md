<div align="center">

# Cortex Skill Organism

### Your AI skills are alive. They compete, mutate, breed, and evolve.

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![MIT License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Version: 1.3.0](https://img.shields.io/badge/version-1.3.0-orange.svg)](../CHANGELOG.md)
[![Skills: 27](https://img.shields.io/badge/skills-27-blueviolet.svg)](../skills/)
[![GitHub Stars](https://img.shields.io/github/stars/TECHKNOWMAD-LABS/cortex-research-suite?style=social)](https://github.com/TECHKNOWMAD-LABS/cortex-research-suite)

</div>

---

## The Idea

What if AI skills weren't static prompts — but **living organisms** that compete for survival?

Cortex Skill Organism implements a biological evolution engine inspired by [Karpathy's autoresearch pattern](https://github.com/karpathy/autoresearchgpt). Each skill has DNA (its `SKILL.md` instructions) and an arena strategy (its `ARENA.md`). The engine runs genetic selection: observe telemetry, mutate top performers, cull the weak, crossbreed the strong, and heal the critical. What emerges after thousands of generations is something no human could design by hand.

---

## See It In Action

Open [`dashboards/petri-dish.html`](../dashboards/petri-dish.html) — watch 27 skills evolve as glowing organisms in a digital petri dish. No install, no API key. Press PLAY and watch natural selection happen in real-time.

Or run the CLI simulator:

```bash
# 1000 generations in under 2 seconds
python evolution_simulator.py --gens 1000 --seed 42

# Try the chaos seed
python evolution_simulator.py --gens 5000 --seed 1337

# Production overnight evolution
python enterprise_runner.py --overnight --generations 10
```

---

## The Evolution Loop

```
    OBSERVE          MUTATE           SELECT          REPRODUCE         HEAL
┌──────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌──────────┐
│ Collect      │→│ Generate   │→│ Cull weak  │→│ Crossover  │→│ Restore  │
│ telemetry    │ │ variants   │ │ (<0.6)     │ │ top 10     │ │ critical │
│ per skill    │ │ from top 5 │ │ Promote    │ │ Create 1-3 │ │ skills   │
│              │ │            │ │ strong     │ │ offspring  │ │          │
└──────────────┘ └────────────┘ │ (>0.8)     │ └────────────┘ └──────────┘
                                └────────────┘
```

**Fitness = 0.40 x success_rate + 0.40 x satisfaction + 0.20 x invocation_frequency**

- Below 0.6 with < 5 uses? **Culled.**
- Above 0.8? **Promoted to auto-deploy.**
- Top 10 performers? **Crossbred to produce offspring.**

---

## Enterprise Runner

`enterprise_runner.py` provides production-grade safety for autonomous overnight evolution:

| Feature | Detail |
|---------|--------|
| **SHA-256 integrity** | Registry verified before and after every mutation |
| **Atomic rollback** | Full snapshots — instant rollback on any failure |
| **fcntl lockfile** | Prevents concurrent execution |
| **Health gate** | Aborts if >30% critical or >80% deprecated |
| **JSON logging** | Structured logs with rotation (50 MB max) |
| **Telemetry retention** | Auto-purges data older than 90 days |
| **Signal handling** | Graceful shutdown on SIGTERM/SIGINT |
| **CI/CD exit codes** | 0=success, 1=failure, 2=lock, 3=integrity, 4=health, 5=rollback |

---

## Installation

```bash
pip install cortex-skill-organism
```

Or from source:

```bash
git clone https://github.com/TECHKNOWMAD-LABS/cortex-research-suite.git
cd cortex-research-suite && pip install -e .
```

**Requirements:** Python 3.10+, zero external dependencies.

---

## Quick Start

```python
from pathlib import Path
from cortex_skill_organism import SkillOrganism

organism = SkillOrganism(
    registry_path=Path("skill_registry.json"),
    telemetry_db=Path("skill_telemetry.db"),
    log_dir=Path("logs"),
)

result = organism.evolve()
report = organism.report()
```

---

## Live Results

From an actual evolution run on the 27-skill ecosystem (v1.3.0):

```
EVOLUTION CYCLE COMPLETE — 0.03s
  Skills observed: 27
  Culled: 7
  Promoted: 1
  Offspring: 2
  Critical (healing): 3
```

1,040+ invocations processed across 7 categories: research, MLOps, agents, meta, security, prompting, creative. Includes 5 trilogy integration skills (MindSpider, intelligence analysis, multimodal, forum intelligence, scenario simulation) and web-intelligence.

---

## Notable Seeds

Try these seeds with the evolution simulator or the Petri Dish dashboard:

| Seed | Name | What happens |
|:----:|------|-------------|
| `42` | The Classic | Balanced evolution, clean convergence |
| `137` | Fine Structure | Late-game paradigm shift reshuffles everything |
| `2025` | Year Zero | Slow start, explosive mid-game growth |
| `7777` | Lucky Streak | One skill dominates for 500 gens, then collapses |
| `1337` | Chaos Mode | Maximum entropy — extinction events every 100 gens |
| `9999` | The Marathon | Slow burn, 3 species survive to generation 10,000 |

---

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md). Good first issues: custom fitness functions, telemetry exporters, health check strategies, new evolution visualizations.

## License

MIT. See [LICENSE](../LICENSE).

## Citation

```bibtex
@software{cortex_2026,
  title={Cortex: Evolutionary Intelligence for AI Skill Ecosystems},
  author={TechKnowmad Labs},
  year={2026},
  url={https://github.com/TECHKNOWMAD-LABS/cortex-research-suite}
}
```

---

<div align="center">

**Built by [TechKnowmad AI](https://techknowmad.ai)**

*27 skills. One organism. Infinite evolution.*

</div>
