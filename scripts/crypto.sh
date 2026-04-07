#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CLI_PATH="$PROJECT_ROOT/src/crypto.py"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 is required but not found in PATH" >&2
  exit 1
fi

if [[ ! -f "$CLI_PATH" ]]; then
  echo "Error: expected CLI at $CLI_PATH" >&2
  exit 1
fi

python3 "$CLI_PATH" "$@"
