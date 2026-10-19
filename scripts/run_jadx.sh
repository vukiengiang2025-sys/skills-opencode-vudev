#!/usr/bin/env bash
set -euo pipefail
TOOLS_DIR=${1:-/opt/tools}
JADX="$TOOLS_DIR/jadx/bin/jadx"
OUT_DIR=${2:-/work/out}
APK=$3

if [ ! -x "$JADX" ]; then
  echo "jadx not found at $JADX"
  exit 1
fi
mkdir -p "$OUT_DIR/jadx"
"$JADX" -d "$OUT_DIR/jadx" "$APK"
