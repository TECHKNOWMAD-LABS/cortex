#!/usr/bin/env bash
# Publish pipeline for Cortex Research Suite
# Usage: bash scripts/publish.sh [--dry-run]
set -euo pipefail

DRY_RUN="${1:-}"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

echo "=== Cortex Research Suite — Publish Pipeline ==="
echo ""

# Step 1: Run tests
echo "Step 1: Running tests..."
python3 -m pytest tests/ -q --tb=short 2>&1 || { echo "FAIL: Tests did not pass"; exit 1; }
echo ""

# Step 2: Lint check
echo "Step 2: Running linter..."
python3 -m ruff check cortex/ --select E,F --quiet 2>&1 || echo "WARN: Some lint issues (non-blocking)"
echo ""

# Step 3: Build main package
echo "Step 3: Building cortex-research-suite..."
python3 -m build 2>&1 || { echo "FAIL: Build failed"; exit 1; }
echo ""

# Step 4: Check distribution
echo "Step 4: Checking distribution..."
python3 -m twine check dist/* 2>&1 || { echo "FAIL: twine check failed"; exit 1; }
echo ""

# Step 5: Build de-slop-cli
echo "Step 5: Building de-slop-cli..."
cd packages/de-slop-cli
python3 -m build 2>&1 || { echo "FAIL: de-slop-cli build failed"; exit 1; }
python3 -m twine check dist/* 2>&1 || { echo "FAIL: de-slop-cli twine check failed"; exit 1; }
cd "$REPO_ROOT"
echo ""

# Step 6: Security check
echo "Step 6: Arena HTML security verification..."
python3 -c "
html = open('dashboards/skill_arena_demo.html').read()
assert 'Content-Security-Policy' in html, 'Missing CSP'
assert 'sessionStorage' in html, 'Missing sessionStorage'
assert 'MAX_AUTO_RUNS' in html, 'Missing rate limit'
print('  All security checks passed')
"
echo ""

# Step 7: Publish (or dry-run)
if [ "$DRY_RUN" = "--dry-run" ]; then
    echo "DRY RUN — skipping PyPI upload"
    echo "To publish for real: bash scripts/publish.sh"
else
    echo "Step 7: Publishing to PyPI..."
    echo "  Upload cortex-research-suite..."
    python3 -m twine upload dist/* || echo "WARN: Upload may have failed (check PyPI)"
    echo "  Upload de-slop-cli..."
    cd packages/de-slop-cli
    python3 -m twine upload dist/* || echo "WARN: Upload may have failed (check PyPI)"
    cd "$REPO_ROOT"
fi

echo ""
echo "=== Publish pipeline complete ==="
