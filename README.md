# Cortex Research Suite

[![CI](https://github.com/TECHKNOWMAD-LABS/cortex-research-suite/actions/workflows/ci.yml/badge.svg)](https://github.com/TECHKNOWMAD-LABS/cortex-research-suite/actions/workflows/ci.yml)
[![Evaluation Pipeline](https://github.com/TECHKNOWMAD-LABS/cortex-research-suite/actions/workflows/eval.yml/badge.svg)](https://github.com/TECHKNOWMAD-LABS/cortex-research-suite/actions/workflows/eval.yml)
[![Security Scan](https://github.com/TECHKNOWMAD-LABS/cortex-research-suite/actions/workflows/security.yml/badge.svg)](https://github.com/TECHKNOWMAD-LABS/cortex-research-suite/actions/workflows/security.yml)
[![Python 3.10-3.12](https://img.shields.io/badge/python-3.10--3.12-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

21 autonomous skills + a Python evaluation framework for AI/ML research and development. Covers research workflows, MLOps enforcement, security auditing, agent orchestration, quality assurance, and developer tooling. Works natively with Claude Code and integrates with LangChain, CrewAI, and OpenAI via MCP adapters.

## Quickstart in 60 Seconds

```bash
# Clone and install
git clone https://github.com/TECHKNOWMAD-LABS/cortex-research-suite.git
cd cortex-research-suite
pip install -e ".[dev]"

# Run the test suite
pytest

# Generate a synthetic dataset (50 prompts, seeded for reproducibility)
cortex-generate --count 50 --seed 42 --output ./datasets

# Run a benchmark evaluation
cortex-benchmark --suite reasoning --output ./results

# Use any skill directly
cd skills/security-audit   # Each skill has a SKILL.md with instructions
```

### Use as a Python Library

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

## Skills

| Skill | Category | Description |
|-------|----------|-------------|
| `agent-orchestrator` | Agents | Multi-agent coordination and task dispatch |
| `agent-output-validator` | Validation | Automated validation of agent outputs against quality gates |
| `code-review-engine` | Engineering | Automated code review with security checks |
| `context-engineer` | Engineering | Context window optimization and prompt context management |
| `de-slop` | Quality | AI-generated writing pattern detection and removal |
| `design-system-forge` | Design | Design system generation and component library scaffolding |
| `dev-lifecycle-engine` | DevOps | Development lifecycle management |
| `diff-generator` | Engineering | Structured diff generation for code and document changes |
| `github-mcp` | Integration | GitHub API via Model Context Protocol |
| `meta-skill-evolver` | Meta | Evolutionary skill improvement and mutation engine |
| `mlops-standards` | MLOps | ML operations best practices enforcement |
| `persistent-memory` | Infrastructure | SQLite-backed memory with FTS5 search |
| `pre-package-pipeline` | Packaging | Skill validation and packaging pipeline |
| `prompt-architect` | Engineering | Prompt engineering and optimization |
| `repo-publisher` | DevOps | Pre-publish pipeline with security scanning and quality gates |
| `research-workflow` | Research | Experiment design and methodology |
| `security-audit` | Security | Bandit + semgrep + secret scanning pipeline |
| `session-memory` | Infrastructure | Session-scoped memory persistence across conversations |
| `skill-test-harness` | Testing | Automated skill testing framework |
| `skill-validator` | Validation | Skill structure and manifest validation |
| `tdd-enforcer` | Testing | Test-driven development enforcement with coverage tracking |

See [AGENTS.md](AGENTS.md) for the full agent manifest with platform-specific integration guides.

## Cortex Python Framework

The `cortex/` package is an installable Python library providing:

| Module | Purpose |
|--------|---------|
| `cortex.synthetic` | Synthetic data generation (reasoning, research, strategy, domain, adversarial) |
| `cortex.evaluation` | LLM-as-Judge scoring, benchmark suites, regression detection |
| `cortex.agents` | Multi-agent orchestrator, debate arena, DAG task graphs |
| `cortex.models` | Model provider abstraction (Anthropic SDK + CLI fallback) |
| `cortex.telemetry` | Structured logging, SQLite metrics collector |
| `cortex.config` | YAML + env var configuration with thread-safe singleton |
| `cortex.utils` | Atomic I/O, input sanitization, prompt injection detection |
| `cortex.experiments` | Experiment tracking with comparison and best-run queries |

## Skill Organism

The `skill-organism/` directory contains the evolution engine. Skills are automatically tested and scored. Underperformers get modified via mutation, top performers get replicated via crossbreeding, and the system recovers from population loss by restoring previously successful versions. Generation 0-1 skills are preserved indefinitely.

The enterprise runner (`enterprise_runner.py`) enforces SHA-256 integrity checks on the skill registry, supports atomic rollback on failure, and returns CI/CD-compatible exit codes.

## Cross-Platform Support

The `cross-platform/` directory contains generated adapters for each platform.

| Platform | Adapter Type | Directory | Status |
|----------|-------------|-----------|--------|
| Claude Code | Native Skills | `skills/` | Primary |
| MCP (Model Context Protocol) | FastMCP Servers | `cross-platform/generated/mcp/` | Generated |
| LangChain | Tool Classes | `cross-platform/generated/langchain/` | Generated |
| CrewAI | Tool Wrappers | `cross-platform/generated/crewai/` | Generated |
| OpenAI GPT Actions | Action Schemas | `cross-platform/generated/openai/` | Generated |
| AGENTS.md | Agent Definitions | `cross-platform/generated/agents/` | Generated |
| VS Code | MCP via Extension | `cross-platform/generated/mcp/` | Compatible |
| JetBrains IDEs | MCP via Plugin | `cross-platform/generated/mcp/` | Compatible |
| GitHub Copilot | MCP via Extension | `cross-platform/generated/mcp/` | Compatible |
| Cursor | MCP via Settings | `cross-platform/generated/mcp/` | Compatible |
| Windsurf | MCP via Config | `cross-platform/generated/mcp/` | Compatible |

### Using with MCP

Each MCP adapter is a standalone FastMCP server:

```bash
cd cross-platform/generated/mcp/<skill-name>/
pip install -e .
python -m <skill_module>
```

### Using with LangChain

```python
from langchain_cortex import SecurityAuditTool

tool = SecurityAuditTool()
result = tool.run({"target": "./my-project"})
```

### Using with CrewAI

```python
from crewai_cortex import SecurityAuditTool

agent = Agent(
    role="Security Analyst",
    tools=[SecurityAuditTool()]
)
```

### Universal Skill Manifest

Each skill has a platform-agnostic manifest at `cross-platform/manifests/<skill>.json` describing inputs, outputs, dependencies, and platform-specific configuration.

## Project Structure

```
cortex-research-suite/
├── cortex/                    # Python framework (pip install -e .)
│   ├── agents/                # Multi-agent runtime (orchestrator, debate, task graph)
│   ├── evaluation/            # LLM judge, benchmarks, regression detection
│   ├── synthetic/             # Dataset generators (reasoning, research, strategy, adversarial)
│   ├── models/                # Model providers (Anthropic SDK + CLI fallback)
│   ├── telemetry/             # Logging and metrics
│   ├── config/                # Settings with YAML + env var support
│   ├── pipelines/             # Skill runner, dataset pipeline
│   └── utils/                 # I/O, security, sanitization
├── skills/                    # 21 autonomous skills (SKILL.md + scripts/)
├── skill-organism/            # Skill evolution engine
├── cross-platform/            # Generated adapters (MCP, LangChain, CrewAI, OpenAI)
├── tests/                     # 127 tests, 80%+ coverage
├── scripts/                   # CLI entry points
├── docs/                      # Documentation site (GitHub Pages)
└── .github/workflows/         # CI/CD (lint, test, security, release)
```

## Security

All code passes automated security scanning on every push:

- Bandit Python SAST with zero HIGH/MEDIUM findings
- CodeQL semantic code analysis
- Secret scanning with push protection enabled
- Dependabot automated dependency updates
- Prompt injection detection (7 compiled regex patterns)
- Path traversal protection across all I/O operations

Report vulnerabilities to admin@techknowmad.ai. See [SECURITY.md](SECURITY.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide. All PRs require:

- Passing CI checks (bandit, lint, tests)
- One approving review
- No leaked secrets or credentials

## License

MIT — see [LICENSE](LICENSE).
