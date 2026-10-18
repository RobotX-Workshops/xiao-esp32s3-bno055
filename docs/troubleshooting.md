# Troubleshooting

Flash the scanner first: `scripts/flash.sh i2c_scan`, then `python3 scripts/monitor.py`.

| Symptom | Likely cause | Fix |
|---|---|---|
| `scan done, 0 device(s)` and `i2c.master: probe device timeout` | SDA or SCL not connected, or not pulled up | Reseat the wires, check 3V3 and GND, and make sure SDA is on D4 and SCL on D5 |
| Device found at `0x29` | ADR pin is high | Set `BNO055_ADDR` to `0x29` in the firmware |
| `No BNO055 detected` loops forever | The scanner finds nothing | Same as the first row |
| Chip ID is not `0xA0` | The device at `0x28` is not a BNO055 | Check for another I2C device on the bus |
| Calibration stays at 0 | Sensor has not been moved | See "Calibration" in the README |
| No serial port appears | Charge-only USB cable | Use a data cable. Hold BOOT while plugging in to enter the bootloader |
| `Permission denied` on `/dev/ttyACM0` | User not in `dialout` | `sudo usermod -aG dialout $USER`, then log out and back in |

## Diagnosing a stuck line

If the scan times out, a line may be held low. Flash a sketch that reads the pins
with the internal pull-up enabled. A floating pin reads 1, so a pin that reads 0
is being held low by a wire or a short. A pin that is high with nothing attached
is being pulled up by the breakout.
