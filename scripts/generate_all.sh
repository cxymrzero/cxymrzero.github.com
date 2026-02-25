#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 "$ROOT/scripts/generate_categories.py"

if [[ "${1:-}" == "serve" ]]; then
  cd "$ROOT"
  bundle exec jekyll serve
else
  cd "$ROOT"
  bundle exec jekyll build
fi
