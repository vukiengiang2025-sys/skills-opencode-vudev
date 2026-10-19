#!/usr/bin/env bash
set -euo pipefail

CMD=${1:-}
shift || true

case "$CMD" in
  analyze)
    python /work/app/cli.py analyze "$@"
    ;;
  api)
    python /work/app/api.py
    ;;
  *)
    echo "Usage: entrypoint.sh [analyze <apk> -o <outdir>] | [api]"
    exit 2
    ;;
esac
