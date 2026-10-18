#!/usr/bin/env python3
"""Check that the flashed webserial_3d firmware is streaming sensible BNO055 data.
Usage: verify.py [port]. Exits 0 on success, 1 otherwise."""
import math
import sys
import time

import serial

port = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyACM0"
quat = None
calib = None

with serial.Serial(port, 115200, timeout=1) as s:
    end = time.time() + 6
    while time.time() < end and not (quat and calib):
        line = s.readline().decode(errors="replace").strip()
        if line.startswith("Quaternion:"):
            quat = [float(v) for v in line.split(":")[1].split(",")]
        elif line.startswith("Calibration:"):
            calib = [int(v) for v in line.split(":")[1].split(",")]
        elif "No BNO055" in line:
            print("FAIL:", line)
            sys.exit(1)

if not (quat and calib):
    print("FAIL: no data received. Is the webserial_3d firmware flashed?")
    sys.exit(1)

norm = math.sqrt(sum(v * v for v in quat))
if abs(norm - 1) > 0.05:
    print(f"FAIL: quaternion norm {norm:.3f}, expected ~1")
    sys.exit(1)

print(f"OK: quaternion {quat} (norm {norm:.3f}); calibration sys/gyro/accel/mag = {calib}")
