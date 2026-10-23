#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
python "$ROOT/code/final_experiment.py" --out "$ROOT" --n-mc 20000
