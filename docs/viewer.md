# Local 3D viewer

`scripts/viewer.py` reads the board's serial output and serves a live 3D view at
`http://localhost:8000`. Unlike the Web Serial viewers, the browser needs no serial permission.

## Launch

1. Wire the sensor ([wiring.md](wiring.md)) and flash the streaming firmware:
   ```bash
   scripts/setup.sh                  # once
   scripts/flash.sh webserial_3d
   ```
2. Close anything else using the serial port (Arduino IDE, a serial monitor, another browser tab
   connected through Web Serial). Only one program can hold the port.
3. Start the viewer:
   ```bash
   python3 scripts/viewer.py                 # Linux default: /dev/ttyACM0, port 8000
   python3 scripts/viewer.py COM5 8000       # Windows example
   python3 scripts/viewer.py /dev/cu.usbmodem1101   # macOS example
   ```
   It opens your browser. If it does not, go to `http://localhost:8000`. Stop it with Ctrl+C.

The page loads three.js from a CDN, so the browser needs internet access.
The status line says **live** while data arrives and **waiting for data...** otherwise.

## Reading the display

- **Axes:** the board model carries arrows for the sensor's own axes: X red, Y green, Z blue.
  Z points up out of the board's top face when it lies flat.
- **Heading / Pitch / Roll:** Euler angles in degrees from the BNO055 fusion output.
- **Calibration:** system, gyro, accel and mag each show a 0 to 3 bar. The viewer lists what to do
  for anything below 3:
  - Gyro: keep the sensor still for a few seconds.
  - Accel: hold it still in several different orientations (each face).
  - Mag: wave it in a figure eight.
  The BNO055 starts at 0 on every power-up, so heading drifts until the magnetometer is calibrated.
- **Controls:** drag to orbit, scroll to zoom, press `Z` to set the current pose as the zero reference.

## Troubleshooting

| Problem | Fix |
|---|---|
| `Device or resource busy` | Another program holds the port. Close it (`fuser /dev/ttyACM0` shows the process on Linux) |
| `Permission denied` | `sudo usermod -aG dialout $USER`, then log out and back in |
| Stuck on "waiting for data..." | Run `python3 scripts/verify.py`. If it fails, see [troubleshooting.md](troubleshooting.md) |
| Port 8000 in use | Pass another port as the second argument |
| Model moves the wrong way | The sensor-to-scene axis mapping is in `viewer/index.html` (`fromBno`) |
