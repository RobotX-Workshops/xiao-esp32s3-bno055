# Wiring

![Wiring diagram](wiring.svg)

| XIAO ESP32S3 | BNO055 breakout | Notes |
|---|---|---|
| D4 (GPIO5) | SDA | I2C data |
| D5 (GPIO6) | SCL | I2C clock |
| 3V3 | VIN | 3.3 V is fine for Adafruit-style breakouts |
| GND | GND | common ground |

- Power comes from the USB-C cable. Nothing else is needed.
- Leave ADR open (or low) for I2C address `0x28`. Tie it high for `0x29`
  and set `BNO055_ADDR` in `firmware/webserial_3d/webserial_3d.ino`.
- The breakout needs I2C pull-ups on SDA and SCL. Adafruit and most clone boards
  include them. If yours does not, add 4.7 kOhm resistors from each line to 3V3.
- Check the pin positions against the labels printed on your XIAO. D4/D5 are
  GPIO5/GPIO6, not the pins next to them.
