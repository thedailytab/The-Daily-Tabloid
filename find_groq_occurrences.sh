#!/usr/bin/env bash
set -euo pipefail
echo "Searching for 'groq' occurrences (excluding node_modules/.git)..."
if command -v rg >/dev/null 2>&1; then
  rg -n --hidden --glob '!node_modules' --glob '!.git' 'groq' || true
else
  grep -RIn --exclude-dir=node_modules --exclude-dir=.git 'groq' || true
fi
echo
echo "Search complete. Review the occurrences above before making changes."