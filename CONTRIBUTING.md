# Contributing to Cortex Research Suite

Thanks for your interest in contributing! Cortex is an AI Research Operating System where 27 self-evolving skills compete, mutate, and evolve through genetic selection. Whether you're adding a new skill, improving the evolution engine, or building dashboard visualizations — we'd love your help.

## Where to Start

- **New skill** — Follow the [Adding a New Skill](#adding-a-new-skill) guide below
- **Bug fix** — Check [open issues](https://github.com/TECHKNOWMAD-LABS/cortex-research-suite/issues) or report a new one
- **Feature** — Open an issue to discuss your idea first
- **Dashboard** — The Petri Dish and Arena dashboards are standalone HTML — easy to hack on
- **Cross-platform adapter** — We maintain 162 adapters across 6 platforms

## Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes (see code standards below)
4. Run the full test suite: `pytest`
5. Push to your fork and open a PR against `main`
6. Address review feedback

All PRs require:
- Passing CI checks (ruff, bandit, pytest, security scan)
- One approving review
- No leaked secrets or credentials

## Adding a New Skill

Every skill follows the same structure:

```
skills/{skill-name}/
  SKILL.md         — skill instruction (the "DNA" the organism evolves)
  ARENA.md         — arena config (the "program.md" — evolution strategy)
  scripts/         — Python implementation scripts
  references/      — (optional) reference docs, checklists
```

**SKILL.md template:**

```markdown
# {skill-name}
## Overview — what this skill does
## Core instruction — the main prompt
## Output schema — expected JSON output
## Examples — 2-3 before/after demonstrations
## Common gotchas — failure modes to avoid
```

**ARENA.md:** Copy from any existing skill, then update:
- `notes` — what "better" means for YOUR skill
- `eval_budget_seconds` — 30s default, increase for API-heavy skills
- `allowed_mutations` — which improvement strategies apply
- `trilogy` fields — if integrating with MindSpider/BettaFish/MiroFish

**Test your skill:**

```bash
# Generate evaluation dataset
python3 datasets/generators/skill_dataset_generator.py --skill {skill-name} --n 50

# Run LLM-as-Judge evaluation
python3 skills/skill-test-harness/scripts/eval_judge.py \
  --skill {skill-name} \
  --dataset datasets/synthetic/{skill-name}/shard_000.json

# Run evolution (optional — let the organism improve your skill)
python3 skill-organism/enterprise_runner.py --skill {skill-name} --generations 5
```

## Code Standards

**Python:**
- Type hints on all function parameters and return values
- Docstrings for all functions and classes (Google style)
- No bare `except:` — catch specific exceptions
- Parameterized queries for SQL (never f-strings)
- Format with `ruff` (line length 120)

**General:**
- Keep functions focused and reasonably sized
- Meaningful variable names
- Inline comments for non-obvious logic only

## Security Requirements

- Never commit secrets (API keys, tokens, credentials)
- Use `defusedxml` for parsing untrusted XML
- Pass `shell=False` to `subprocess` calls
- Validate all user inputs
- Review dependencies before adding

## Testing

```bash
# Run all 194 tests
pytest

# Run security scan
bandit -r . -q

# Run linter
ruff check .

# Smoke test (verifies all 27 skills, no API key needed)
python scripts/smoke_test.py
```

## Commit Message Format

```
Brief summary of changes (50 chars max)

Longer explanation if needed. Explain the why, not just what changed.
```

## License

MIT. By contributing, you agree that your contributions will be licensed under the same terms.
