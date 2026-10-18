#!/usr/bin/env bash
# Compile and flash a sketch to the XIAO ESP32S3.
# Usage: scripts/flash.sh [sketch] [port]     (defaults: webserial_3d, /dev/ttyACM0)
set -euo pipefail

SKETCH="${1:-webserial_3d}"
PORT="${2:-/dev/ttyACM0}"
DIR="$(cd "$(dirname "$0")/.." && pwd)/firmware/$SKETCH"
FQBN="esp32:esp32:XIAO_ESP32S3"

[ -d "$DIR" ] || { echo "No such sketch: $SKETCH (try webserial_3d or i2c_scan)" >&2; exit 1; }
arduino-cli compile --fqbn "$FQBN" "$DIR"
arduino-cli upload -p "$PORT" --fqbn "$FQBN" "$DIR"
