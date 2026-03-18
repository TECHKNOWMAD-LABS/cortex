<div align="center">

# Cortex Research Suite

### The world's first AI Research Operating System where skills evolve like living organisms

[![CI](https://github.com/TECHKNOWMAD-LABS/cortex-research-suite/actions/workflows/ci.yml/badge.svg)](https://github.com/TECHKNOWMAD-LABS/cortex-research-suite/actions/workflows/ci.yml)
[![Evaluation Pipeline](https://github.com/TECHKNOWMAD-LABS/cortex-research-suite/actions/workflows/eval.yml/badge.svg)](https://github.com/TECHKNOWMAD-LABS/cortex-research-suite/actions/workflows/eval.yml)
[![Security Scan](https://github.com/TECHKNOWMAD-LABS/cortex-research-suite/actions/workflows/security.yml/badge.svg)](https://github.com/TECHKNOWMAD-LABS/cortex-research-suite/actions/workflows/security.yml)
[![Python 3.10-3.12](https://img.shields.io/badge/python-3.10--3.12-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Version: 1.3.0](https://img.shields.io/badge/version-1.3.0-orange.svg)](CHANGELOG.md)
[![Skills: 27](https://img.shields.io/badge/skills-27-blueviolet.svg)](skills/)
[![Tests: 194](https://img.shields.io/badge/tests-194%20passed-brightgreen.svg)](tests/)
[![Platforms: 6](https://img.shields.io/badge/platforms-6-ff69b4.svg)](cross-platform/)
[![NVIDIA Inception](https://img.shields.io/badge/NVIDIA-Inception%20Program-76b900.svg)](https://www.nvidia.com/en-us/startups/)
[![Zoho for Startups](https://img.shields.io/badge/Zoho-Startup%20Partner-e42527.svg)](https://www.zoho.com/startups/)
[![DPIIT Registered](https://img.shields.io/badge/DPIIT-Registered%20Startup-ff9933.svg)](https://www.startupindia.gov.in/)

**27 self-evolving skills** | **6 platforms** | **194 tests** | **Zero-config browser demos** | **Enterprise-grade security**

[Try the Petri Dish Demo](#-petri-dish-demo) | [Quickstart](#-quickstart) | [Architecture](#-how-it-works) | [Contributing](CONTRIBUTING.md)

</div>

---

## What if your AI tools could evolve on their own?

Cortex Research Suite treats AI skills as **living organisms**. Each skill has DNA (its prompt instructions), competes in an evaluation arena, and evolves through genetic selection — mutation, crossover, and natural selection. The best variants survive. The weak ones die. After 10,000 generations, what emerges is something no human could have designed by hand.

Built on [Karpathy's autoresearch pattern](https://github.com/karpathy/autoresearchgpt), extended with:

- **Skill Organism Engine** — genetic evolution with fitness scoring, population dynamics, and crash-safe rollback
- **Trilogy Integration** — MindSpider social listening + BettaFish intelligence analysis + MiroFish scenario simulation
- **8 LLM Judge Providers** — Claude, GPT, Groq, Together AI, Ollama, LM Studio, Custom endpoints, or fully synthetic
- **Cross-platform everywhere** — Claude Code, MCP, LangChain, CrewAI, OpenAI GPT Actions, AutoGen

---

## Petri Dish Demo

> **Zero install. Zero API key. Just open and watch.**

Open [`dashboards/petri-dish.html`](dashboards/petri-dish.html) in any browser. Press **PLAY**. Watch 27 AI skills evolve as glowing organisms in a digital petri dish.

**What you'll see:**
- Skills competing for dominance across 10,000 generations
- Real-time mutations, crossovers, extinctions, and rebirths
- Red Queen dynamics where the fitness landscape shifts under everyone's feet
- Paradigm shifts that reshape the entire ecosystem
- Generative audio — chimes on mutation, harmonics on crossover, bass rumble on extinction

**What you can do:**
- Click **CATACLYSM** to trigger mass extinction (and watch who survives)
- Click any organism to see its full genetic history and fitness trajectory
- Activate **Claude Judge** to bring in real LLM evaluation at any generation
- Try seed `42` for the classic run, `7777` for the lucky streak, or `1337` for chaos mode
- Push speed to 80x and watch 10,000 generations fly by in under 2 minutes

**8 Judge Providers** — connect any LLM to judge skill fitness in real-time:

| Provider | Type | Setup |
|----------|------|-------|
| Synthetic | Built-in | No API key needed — runs entirely in-browser |
| Claude (Anthropic) | Cloud | API key in settings |
| GPT (OpenAI) | Cloud | API key in settings |
| Groq | Cloud | API key in settings |
| Together AI | Cloud | API key in settings |
| Ollama | Local | Running on `localhost:11434` |
| LM Studio | Local | Running on `localhost:1234` |
| Custom | Any | Your own endpoint URL |

---

## Quickstart

### Option 1: Browser (no install)

```bash
# Just open the HTML file — works offline, no dependencies
open dashboards/petri-dish.html
```

### Option 2: Full suite

```bash
git clone https://github.com/TECHKNOWMAD-LABS/cortex-research-suite.git
cd cortex-research-suite
pip install -e ".[dev]"

# Run 194 tests to verify everything works
pytest

# Generate evaluation datasets for all 27 skills
python datasets/generators/skill_dataset_generator.py --all-skills --n 50

# Run the evolution simulator (1000 generations in <2 seconds)
python skill-organism/evolution_simulator.py --gens 1000 --seed 42

# Start overnight autonomous evolution
python skill-organism/enterprise_runner.py --overnight --generations 10
```

### Option 3: Core framework only

```bash
pip install cortex-research-suite
```

### Option 4: Python API

```python
from cortex.synthetic.reasoning_generator import ReasoningGenerator
from cortex.evaluation.judge import LLMJudge
from cortex.agents.orchestrator import AgentOrchestrator

# Generate evaluation prompts
gen = ReasoningGenerator(seed=42)
prompts = gen.generate(100)

# Run multi-agent research pipeline
orchestrator = AgentOrchestrator(provider)
result = orchestrator.run("Analyze the impact of transformer architectures on NLP")

# Evaluate output quality
judge = LLMJudge(provider)
score = judge.score(prompt="...", response=result.final_output)
print(f"Quality: {score.normalized:.0%}")  # e.g., Quality: 87%
```

---

## How It Works

### The Evolution Loop

```
         OBSERVE            MUTATE           SELECT          REPRODUCE         HEAL
    ┌──────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐   ┌──────────┐
    │ Collect      │──>│ Generate   │──>│ Cull weak  │──>│ Crossover  │──>│ Restore  │
    │ telemetry    │   │ variants   │   │ (<0.6)     │   │ top 10     │   │ critical │
    │ per skill    │   │ from top 5 │   │ Promote    │   │ Create 1-3 │   │ skills   │
    │              │   │            │   │ strong     │   │ offspring  │   │          │
    └──────────────┘   └────────────┘   │ (>0.8)     │   └────────────┘   └──────────┘
                                        └────────────┘
```

**Fitness = 0.40 x success_rate + 0.40 x satisfaction + 0.20 x invocation_frequency**

### The Intelligence Stack

| Layer | Component | What it does |
|:-----:|-----------|-------------|
| **5** | Scenario Simulator | Swarm-based what-if analysis with counterfactual injection |
| **4** | Intelligence Engine | Multi-source queries, forum analysis, multimodal content |
| **3** | MindSpider Connector | Live social listening feeds from Reddit, HN, Bluesky |
| **2** | Skill Organism | Autonomous evolution with fitness tracking and genetic selection |
| **1** | 27 Core Skills | Research, security, MLOps, orchestration, quality, testing |

---

## 27 Skills

Every skill has a `SKILL.md` (its DNA) and an `ARENA.md` (its evolution strategy). The organism engine reads these to drive autonomous improvement.

| # | Skill | Category | What it does |
|:-:|-------|----------|-------------|
| 1 | `agent-orchestrator` | Agents | Multi-agent coordination with DAG task graphs |
| 2 | `agent-output-validator` | Validation | Quality gates for agent outputs |
| 3 | `code-review-engine` | Engineering | Automated code review with security checks |
| 4 | `context-engineer` | Engineering | Context window optimization and prompt management |
| 5 | `de-slop` | Quality | Detect and remove AI-generated writing patterns |
| 6 | `design-system-forge` | Design | Design system generation and component scaffolding |
| 7 | `dev-lifecycle-engine` | DevOps | Full development lifecycle management |
| 8 | `diff-generator` | Engineering | Structured diffs for code and documents |
| 9 | `forum-intelligence` | Intelligence | Forum analysis with coordination detection |
| 10 | `github-mcp` | Integration | GitHub API via Model Context Protocol |
| 11 | `intelligence-query` | Intelligence | Multi-source intelligence analysis |
| 12 | `meta-skill-evolver` | Meta | The skill that evolves other skills |
| 13 | `mindspider-connector` | Data | Live social listening feed connector |
| 14 | `mlops-standards` | MLOps | ML operations best practices enforcement |
| 15 | `multimodal-analyst` | Intelligence | Cross-modal analysis (text + image + video) |
| 16 | `persistent-memory` | Infrastructure | SQLite-backed memory with FTS5 search |
| 17 | `pre-package-pipeline` | Packaging | Skill validation and packaging |
| 18 | `prompt-architect` | Engineering | Prompt engineering and optimization |
| 19 | `repo-publisher` | DevOps | Pre-publish pipeline with security scanning |
| 20 | `research-workflow` | Research | Experiment design and methodology |
| 21 | `scenario-simulator` | Simulation | Swarm scenario simulation with counterfactuals |
| 22 | `security-audit` | Security | Bandit + semgrep + secret scanning pipeline |
| 23 | `session-memory` | Infrastructure | Session-scoped memory persistence |
| 24 | `skill-test-harness` | Testing | Automated testing with LLM-as-Judge |
| 25 | `skill-validator` | Validation | Skill structure and manifest validation |
| 26 | `tdd-enforcer` | Testing | Test-driven development enforcement |
| 27 | `web-intelligence` | Intelligence | Live web scraping with Scrapling |

See [AGENTS.md](AGENTS.md) for the full agent manifest with platform-specific guides.

---

## 6-Platform Cross-Platform Support

Every skill works everywhere. 162 adapter files generated and tested.

| Platform | Adapter | Status | Directory |
|----------|---------|:------:|-----------|
| Claude Code | Native Skills | 27/27 | `skills/` |
| MCP (Model Context Protocol) | FastMCP Servers | 27/27 | `cross-platform/generated/mcp/` |
| LangChain | Tool Classes | 27/27 | `cross-platform/generated/langchain/` |
| CrewAI | Tool Wrappers | 27/27 | `cross-platform/generated/crewai/` |
| OpenAI GPT Actions | OpenAPI Schemas | 27/27 | `cross-platform/generated/openai/` |
| AutoGen / Agents | Agent Manifests | 27/27 | `cross-platform/generated/agents/` |

Also compatible with **VS Code, Copilot, Cursor, Windsurf, and JetBrains** via MCP adapters.

---

## Live Mode (optional)

```bash
pip install -e ".[live]"
```

Enables [Scrapling](https://github.com/nichochar/scrapling)-powered real-time web intelligence:

- `mindspider-connector --source scrapling` — live Reddit/HN/Bluesky feeds
- `research-workflow --live-evidence` — real-time Scholar/PubMed/arXiv citations
- `web-intelligence` — full live web sweeps
- `forum-intelligence` — live forum thread scraping

All skills work fully offline without Scrapling — live mode is purely additive.

---

## Browser Dashboards

| Dashboard | File | What it does |
|-----------|------|-------------|
| **Petri Dish** | `dashboards/petri-dish.html` | Interactive evolution visualization with 8 judge providers |
| **Skill Arena** | `dashboards/skill_arena_demo.html` | Live skill evaluation with Anthropic API |
| **Evolution Dashboard** | `dashboards/evolution_dashboard.html` | Evolution progress tracking |
| **Benchmark Dashboard** | `dashboards/benchmark_dashboard.html` | Skill performance benchmarks |

All dashboards are standalone HTML — no build step, no server, no dependencies.

---

## Cortex Python Framework

| Module | What it does |
|--------|-------------|
| `cortex.synthetic` | Synthetic data generation (reasoning, research, strategy, domain, adversarial) |
| `cortex.evaluation` | LLM-as-Judge scoring, benchmark suites, regression detection |
| `cortex.agents` | Multi-agent orchestrator, debate arena, DAG task graphs |
| `cortex.models` | Model provider abstraction (Anthropic SDK + CLI fallback) |
| `cortex.telemetry` | Structured logging, SQLite metrics collector |
| `cortex.config` | YAML + env var configuration with thread-safe singleton |
| `cortex.utils` | Atomic I/O, input sanitization, prompt injection detection |
| `cortex.experiments` | Experiment tracking with comparison and best-run queries |

---

## Enterprise-Grade Security

Every push is scanned. Every input is sanitized. Every secret is blocked.

- **Bandit SAST** — zero HIGH/MEDIUM findings
- **CodeQL** — semantic code analysis on every PR
- **Secret scanning** — push protection enabled, pre-commit hooks
- **Prompt injection detection** — 7 compiled regex patterns
- **Path traversal protection** — all I/O operations validated
- **Browser dashboards** — CSP headers, sessionStorage isolation, rate limiting, input sanitization
- **SQL injection prevention** — parameterized queries everywhere
- **Dependency monitoring** — Dependabot with weekly updates

See [SECURITY.md](SECURITY.md) for the full security policy including per-skill hardening details.

---

## Project Structure

```
cortex-research-suite/
├── cortex/                    # Python framework (pip install -e .)
├── skills/                    # 27 self-evolving skills (SKILL.md + ARENA.md + scripts/)
├── skill-organism/            # Evolution engine (observe → mutate → select → reproduce → heal)
├── dashboards/                # 4 browser dashboards (Petri Dish, Arena, Evolution, Benchmark)
├── cross-platform/            # 162 generated adapters (MCP, LangChain, CrewAI, OpenAI, AutoGen)
├── knowledge/                 # Knowledge store (FTS5 + GraphRAG)
├── datasets/                  # Synthetic datasets + MindSpider feed
├── benchmarks/                # Performance baselines for all skills
├── experiments/               # Experiment tracker (SQLite)
├── packages/                  # Standalone packages (de-slop-cli)
├── docs/                      # Documentation site (GitHub Pages)
├── scripts/                   # CLI entry points and utilities
├── tests/                     # 194 tests across 18 modules
└── .github/workflows/         # CI/CD (lint, test, security, eval, release)
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). We welcome PRs for:

- New skills (follow the SKILL.md + ARENA.md pattern)
- Custom fitness functions for the evolution engine
- Additional cross-platform adapters
- Dashboard improvements and new visualizations
- Telemetry exporters and health check strategies

All PRs require passing CI (bandit, lint, tests), one approving review, and no leaked secrets.

---

## Legal

MIT licensed. Trilogy integration skills are inspired by the architectural patterns of MindSpider, BettaFish, and MiroFish. No code was copied. See [LEGAL_NOTES.md](LEGAL_NOTES.md).

---

<div align="center">

**Built by [TechKnowmad AI](https://techknowmad.ai)**

*27 skills. 6 platforms. 194 tests. One evolving organism.*

</div>
