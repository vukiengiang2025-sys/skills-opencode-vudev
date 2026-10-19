#!/usr/bin/env bash
set -euo pipefail

TOOLS_DIR=${1:-/opt/tools}
mkdir -p "$TOOLS_DIR"
cd "$TOOLS_DIR"

# Download apktool
if [ ! -f "$TOOLS_DIR/apktool.jar" ]; then
  echo "Downloading apktool..."
  wget -q -O apktool.jar https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool.jar || \
  wget -q -O apktool.jar https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.7.0.jar || true
  cat > apktool <<'EOF'
#!/usr/bin/env bash
java -jar "$(dirname "$0")/apktool.jar" "$@"
EOF
  chmod +x apktool
fi

# Download jadx
if [ ! -d "$TOOLS_DIR/jadx" ]; then
  echo "Downloading jadx..."
  JADX_VER=1.4.4
  wget -q -O jadx.zip https://github.com/skylot/jadx/releases/download/v${JADX_VER}/jadx-${JADX_VER}.zip
  unzip -q jadx.zip -d jadx_tmp
  mv jadx_tmp/* $TOOLS_DIR/jadx || true
  rm -rf jadx_tmp jadx.zip
  chmod +x $TOOLS_DIR/jadx/bin/jadx
fi

echo "Tools downloaded to $TOOLS_DIR"
