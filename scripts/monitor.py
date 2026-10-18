#!/usr/bin/env python3
"""Print the serial output from the board. Usage: monitor.py [port] [seconds]"""
import sys
import time

import serial

port = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyACM0"
seconds = float(sys.argv[2]) if len(sys.argv) > 2 else 10

with serial.Serial(port, 115200, timeout=1) as s:
    end = time.time() + seconds
    while time.time() < end:
        line = s.readline().decode(errors="replace").rstrip()
        if line:
            print(line)
