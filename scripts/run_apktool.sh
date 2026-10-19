#!/usr/bin/env bash
set -euo pipefail
TOOLS_DIR=${1:-/opt/tools}
APK=$2
OUT_DIR=${3:-/work/out}

APKTOOL_JAR="$TOOLS_DIR/apktool.jar"
APKTOOL_SCRIPT="$TOOLS_DIR/apktool"

if [ ! -f "$APKTOOL_JAR" ]; then
  echo "apktool jar not found at $APKTOOL_JAR"
  exit 1
fi

NAME=$(basename "$APK" .apk)
mkdir -p "$OUT_DIR/$NAME/apktool"
$APKTOOL_SCRIPT d "$APK" -o "$OUT_DIR/$NAME/apktool" -f
