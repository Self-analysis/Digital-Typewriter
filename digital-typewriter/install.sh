#!/bin/bash
# Digital Typewriter - Fedora 44 installation
set -euo pipefail

APP_ID="com.digitaltypewriter.app"
PREFIX="/usr/share/digital-typewriter"
DESKTOP="/usr/share/applications/${APP_ID}.desktop"
METainfo="/usr/share/metainfo/${APP_ID}.metainfo.xml"
ICON_DIR="/usr/share/icons/hicolor/scalable/apps"
BIN="/usr/bin/digital-typewriter"

if ! grep -q '^ID=fedora$' /etc/os-release; then
  echo "This installer is intended for Fedora."
  exit 1
fi

sudo dnf install -y python3 python3-gobject gtk4 libadwaita desktop-file-utils appstream

sudo rm -rf "$PREFIX"
sudo mkdir -p "$PREFIX" "$PREFIX/ui" "$PREFIX/layouts" "$PREFIX/assets" /usr/share/metainfo "$ICON_DIR"

sudo cp main.py app.py editor.py keyboard.py "$PREFIX/"
sudo cp -r ui/. "$PREFIX/ui/"
sudo cp -r layouts/. "$PREFIX/layouts/"
sudo cp -r assets/. "$PREFIX/assets/"

sudo install -Dm644 "digital-typewriter.desktop" "$DESKTOP"
sudo install -Dm644 "com.digitaltypewriter.app.metainfo.xml" "$METainfo"
if [ -f "$PREFIX/assets/icon.svg" ]; then
  sudo install -Dm644 "$PREFIX/assets/icon.svg" "$ICON_DIR/${APP_ID}.svg"
fi

sudo ln -sf "$PREFIX/main.py" "$BIN"
sudo chmod 755 "$PREFIX/main.py"

sudo desktop-file-validate "$DESKTOP"
if command -v appstreamcli >/dev/null 2>&1; then
  appstreamcli validate "$METainfo" || true
fi
sudo update-desktop-database /usr/share/applications || true
sudo gtk-update-icon-cache -q -f /usr/share/icons/hicolor || true

cat <<EOF

Digital Typewriter installed successfully.

Launch it from GNOME Applications as:
  Digital Typewriter

Or run:
  digital-typewriter
EOF
