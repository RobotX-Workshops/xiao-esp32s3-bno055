#!/usr/bin/env bash
# Install arduino-cli (if missing), the ESP32 core and the BNO055 libraries.
set -euo pipefail

if ! command -v arduino-cli >/dev/null; then
  echo "arduino-cli not found. Install it from https://arduino.github.io/arduino-cli/latest/installation/" >&2
  echo "e.g. (Linux/macOS): curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | BINDIR=~/.local/bin sh" >&2
  exit 1
fi

arduino-cli core update-index
arduino-cli core install esp32:esp32
arduino-cli lib install "Adafruit BNO055" "Adafruit Unified Sensor" "Adafruit BusIO"
pip install --user pyserial
echo "Setup complete."
